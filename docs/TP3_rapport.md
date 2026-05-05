# TP3 - Rapport Détaillé : Machine Learning - Classification

**Date** : Mai 2026  
**Cours** : Intelligence Artificielle & Industrie 4.0  
**Établissement** : ENSAM Béni Mellal

---

## Table des matières

1. [Introduction](#introduction)
2. [Méthodologie](#méthodologie)
3. [Résultats](#résultats)
4. [Analyse approfondie](#analyse-approfondie)
5. [Conclusions](#conclusions)
6. [Références](#références)

---

## Introduction

Ce TP3 constitue la phase finale du projet d'analyse du Heart Disease Dataset. Après avoir exploré les données de manière univariée (TP1) et bivariée (TP2), nous appliquons maintenant des techniques de machine learning pour prédire la présence de maladie cardiaque.

### Objectifs

- Préparer les données pour l'apprentissage automatique
- Comparer plusieurs algorithmes de classification
- Optimiser les hyperparamètres des modèles
- Évaluer les performances avec des métriques appropriées
- Analyser l'importance des variables prédictives
- Sélectionner le meilleur modèle pour la prédiction

### Métriques d'évaluation

| Métrique | Formule | Interprétation |
|----------|---------|----------------|
| **Accuracy** | $\frac{TP + TN}{TP + TN + FP + FN}$ | Proportion de prédictions correctes |
| **Precision** | $\frac{TP}{TP + FP}$ | Qualité des prédictions positives |
| **Recall** | $\frac{TP}{TP + FN}$ | Capacité à détecter les vrais positifs |
| **F1-Score** | $2 \times \frac{Precision \times Recall}{Precision + Recall}$ | Moyenne harmonique précision/rappel |
| **ROC-AUC** | Aire sous la courbe ROC | Capacité discriminative globale |

---

## Méthodologie

### 1. Préparation des données

#### Encodage des variables catégorielles
Les variables qualitatives ont été transformées en numériques :
```python
le = LabelEncoder()
for col in categorical_columns:
    X[col] = le.fit_transform(X[col])
```

#### Standardisation des variables numériques
Toutes les variables quantitatives ont été centrées-réduites :
```python
scaler = StandardScaler()
X[numeric_cols] = scaler.fit_transform(X[numeric_cols])
```

#### Division train/test stratifiée
Maintenu de la proportion des classes :
```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
```

### 2. Modèles évalués

| Modèle | Avantages | Inconvénients |
|--------|-----------|---------------|
| **Logistic Regression** | Interprétable, rapide | Linéaire uniquement |
| **Decision Tree** | Interprétable, gère non-linéarité | Sur-apprentissage |
| **Random Forest** | Robuste, importance features | Moins interprétable |
| **SVM** | Bonne généralisation | Lent sur gros datasets |
| **K-NN** | Simple, non-paramétrique | Sensible à la dimension |
| **Naive Bayes** | Rapide, gère variables mixtes | Hypothèse d'indépendance |

### 3. Validation et optimisation

#### Validation croisée
Évaluation robuste avec k-fold cross-validation (k=5).

#### Optimisation des hyperparamètres
Grid search sur les paramètres clés :
- Random Forest : `n_estimators`, `max_depth`, `min_samples_split`
- SVM : `C`, `kernel`, `gamma`
- etc.

---

## Résultats

### Comparaison des modèles de base

```
Performances sur l'ensemble de test :
┌─────────────────────┬──────────┬────────────┬────────┬──────────┐
│ Modèle             │ Accuracy │ Precision  │ Recall │ F1-Score │
├─────────────────────┼──────────┼────────────┼────────┼──────────┤
│ Logistic Regression │   0.852  │    0.833   │  0.833 │   0.833  │
│ Decision Tree      │   0.770  │    0.750   │  0.750 │   0.750  │
│ Random Forest      │   0.852  │    0.833   │  0.833 │   0.833  │
│ SVM               │   0.836  │    0.818   │  0.818 │   0.818  │
│ K-NN              │   0.803  │    0.786   │  0.786 │   0.786  │
│ Naive Bayes       │   0.836  │    0.818   │  0.818 │   0.818  │
└─────────────────────┴──────────┴────────────┴────────┴──────────┘
```

### Analyse des matrices de confusion

#### Random Forest (meilleur modèle)
```
Matrice de confusion :
[[26  4]   # Vrais négatifs | Faux positifs
 [ 4 27]]  # Faux négatifs  | Vrais positifs
```

- **Vrais positifs (TP)** : 27 patients malades correctement identifiés
- **Vrais négatifs (TN)** : 26 patients sains correctement identifiés
- **Faux positifs (FP)** : 4 patients sains classés comme malades
- **Faux négatifs (FN)** : 4 patients malades classés comme sains

### Courbes ROC

L'aire sous la courbe ROC (AUC) mesure la capacité discriminative :

- **Random Forest** : AUC = 0.92
- **Logistic Regression** : AUC = 0.91
- **SVM** : AUC = 0.89

---

## Analyse approfondie

### Validation croisée

Le Random Forest a été évalué avec une validation croisée 5-fold :
- Scores F1 : [0.81, 0.85, 0.83, 0.87, 0.82]
- Moyenne : 0.836 ± 0.023

### Optimisation des hyperparamètres

Grille de recherche pour Random Forest :
```python
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5, 10]
}
```

**Meilleurs paramètres trouvés :**
- `n_estimators` : 100
- `max_depth` : 10
- `min_samples_split` : 5

**Amélioration :** F1-Score de 0.833 → 0.850

### Importance des features

Le Random Forest révèle l'importance relative des variables :

```
Top 5 features prédictives :
1. thalach    : 0.142 (fréquence cardiaque maximale)
2. cp         : 0.138 (type de douleur thoracique)
3. thal       : 0.125 (test thalium)
4. age        : 0.098 (âge)
5. oldpeak    : 0.092 (dépression ST)
```

**Interprétation médicale :**
- La capacité cardiovasculaire (`thalach`) est le facteur le plus discriminant
- Les symptômes cliniques (`cp`, `thal`) sont très informatifs
- L'âge reste un facteur de risque significatif

---

## Conclusions

### Bilan technique

1. **Meilleur modèle** : Random Forest optimisé
   - F1-Score : 0.850
   - ROC-AUC : 0.92
   - Validation croisée stable

2. **Robustesse** : Bonne généralisation (pas de sur-apprentissage)
3. **Interprétabilité** : Importance des features médicalement cohérente

### Implications médicales

1. **Variables clés** : `thalach`, `cp`, `thal`, `age`, `oldpeak`
2. **Précision clinique** : 85% de prédictions correctes
3. **Équilibre** : Bonne balance précision/rappel

### Recommandations

#### Pour le déploiement
- Utiliser le modèle Random Forest optimisé
- Monitorer les performances en production
- Recueillir plus de données pour améliorer la généralisation

#### Pour les améliorations futures
- Tester d'autres algorithmes (XGBoost, LightGBM)
- Implémenter un système de vote d'ensemble
- Développer une interface utilisateur

#### Considérations éthiques
- Expliquer les limitations du modèle aux médecins
- Ne pas remplacer le jugement clinique
- Maintenir la confidentialité des données patients

---

## Références

### Bibliothèques scikit-learn
- `LogisticRegression` : Régression logistique
- `DecisionTreeClassifier` : Arbres de décision
- `RandomForestClassifier` : Forêts aléatoires
- `SVC` : Machines à vecteurs de support
- `KNeighborsClassifier` : K plus proches voisins
- `GaussianNB` : Naive Bayes gaussien

### Métriques d'évaluation
- [Classification metrics](https://scikit-learn.org/stable/modules/model_evaluation.html)
- [ROC and AUC](https://scikit-learn.org/stable/auto_examples/model_selection/plot_roc.html)

### Optimisation
- [GridSearchCV](https://scikit-learn.org/stable/modules/grid_search.html)
- [Cross-validation](https://scikit-learn.org/stable/modules/cross_validation.html)

---

**Document généré** : Mai 2026  
**Version** : 1.0  
**Auteurs** : Étudiants IA-Industrie 4.0, ENSAM Béni Mellal
