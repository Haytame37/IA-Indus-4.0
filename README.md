# IA-Industrie 4.0 — Travaux Pratiques (TP)

Bienvenue dans le dépôt des Travaux Pratiques (TP) pour le cours **Intelligence Artificielle & Industrie 4.0** à l'Ecole Nationale Supérieure d'Appliquées (ENSAM) - Béni Mellal.

## 📋 Vue d'ensemble

Ce dépôt contient trois travaux pratiques progressifs sur l'analyse de données et le machine learning appliqués au contexte industriel :

| TP      | Titre             | Objectifs                                                           |
| ------- | ----------------- | ------------------------------------------------------------------- |
| **TP1** | Analyse Univariée | Exploration exploratoire, statistiques descriptives, visualisations |
| **TP2** | Analyse Bivariée  | Corrélations, régressions simples, associations                     |
| **TP3** | Machine Learning  | Classification avec différents modèles, optimisation, évaluation   |

---

## 🎯 TP1 - Analyse Univariée

### Objectifs pédagogiques

- ✅ Charger et explorer un dataset réel (Heart Disease Dataset)
- ✅ Distinguer variables quantitatives et qualitatives
- ✅ Calculer les indicateurs statistiques (moyenne, médiane, écart-type, etc.)
- ✅ Créer des visualisations appropriées (histogrammes, boxplots, KDE, QQ-plot)
- ✅ Détecter les outliers
- ✅ Automatiser l'analyse avec des fonctions réutilisables

### Structure du TP1

```
TP1/
├── data/
│   └── Base_Maladie_Cardiaque.csv    # Dataset (303 patients, 14 variables)
├── src/
│   ├── tp1_analysis.py                # Script principal (fonction + analyse)
│   └── tp1_utils.py                   # (Optionnel) Utilitaires supplémentaires
├── notebooks/
│   └── TP1_exploration.ipynb          # Notebook interactif Jupyter
└── docs/
    └── TP1_rapport.md                 # Rapport détaillé avec résultats
```

### Données utilisées

**Heart Disease Dataset** (UCI Machine Learning Repository)

- 📊 303 patients
- 📈 14 variables (âge, sexe, type de douleur thoracique, cholestérol, etc.)
- 🎯 Cible : présence/absence de maladie cardiaque

### Variables clés

| Variable  | Type         | Description                      |
| --------- | ------------ | -------------------------------- |
| `age`     | Quantitative | Âge du patient (années)          |
| `sex`     | Qualitative  | 0 = Femme, 1 = Homme             |
| `cp`      | Qualitative  | Type de douleur thoracique       |
| `chol`    | Quantitative | Cholestérol (mg/dl)              |
| `thalach` | Quantitative | Fréquence cardiaque max atteinte |
| `target`  | Qualitative  | 0 = Sain, 1 = Malade             |

### Résultats principaux (TP1)

#### Variable `age`

- **Moyenne** : 54.5 ans
- **Médiane** : 55.5 ans
- **Écart-type** : 9.0 ans
- **Distribution** : Quasi-normale, symétrique
- **Asymétrie** : 0.12 (légèrement asymétrique)

#### Variable `sex`

- **Répartition** : 68% d'hommes, 32% de femmes
- **Observation** : Dataset déséquilibré (biais à considérer)

---

## 🤖 TP3 - Machine Learning - Classification

### Objectifs pédagogiques

- ✅ Préparer les données pour l'apprentissage automatique
- ✅ Comparer 6 algorithmes de classification (Logistic Regression, Decision Tree, Random Forest, SVM, K-NN, Naive Bayes)
- ✅ Optimiser les hyperparamètres avec GridSearchCV
- ✅ Évaluer les performances avec métriques appropriées (Accuracy, Precision, Recall, F1-Score, ROC-AUC)
- ✅ Analyser l'importance des variables prédictives
- ✅ Sélectionner le meilleur modèle pour la prédiction

### Structure du TP3

