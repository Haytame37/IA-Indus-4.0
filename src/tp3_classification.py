"""
TP3 - Machine Learning : Classification du Heart Disease Dataset

Module : tp3_classification.py
Description : Implémentation de modèles de classification pour prédire
             la présence de maladie cardiaque.

Auteur : Étudiants IA-Industrie 4.0
Date : 2026
Version : 1.0
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                           f1_score, roc_auc_score, confusion_matrix,
                           classification_report, roc_curve)
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Configuration graphique
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['font.size'] = 10
sns.set_style('whitegrid')

DATA_DIR = Path(__file__).parent.parent / 'data'
CSV_FILE = DATA_DIR / 'Base_Maladie_Cardiaque.csv'


def load_and_preprocess_data(filepath=None):
    """Charge et prétraite les données pour le ML."""
    if filepath is None:
        filepath = CSV_FILE

    df = pd.read_csv(filepath)

    # Conversion des variables catégorielles
    categorical_vars = ['sex', 'cp', 'fbs', 'restecg', 'exang', 'slope', 'thal', 'target']
    df[categorical_vars] = df[categorical_vars].apply(lambda x: x.astype('category'))

    # Séparation features/target
    X = df.drop('target', axis=1)
    y = df['target']

    # Encodage des variables catégorielles
    le = LabelEncoder()
    for col in X.select_dtypes(include=['category']).columns:
        X[col] = le.fit_transform(X[col])

    # Standardisation des variables numériques
    numeric_cols = X.select_dtypes(include=['number']).columns
    scaler = StandardScaler()
    X[numeric_cols] = scaler.fit_transform(X[numeric_cols])

    return X, y, df


def split_data(X, y, test_size=0.2, random_state=42):
    """Divise les données en train/test."""
    return train_test_split(X, y, test_size=test_size, random_state=random_state,
                          stratify=y)


def evaluate_model(model, X_train, X_test, y_train, y_test, model_name=""):
    """Évalue un modèle de classification."""
    # Entraînement
    model.fit(X_train, y_train)

    # Prédictions
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None

    # Métriques
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred),
        'recall': recall_score(y_test, y_pred),
        'f1_score': f1_score(y_test, y_pred),
    }

    if y_pred_proba is not None:
        metrics['roc_auc'] = roc_auc_score(y_test, y_pred_proba)

    # Matrice de confusion
    cm = confusion_matrix(y_test, y_pred)

    print(f"\n=== Évaluation : {model_name} ===")
    print(f"Accuracy  : {metrics['accuracy']:.3f}")
    print(f"Precision : {metrics['precision']:.3f}")
    print(f"Recall    : {metrics['recall']:.3f}")
    print(f"F1-Score  : {metrics['f1_score']:.3f}")
    if 'roc_auc' in metrics:
        print(f"ROC-AUC   : {metrics['roc_auc']:.3f}")

    print(f"\nMatrice de confusion :\n{cm}")
    print(f"\nRapport de classification :\n{classification_report(y_test, y_pred)}")

    return metrics, cm, y_pred, y_pred_proba


def plot_confusion_matrix(cm, model_name="", save_path=None):
    """Affiche la matrice de confusion."""
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=['Sain (0)', 'Malade (1)'],
                yticklabels=['Sain (0)', 'Malade (1)'])
    plt.title(f'Matrice de confusion - {model_name}')
    plt.xlabel('Prédiction')
    plt.ylabel('Réel')
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Matrice sauvegardée : {save_path}")
    plt.show()


def plot_roc_curve(y_test, y_pred_proba, model_name="", save_path=None):
    """Affiche la courbe ROC."""
    if y_pred_proba is None:
        print(f"Modèle {model_name} ne supporte pas predict_proba")
        return

    fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
    roc_auc = roc_auc_score(y_test, y_pred_proba)

    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='darkorange', linewidth=2,
             label=f'ROC curve (AUC = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', linewidth=2, linestyle='--',
             label='Random classifier')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(f'Courbe ROC - {model_name}')
    plt.legend(loc="lower right")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ ROC curve sauvegardée : {save_path}")
    plt.show()


def compare_models(X_train, X_test, y_train, y_test, models=None):
    """Compare plusieurs modèles de classification."""
    if models is None:
        models = {
            'Logistic Regression': LogisticRegression(random_state=42),
            'Decision Tree': DecisionTreeClassifier(random_state=42),
            'Random Forest': RandomForestClassifier(random_state=42, n_estimators=100),
            'SVM': SVC(random_state=42, probability=True),
            'K-NN': KNeighborsClassifier(),
            'Naive Bayes': GaussianNB()
        }

    results = {}
    cms = {}

    for name, model in models.items():
        print(f"\n{'='*50}")
        print(f"Évaluation du modèle : {name}")
        print('='*50)

        metrics, cm, y_pred, y_pred_proba = evaluate_model(
            model, X_train, X_test, y_train, y_test, name
        )

        results[name] = metrics
        cms[name] = cm

        # Visualisations
        plot_confusion_matrix(cm, name)
        if y_pred_proba is not None:
            plot_roc_curve(y_test, y_pred_proba, name)

    # Comparaison finale
    df_results = pd.DataFrame(results).T
    df_results = df_results.round(3)

    print(f"\n{'='*70}")
    print("COMPARAISON FINALE DES MODÈLES")
    print('='*70)
    print(df_results.to_string())

    # Meilleur modèle
    best_model = df_results['f1_score'].idxmax()
    best_score = df_results['f1_score'].max()

    print(f"\n🏆 Meilleur modèle : {best_model} (F1-Score = {best_score:.3f})")

    return df_results, cms


def cross_validation_scores(model, X, y, cv=5):
    """Effectue une validation croisée."""
    scores = cross_val_score(model, X, y, cv=cv, scoring='f1')
    print(f"Validation croisée (CV={cv}) :")
    print(f"  Scores F1 : {scores}")
    print(f"  Moyenne   : {scores.mean():.3f} ± {scores.std():.3f}")
    return scores


def optimize_hyperparameters(model, param_grid, X_train, y_train, cv=5):
    """Optimise les hyperparamètres avec GridSearchCV."""
    grid_search = GridSearchCV(model, param_grid, cv=cv, scoring='f1', n_jobs=-1)
    grid_search.fit(X_train, y_train)

    print(f"\nOptimisation des hyperparamètres :")
    print(f"Meilleurs paramètres : {grid_search.best_params_}")
    print(f"Meilleur score F1    : {grid_search.best_score_:.3f}")

    return grid_search.best_estimator_, grid_search.best_params_, grid_search.best_score_


def analyze_feature_importance(model, X_train, feature_names, model_name="", save_path=None):
    """Analyse l'importance des features (si disponible)."""
    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
        indices = np.argsort(importances)[::-1]

        plt.figure(figsize=(10, 6))
        plt.title(f'Importance des features - {model_name}')
        plt.bar(range(len(importances)), importances[indices],
                align='center', color='steelblue')
        plt.xticks(range(len(importances)), [feature_names[i] for i in indices],
                   rotation=45, ha='right')
        plt.xlabel('Features')
        plt.ylabel('Importance')
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Importance sauvegardée : {save_path}")
        plt.show()

        # Top 5 features
        top_features = pd.DataFrame({
            'Feature': [feature_names[i] for i in indices[:5]],
            'Importance': importances[indices[:5]]
        })
        print(f"\nTop 5 features pour {model_name} :")
        print(top_features.to_string(index=False))

        return importances, indices
    else:
        print(f"Le modèle {model_name} ne supporte pas l'importance des features")
        return None, None


