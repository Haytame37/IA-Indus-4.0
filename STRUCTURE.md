# 📁 Structure Professionnelle du Projet

## Vue d'ensemble

```
TP/                           # Racine du projet
├── README.md                  # Documentation générale
├── STRUCTURE.md              # Ce fichier
├── requirements.txt          # Dépendances Python
├── .gitignore               # Fichiers Git à ignorer
│
├── data/                     # 📊 Données brutes
│   └── Base_Maladie_Cardiaque.csv
│
├── src/                      # 🐍 Code source modulaire
│   ├── __init__.py
│   ├── tp1_analysis.py       # TP1: Analyse univariée
│   ├── tp2_analysis.py       # TP2: Analyse bivariée
│   ├── tp3_classification.py # TP3: Machine Learning
│   └── utils.py              # Utilitaires communs
│
├── notebooks/                # 📓 Notebooks Jupyter interactifs
│   ├── TP1_exploration.ipynb
│   ├── TP2_exploration.ipynb
│   └── TP3_classification.ipynb
│
├── docs/                     # 📄 Documentation & Rapports
│   ├── TP1_rapport.md        # Rapport TP1
│   ├── TP2_rapport.md        # Rapport TP2
│   ├── TP3_rapport.md        # Rapport TP3
│   └── manuals/              # Manuels de référence
│       ├── TP1_TP2_TP3_manual.pdf
│       └── TP2_manual.pdf
│
├── tests/                    # 🧪 Tests unitaires
│   ├── __init__.py
│   ├── test_tp1_analysis.py
│   ├── test_tp2_analysis.py
│   └── test_tp3_classification.py
│
├── venv/                     # 🔧 Environnement virtuel
│   └── [Python packages]
│
└── .git/                     # 🌳 Historique Git

```

## Convention de Nommage

### Fichiers Python
- `tp1_analysis.py` → Analyse univariée
- `tp2_analysis.py` → Analyse bivariée  
- `tp3_classification.py` → Classification ML
- `utils.py` → Utilitaires partagés

### Notebooks Jupyter
- `TP1_exploration.ipynb` → Exploration TP1
- `TP2_exploration.ipynb` → Exploration TP2
- `TP3_classification.ipynb` → Exploration TP3

### Rapports
- `TP1_rapport.md` → Résultats + interprétations TP1
- `TP2_rapport.md` → Résultats + interprétations TP2
- `TP3_rapport.md` → Résultats + interprétations TP3

## 🚀 Installation et Utilisation

### 1. Configuration initiale

```bash
# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

### 2. Exécuter les analyses

```bash
# TP1 - Analyse univariée
python src/tp1_analysis.py

# TP2 - Analyse bivariée
python src/tp2_analysis.py

# TP3 - Classification ML
python src/tp3_classification.py
```

### 3. Notebooks interactifs

```bash
# Lancer Jupyter
jupyter notebook

# Ouvrir les notebooks
notebooks/TP1_exploration.ipynb
notebooks/TP2_exploration.ipynb
notebooks/TP3_classification.ipynb
```

### 4. Exécuter les tests

```bash
# Tous les tests
pytest tests/

# Teste spécifiques
pytest tests/test_tp1_analysis.py
pytest tests/test_tp2_analysis.py
pytest tests/test_tp3_classification.py
```

## 📊 Contenu de chaque TP

### TP1 - Analyse Univariée
- **Fichiers:** `src/tp1_analysis.py`, `notebooks/TP1_exploration.ipynb`, `docs/TP1_rapport.md`
- **Analyses:** Statistiques descriptives, visualisations, détection d'outliers
- **Variables étudiées:** Age, sexe, type de douleur thoracique, cholestérol, etc.

### TP2 - Analyse Bivariée
- **Fichiers:** `src/tp2_analysis.py`, `notebooks/TP2_exploration.ipynb`, `docs/TP2_rapport.md`
- **Analyses:** Corrélations, régressions, tests d'association, ANOVA
- **Tests statistiques:** Pearson, Chi², Cramér's V, point-bisérielle

### TP3 - Machine Learning Classification
- **Fichiers:** `src/tp3_classification.py`, `notebooks/TP3_classification.ipynb`, `docs/TP3_rapport.md`
- **Modèles:** Logistic Regression, Decision Tree, Random Forest, SVM, K-NN, Naive Bayes
- **Optimisation:** GridSearchCV, validation croisée
- **Évaluation:** Accuracy, Precision, Recall, F1-Score, ROC-AUC

## 🔄 Workflow Git

```bash
# Voir l'état
git status

# Ajouter les changements
git add .

# Committer avec message clair
git commit -m "feat: Description de la modification"

# Pousser vers GitHub
git push origin main
```

### Convention de commits
- `feat:` Nouvelle fonctionnalité
- `fix:` Correction de bug
- `refactor:` Restructuration du code
- `docs:` Mise à jour de documentation
- `test:` Ajout/amélioration de tests

## 📝 Fichiers Importants

### `requirements.txt`
Liste des dépendances Python avec versions exactes pour reproductibilité.

### `README.md`
Documentation générale du projet avec objectifs et résultats clés.

### `STRUCTURE.md` (ce fichier)
Guide de la structure et de l'organisation du projet.

### `.gitignore`
Fichiers et dossiers à ignorer par Git (venv/, __pycache__/, etc.)

## 🎯 Objectifs du Projet

1. ✅ **TP1:** Exploration univariée du dataset Heart Disease
2. ✅ **TP2:** Analyse bivariée et tests d'association
3. ✅ **TP3:** Prédiction par classification ML

## 📧 Support et Questions

- Consultez les rapports dans `docs/`
- Explorez les notebooks pour des exemples interactifs
- Vérifiez les commentaires dans le code source
- Consultez les manuels dans `docs/manuals/`

---

**Dernière mise à jour:** 5 mai 2026  
**Version:** 2.0 (Structure professionnelle)  
**Auteurs:** Étudiants IA-Industrie 4.0, ENSAM Béni Mellal