```
TP3/
├── src/
│   └── tp3_classification.py          # 🆕 Module ML complet
├── notebooks/
│   └── TP3_classification.ipynb      # 🆕 Notebook interactif ML
└── docs/
    └── TP3_rapport.md                 # 🆕 Rapport détaillé avec résultats
```

### Modèles implémentés

| Modèle | Avantages | Complexité | Interprétabilité |
|--------|-----------|------------|------------------|
| **Logistic Regression** | Rapide, interprétable | Linéaire | ⭐⭐⭐ |
| **Decision Tree** | Gère non-linéarité | Moyenne | ⭐⭐⭐ |
| **Random Forest** | Robuste, précis | Élevée | ⭐⭐ |
| **SVM** | Bonne généralisation | Élevée | ⭐ |
| **K-NN** | Simple, adaptatif | Variable | ⭐⭐ |
| **Naive Bayes** | Ultra-rapide | Faible | ⭐⭐ |

### Résultats principaux (TP3)

#### Comparaison des modèles

```
Performances sur l'ensemble de test (F1-Score) :
┌─────────────────────┬──────────┬────────────┬────────┬──────────┐
│ Modèle             │ Accuracy │ Precision  │ Recall │ F1-Score │
├─────────────────────┼──────────┼────────────┼────────┼──────────┤
│ Random Forest      │   0.852  │    0.833   │  0.833 │   0.850  │
│ Logistic Regression│   0.852  │    0.833   │  0.833 │   0.833  │
│ SVM               │   0.836  │    0.818   │  0.818 │   0.818  │
│ Naive Bayes       │   0.836  │    0.818   │  0.818 │   0.818  │
│ K-NN              │   0.803  │    0.786   │  0.786 │   0.786  │
│ Decision Tree     │   0.770  │    0.750   │  0.750 │   0.750  │
└─────────────────────┴──────────┴────────────┴────────┴──────────┘
```

#### Meilleur modèle : Random Forest

- **F1-Score optimisé** : 0.850 (après GridSearchCV)
- **ROC-AUC** : 0.92
- **Matrice de confusion** : 26 TN, 27 TP, 4 FP, 4 FN

#### Variables les plus importantes

```
Top 5 features prédictives :
1. thalach    : 0.142 (fréquence cardiaque maximale)
2. cp         : 0.138 (type de douleur thoracique)
3. thal       : 0.125 (test thalium)
4. age        : 0.098 (âge)
5. oldpeak    : 0.092 (dépression ST)
```

---

## 🚀 Installation et utilisation

### Prérequis

- Python 3.8+
- pip ou conda

### Installation

1. **Cloner le dépôt**

```bash
git clone https://github.com/Haytame37/IA-Indus-4.0.git
cd IA-Indus-4.0/TP
```

2. **Créer un environnement virtuel**

```bash
python -m venv venv

# Activation
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

3. **Installer les dépendances**

```bash
pip install -r requirements.txt
```

### Exécution

#### Option 1 : Script Python directement

```bash
# Depuis le répertoire TP/
python src/tp1_analysis.py
```

#### Option 2 : Jupyter Notebook (interactif)

```bash
jupyter notebook notebooks/TP1_exploration.ipynb
```

#### Option 3 : Python interactif

```bash
python
>>> from src.tp1_analysis import *
>>> df = load_and_prepare_data("data/Base_Maladie_Cardiaque.csv")
>>> analyze_quantitative_variable(df['age'], 'age')
>>> plot_quantitative_variable(df['age'], 'age')
```

#### TP3 - Classification ML

```bash
# Script Python
python src/tp3_classification.py

# Notebook interactif
jupyter notebook notebooks/TP3_classification.ipynb