def main():
    """Exécute l'analyse ML complète."""
    print('=' * 70)
    print('TP3 - MACHINE LEARNING : CLASSIFICATION HEART DISEASE')
    print('=' * 70)

    # Chargement et prétraitement
    X, y, df = load_and_preprocess_data()
    print(f"✓ Données chargées : {X.shape[0]} échantillons, {X.shape[1]} features")

    # Division train/test
    X_train, X_test, y_train, y_test = split_data(X, y)
    print(f"✓ Division : Train {X_train.shape[0]}, Test {X_test.shape[0]}")

    # Comparaison des modèles
    results, cms = compare_models(X_train, X_test, y_train, y_test)

    # Analyse du meilleur modèle (Random Forest)
    print(f"\n{'='*50}")
    print("ANALYSE APPROFONDIE - RANDOM FOREST")
    print('='*50)

    rf_model = RandomForestClassifier(random_state=42, n_estimators=100)
    rf_model.fit(X_train, y_train)

    # Validation croisée
    cross_validation_scores(rf_model, X_train, y_train)

    # Optimisation des hyperparamètres
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [None, 10, 20],
        'min_samples_split': [2, 5, 10]
    }

    best_rf, best_params, best_score = optimize_hyperparameters(
        rf_model, param_grid, X_train, y_train
    )

    # Évaluation du modèle optimisé
    evaluate_model(best_rf, X_train, X_test, y_train, y_test, "Random Forest Optimisé")

    # Importance des features
    analyze_feature_importance(best_rf, X_train, X.columns.tolist(), "Random Forest")

    print(f"\n{'='*70}")
    print('TP3 TERMINÉ - ANALYSE MACHINE LEARNING COMPLÈTE')
    print('='*70)


if __name__ == '__main__':
    main()
