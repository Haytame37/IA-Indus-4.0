"""
train.py
--------
Entraîne un pipeline sklearn complet (prétraitement + Random Forest)
sur le dataset de tâches (6 catégories dont Créativité), évalue les
performances et sauvegarde le modèle.

Usage :
    python generate_dataset.py   # génère tasks_dataset.csv
    python train.py              # entraîne et sauvegarde model.pkl
"""

import json
import joblib
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, StandardScaler


# ------------------------------------------------------------------
# Chargement et préparation
# ------------------------------------------------------------------
def load_data(path: str = "tasks_dataset.csv"):
    df = pd.read_csv(path)

    # LabelEncoder gère automatiquement les 6 catégories incluant Créativité
    le = LabelEncoder()
    df["category_enc"] = le.fit_transform(df["category"])
    joblib.dump(le, "label_encoder.pkl")

    features = ["description", "category_enc", "urgency", "effort_hours", "goal_aligned"]
    X = df[features]
    y = df["impact_class"]

    return X, y, le


# ------------------------------------------------------------------
# Construction du pipeline sklearn
# ------------------------------------------------------------------
def build_pipeline() -> Pipeline:
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "tfidf",
                TfidfVectorizer(
                    max_features=600,       # Augmenté pour 6 catégories
                    ngram_range=(1, 2),
                    min_df=2,
                    sublinear_tf=True,
                ),
                "description",
            ),
            (
                "scaler",
                StandardScaler(),
                ["urgency", "effort_hours", "category_enc"],
            ),
            (
                "pass",
                "passthrough",
                ["goal_aligned"],
            ),
        ],
        remainder="drop",
    )

    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", RandomForestClassifier(
            n_estimators=200,       # Base augmentée pour 6 classes
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            class_weight="balanced",
            n_jobs=-1,
        )),
    ])

    return pipeline


# ------------------------------------------------------------------
# Recherche des meilleurs hyperparamètres (GridSearch)
# ------------------------------------------------------------------
def tune_hyperparameters(pipeline: Pipeline, X_train, y_train) -> Pipeline:
    print("\nRecherche des hyperparamètres (GridSearchCV)...")

    param_grid = {
        # 100 retiré — capacité insuffisante pour 5 classes d'impact + 6 catégories
        "classifier__n_estimators": [200, 300],
        "classifier__max_depth": [8, 10, None],
        "classifier__min_samples_split": [2, 5],
    }

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    search = GridSearchCV(
        pipeline,
        param_grid,
        scoring="f1_macro",
        cv=cv,
        n_jobs=-1,
        verbose=1,
    )
    search.fit(X_train, y_train)

    print(f"\nMeilleurs paramètres : {search.best_params_}")
    print(f"Meilleur F1-macro (CV) : {search.best_score_:.4f}")

    return search.best_estimator_


# ------------------------------------------------------------------
# Évaluation et rapport
# ------------------------------------------------------------------
def evaluate(pipeline: Pipeline, X_test, y_test) -> dict:
    y_pred = pipeline.predict(X_test)
    classes = pipeline.classes_

    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average="macro")
    cm = confusion_matrix(y_test, y_pred, labels=classes)

    print("\n" + "="*50)
    print("RAPPORT DE CLASSIFICATION")
    print("="*50)
    print(classification_report(y_test, y_pred, target_names=classes))

    print("MATRICE DE CONFUSION")
    print(f"{'':>10}", end="")
    for c in classes:
        print(f"{c:>10}", end="")
    print()
    for i, c in enumerate(classes):
        print(f"{c:>10}", end="")
        for val in cm[i]:
            print(f"{val:>10}", end="")
        print()

    # Résumé F1 par classe formaté
    print("\n" + "="*50)
    print("F1-SCORE PAR CLASSE (résumé)")
    print("="*50)
    from sklearn.metrics import f1_score as f1_per_class
    f1_scores = f1_per_class(y_test, y_pred, average=None, labels=classes)
    for cls, f1_val in zip(classes, f1_scores):
        bar = "█" * int(f1_val * 20)
        status = "✓" if f1_val >= 0.75 else "~" if f1_val >= 0.60 else "✗"
        print(f"  {status} {cls:<8}  F1 = {f1_val:.3f}  {bar}")

    print(f"\nAccuracy  : {acc:.4f}")
    print(f"F1-macro  : {f1:.4f}")

    return {
        "accuracy": round(float(acc), 4),
        "f1_macro": round(float(f1), 4),
        "classes": list(classes),
        "confusion_matrix": cm.tolist(),
        "f1_per_class": {cls: round(float(s), 4) for cls, s in zip(classes, f1_scores)},
    }


# ------------------------------------------------------------------
# Point d'entrée
# ------------------------------------------------------------------
def train(data_path: str = "tasks_dataset.csv", tune: bool = True):
    print("Chargement des données...")
    X, y, label_encoder = load_data(data_path)
    print(f"  {len(X)} exemples · {y.nunique()} classes d'impact")
    print(f"  Catégories encodées : {list(label_encoder.classes_)}")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )
    print(f"  Train : {len(X_train)} | Test : {len(X_test)}")

    pipeline = build_pipeline()

    if tune:
        pipeline = tune_hyperparameters(pipeline, X_train, y_train)
    else:
        print("\nEntraînement sans GridSearch...")
        pipeline.fit(X_train, y_train)

    metrics = evaluate(pipeline, X_test, y_test)

    joblib.dump(pipeline, "model.pkl")
    print("\nModèle sauvegardé : model.pkl")

    with open("metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)
    print("Métriques sauvegardées : metrics.json")

    return pipeline, metrics


if __name__ == "__main__":
    # tune=False pour un test rapide sans GridSearch
    train(tune=True)