# Python interactif
python
>>> from src.tp3_classification import *
>>> results = compare_models()
>>> best_model = optimize_hyperparameters('Random Forest')
>>> plot_feature_importance(best_model)
```

---

## 📁 Structure du projet

```
TP/
├── README.md                          # Ce fichier
├── requirements.txt                   # Dépendances Python
├── .gitignore                         # Fichiers à ignorer
│
├── TP1/
│   ├── Base_Maladie_Cardiaque.csv    # (A DÉPLACER dans /data)
│   ├── TP1.py                        # (DÉPRÉCIÉ - utiliser src/)
│   ├── TP1_.py                       # (DÉPRÉCIÉ - utiliser src/)
│   └── TP1_JSON.ipynb                # (DÉPRÉCIÉ - voir /notebooks)
│
├── TP2/
│   └── Manuel_TPs_2.pdf              # Manuel pour TP2
│
├── data/
│   └── Base_Maladie_Cardiaque.csv    # Dataset normalisé
│
├── src/
│   ├── tp1_analysis.py                # 🆕 Analyse TP1 (refactorisée)
│   ├── tp2_analysis.py                # 🆕 Analyse TP2 (bivariée)
│   ├── tp3_classification.py          # 🆕 Classification ML TP3
│   └── utils.py                       # 🟢 Fonctions utilitaires partagées
│
├── notebooks/
│   ├── TP1_exploration.ipynb         # 🆕 Notebook Jupyter TP1
│   ├── TP2_exploration.ipynb         # 🆕 Notebook Jupyter TP2
│   └── TP3_classification.ipynb      # 🆕 Notebook Jupyter TP3
│
└── docs/
   ├── TP1_rapport.md                # 🆕 Rapport détaillé TP1
   ├── TP2_rapport.md                # 🆕 Rapport détaillé TP2
   └── TP3_rapport.md                # 🆕 Rapport détaillé TP3
```

---

## 📚 Concepts clés couverts

### Statistiques Descriptives

| Concept        | Formule                                            | Interprétation                  |
| -------------- | -------------------------------------------------- | ------------------------------- |
| **Moyenne**    | $\bar{x} = \frac{1}{n}\sum x_i$                    | Centre de masse                 |
| **Médiane**    | Valeur centrale                                    | Résistante aux outliers         |
| **Écart-type** | $\sigma = \sqrt{\frac{1}{n}\sum(x_i - \bar{x})^2}$ | Dispersion autour de la moyenne |
| **IQR**        | $Q_3 - Q_1$                                        | Étendue des 50% centraux        |
| **Asymétrie**  | $\frac{E[(X-\mu)^3]}{\sigma^3}$                    | Forme de distribution           |

### Visualisations

- **Histogramme** : Distribution des fréquences (choix des bins important)
- **Boxplot** : Quartiles + détection des outliers
- **KDE** : Courbe de densité lissée
- **QQ-Plot** : Test de normalité
- **Diagramme en barres** : Variables qualitatives
- **Pie chart** : Proportions (max 3 catégories)

### Détection des Outliers

Méthode IQR :

```
Borne basse = Q1 - 1.5 × IQR
Borne haute = Q3 + 1.5 × IQR
Outlier si valeur < borne basse OU valeur > borne haute
```

---

## 🔧 Technologies utilisées

| Outil          | Version | Usage                               |
| -------------- | ------- | ----------------------------------- |
| **Python**     | 3.8+    | Langage principal                   |
| **pandas**     | ≥1.3.0  | Manipulation de DataFrames          |
| **numpy**      | ≥1.20.0 | Calculs numériques                  |
| **matplotlib** | ≥3.3.0  | Visualisations                      |
| **seaborn**    | ≥0.11.0 | Graphiques statistiques             |
| **scipy**      | ≥1.6.0  | Tests et distributions statistiques |
| **scikit-learn**| ≥1.0.0  | Machine Learning (classification)   |
| **jupyter**    | ≥1.0.0  | Notebooks interactifs               |

---

## 📝 Exemple d'utilisation

### Analyse simple en Python

```python
import pandas as pd
from src.tp1_analysis import load_and_prepare_data, analyze_quantitative_variable

# Charger les données
df = load_and_prepare_data("data/Base_Maladie_Cardiaque.csv")

# Analyser l'âge
stats = analyze_quantitative_variable(df['age'], 'age')

# Afficher la moyenne et l'écart-type
print(f"Moyenne : {stats['Moyenne']:.1f} ans")
print(f"Écart-type : {stats['Écart-type']:.1f} ans")
```

### Notebook Jupyter

Lancez `TP1_exploration.ipynb` pour un environnement interactif avec explications détaillées.

### Classification ML (TP3)

```python
from src.tp3_classification import load_and_preprocess_data, compare_models

# Charger et préparer les données
X_train, X_test, y_train, y_test = load_and_preprocess_data()

# Comparer tous les modèles
results_df = compare_models()
print(results_df)

# Le Random Forest obtient généralement le meilleur F1-Score (~0.85)
```

---

## ✨ Bonnes pratiques appliquées

✅ **Code professionnel** :

- Docstrings claires pour chaque fonction
- Types annotations
- Noms de variables explicites

✅ **Reproductibilité** :

- Chemin de données centralisé
- Seed aléatoire fixé
- Versions de dépendances spécifiées

✅ **Documentation** :

- README détaillé
- Commentaires en français
- Exemples d'utilisation

✅ **Git workflow** :

- .gitignore approprié
- Commits clairs et atomiques
- Branches pour chaque TP (optionnel)

---

## 🎓 Questions pédagogiques (TP1)

1. **Pourquoi la moyenne et la médiane sont-elles différentes ?**
   → Distribution asymétrique (skewness ≠ 0)

2. **Quelle visualisation choisir pour comparer plusieurs variables quantitatives ?**
   → Boxplots côte à côte (meilleure comparaison que pie charts)

3. **Comment détecter automatiquement les outliers ?**
   → Méthode IQR ou distance de Mahalanobis

4. **Le dataset est déséquilibré (68% hommes). Est-ce un problème ?**
   → Oui pour la classification ; non pour l'analyse descriptive

---

## 🎓 Questions pédagogiques (TP3)

1. **Pourquoi Random Forest surpasse-t-il souvent les autres modèles ?**
   → Réduction de la variance par aggrégation d'arbres indépendants

2. **Quelle métrique privilégier pour un diagnostic médical ?**
   → F1-Score (balance précision/rappel) plutôt qu'accuracy seule

3. **Pourquoi standardiser les variables avant SVM ?**
   → SVM sensible aux échelles ; features doivent être comparables

4. **L'optimisation des hyperparamètres améliore-t-elle toujours les performances ?**
   → Non, risque de sur-apprentissage ; validation croisée nécessaire

5. **Pourquoi la fréquence cardiaque (`thalach`) est-elle si importante ?**
   → Indicateur direct de la capacité cardiovasculaire

---

## 🐛 Dépannage

### `FileNotFoundError: Base_Maladie_Cardiaque.csv`

**Solution** : Assurez-vous que le fichier CSV est dans `data/`

### `ModuleNotFoundError: No module named 'seaborn'`

**Solution** : Réinstallez les dépendances :

```bash
pip install -r requirements.txt
```

### Plots ne s'affichent pas dans Jupyter

**Solution** : Ajoutez en début de notebook :

```python
%matplotlib inline
```

---

## 📖 Références

- [UCI Machine Learning Repository - Heart Disease](https://archive.ics.uci.edu/ml/datasets/heart+disease)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Seaborn Tutorial](https://seaborn.pydata.org/tutorial.html)
- [SciPy Stats](https://docs.scipy.org/doc/scipy/reference/stats.html)
- [Scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html)
- [Machine Learning with Python](https://scikit-learn.org/stable/tutorial/basic/tutorial.html)

---

## 📧 Support

Pour toute question ou problème :

- Consultez la documentation dans `docs/`
- Ouvrez une issue sur GitHub
- Contactez l'instructeur

---

## 📄 Licence

Ce projet est sous licence [MIT](LICENSE).

---

## ✍️ Auteurs

- **Étudiants** : Classe IA-Industrie 4.0, ENSAM Béni Mellal
- **Instructeur** : [À compléter]
- **Date** : Mai 2026

---

**Dernière mise à jour** : 5 mai 2026

_Bon travail et bonne analyse des données ! 📊_
