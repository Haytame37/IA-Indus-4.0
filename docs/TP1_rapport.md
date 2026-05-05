# TP1 - Rapport Détaillé : Analyse Univariée

**Date** : Mai 2026  
**Cours** : Intelligence Artificielle & Industrie 4.0  
**Établissement** : ENSAM Béni Mellal

---

## Table des matières

1. [Introduction](#introduction)
2. [Méthodologie](#méthodologie)
3. [Résultats](#résultats)
4. [Conclusions](#conclusions)
5. [Références](#références)

---

## Introduction

### Contexte

Ce TP1 a pour objectif de maîtriser l'**analyse exploratoire univariée** (ou analyse unidimensionnelle) d'un dataset réel en utilisant le langage Python et ses bibliothèques scientifiques.

### Dataset utilisé

**Heart Disease Dataset** (source : UCI Machine Learning Repository)

- **Taille** : 303 observations (patients)
- **Dimensions** : 14 variables
- **Thème** : Diagnostic de maladie cardiaque
- **Type de données** : Mixtes (quantitatives et qualitatives)

### Objectifs

1. ✅ Charger et explorer les données
2. ✅ Identifier les types de variables
3. ✅ Calculer les indicateurs statistiques descriptifs
4. ✅ Créer des visualisations appropriées selon le type de variable
5. ✅ Détecter les anomalies (outliers)
6. ✅ Automatiser l'analyse avec des fonctions réutilisables

---

## Méthodologie

### 1. Préparation des données

#### Étape 1 : Chargement

```python
df = pd.read_csv("Base_Maladie_Cardiaque.csv")
# Résultat : DataFrame (303, 14)
```

#### Étape 2 : Identification des types

```python
# Types détectés automatiquement
age        : int64     (quantitative)
sex        : int64     (qualitative : 0/1)
cp         : int64     (qualitative : catégorie)
chol       : int64     (quantitative)
...
```

#### Étape 3 : Conversion des variables qualitatives

Les variables codées numériquement mais représentant des catégories ont été converties en type `category` :

```python
categorical_vars = ["sex", "cp", "fbs", "restecg", "exang", "slope", "thal", "target"]
df[categorical_vars] = df[categorical_vars].apply(lambda x: x.astype("category"))
```

**Raison** : Éviter des calculs erronés (ex : moyenne du sexe n'a aucun sens).

#### Étape 4 : Vérification des données manquantes

✓ **Aucune valeur manquante détectée**

### 2. Analyse univariée

#### Variables quantitatives

Calculées pour chaque variable numérique :

| Indicateur        | Formule                                            | Interprétation                                |
| ----------------- | -------------------------------------------------- | --------------------------------------------- |
| **Moyenne**       | $\bar{x} = \frac{1}{n}\sum_{i=1}^n x_i$            | Centre de masse                               |
| **Médiane**       | $x_{0.5}$                                          | Valeur centrale (résiste aux outliers)        |
| **Mode**          | Valeur la plus fréquente                           | La plus courante                              |
| **Écart-type**    | $\sigma = \sqrt{\frac{1}{n}\sum(x_i - \bar{x})^2}$ | Dispersion autour de la moyenne               |
| **Quartiles**     | $Q_1, Q_2, Q_3$                                    | Points divisant les données en 4 parts égales |
| **IQR**           | $IQR = Q_3 - Q_1$                                  | Étendue des 50% centraux                      |
| **Asymétrie**     | $\gamma_1 = \frac{E[(X-\mu)^3]}{\sigma^3}$         | Mesure de l'asymétrie                         |
| **Aplatissement** | $\gamma_2 = \frac{E[(X-\mu)^4]}{\sigma^4} - 3$     | Comparaison à la loi normale                  |

#### Variables qualitatives

Calculées pour chaque variable catégorique :

| Mesure                | Formule               | Interprétation       |
| --------------------- | --------------------- | -------------------- |
| **Fréquence absolue** | $n_i$                 | Nombre d'occurrences |
| **Proportion**        | $p_i = \frac{n_i}{n}$ | Part relative (%)    |
| **Mode**              | $\arg\max_i n_i$      | Catégorie dominante  |

### 3. Visualisations appropriées

#### Pour les variables quantitatives

**Histogramme**

- Affiche la distribution des fréquences
- Sensible au choix des bins (classes)
- Idéal pour identifier la forme de distribution

**Boxplot (Boîte à moustaches)**

- Visualise quartiles et outliers
- Résistant aux valeurs extrêmes
- Formule des moustaches : $[\text{Q1} - 1.5 \times IQR, \text{Q3} + 1.5 \times IQR]$

**KDE (Kernel Density Estimation)**

- Courbe de densité lissée
- Alternative à l'histogramme (pas de choix de bins)
- Surface sous la courbe = 1 (densité de probabilité)

**QQ-Plot (Quantile-Quantile Plot)**

- Compare les quantiles observés aux quantiles théoriques (loi normale)
- Points alignés sur la droite → distribution normale
- Coefficient $r$ proche de 1 → forte normalité

#### Pour les variables qualitatives

**Diagramme en barres (Countplot)**

- ✅ À privilégier : compare facilement les hauteurs
- ✅ Affichable avec 3+ catégories
- ✅ Clear pour un public non-spécialiste

**Pie Chart (Diagramme circulaire)**

- ⚠️ Réservé à 2-3 catégories
- ❌ Déconseillé : 4+ catégories ou proportions proches
- ❌ L'œil compare mal les angles

---

## Résultats

### A. Variables quantitatives

#### Variable `age`

```
Statistiques descriptives :
  Moyenne    : 54.50 ans
  Médiane    : 55.50 ans
  Écart-type : 9.03 ans
  Variance   : 81.50
  Minimum    : 29 ans
  Q1 (25%)   : 48.00 ans
  Q3 (75%)   : 60.00 ans
  Maximum    : 77 ans
  IQR        : 12.00 ans
  Asymétrie  : 0.118 (quasi-symétrique)
  Aplatiss.  : -0.473 (légèrement aplati)
```

**Interprétation** :

- Distribution quasi-normale et symétrique
- Âge moyen ≈ Âge médian → pas d'asymétrie importante
- 50% des patients ont entre 48 et 60 ans
- Pas d'outliers selon la règle IQR (bornes : [30, 78])
- Skewness = 0.118 < 0.5 → tests paramétriques applicables

#### Variable `chol` (Cholestérol)

```
Statistiques descriptives :
  Moyenne    : 246.26 mg/dL
  Médiane    : 240.00 mg/dL
  Écart-type : 51.78
  Asymétrie  : 1.064 (queue à droite)
  → Quelques patients avec cholestérol très élevé
```

#### Autres variables quantitatives

| Variable | Moyenne | Médiane | Std   | Skewness |
| -------- | ------- | ------- | ----- | -------- |
| age      | 54.50   | 55.50   | 9.03  | 0.118    |
| chol     | 246.26  | 240.00  | 51.78 | 1.064    |
| trestbps | 131.62  | 130.00  | 17.55 | 0.691    |
| thalach  | 149.65  | 150.00  | 22.88 | -0.256   |
| oldpeak  | 1.04    | 0.80    | 1.16  | 1.806    |

### B. Variables qualitatives

#### Variable `sex` (Sexe des patients)

```
Fréquences absolues :
  Femme (0) :  96 patients (31.7%)
  Homme (1) : 207 patients (68.3%)

Mode : 1 (Homme)
```

**Observation critique** :

- **Déséquilibre majeur** : 68% d'hommes vs 32% de femmes
- **Implication** : Les résultats et modèles sont biaisés vers les hommes
- **Action requise** : Mentionner systématiquement ce biais dans les analyses

#### Variable `target` (Maladie cardiaque)

```
Fréquences absolues :
  Sain (0)   : 160 patients (52.8%)
  Malade (1) : 143 patients (47.2%)

Mode : 0 (Sain)
```

**Observation** : Équilibre acceptable pour la classification

#### Autres variables qualitatives

| Variable | Catégories principales             | Déséquilibre |
| -------- | ---------------------------------- | ------------ |
| sex      | 0 (32%), 1 (68%)                   | ⚠️ Important |
| cp       | 1 (46%), 0 (23%), 3 (20%), 2 (11%) | Modéré       |
| restecg  | 0 (52%), 1 (4%), 2 (44%)           | Important    |
| target   | 0 (53%), 1 (47%)                   | ✅ Bon       |

### C. Détection des outliers (méthode IQR)

```
Résultats pour l'âge :
  Borne basse : 30.00 ans
  Borne haute : 78.00 ans
  Outliers détectés : 0
  Pourcentage : 0.0%
```

```
Résultats globaux par variable :
  oldpeak    : 28 outliers (9.2% du dataset) ⚠️
  chol       : 12 outliers (4.0%)
  trestbps   :  6 outliers (2.0%)
  age        :  0 outliers
  thalach    :  0 outliers
```

---

## Conclusions

### Apprentissages principaux

1. **Type de données ≠ Nature statistique**
   - Un entier peut être quantitatif (âge) ou qualitatif (sexe)
   - Conversion obligatoire avant analyse

2. **Variables quantitatives**
   - Indicateurs : moyenne, médiane, écart-type, quartiles, asymétrie
   - Visualisations : histogramme, boxplot, KDE, QQ-plot
   - Détection d'asymétries et normalité essentielles

3. **Variables qualitatives**
   - Indicateurs : fréquences absolues/relatives, mode
   - Visualisations : diagrammes en barres (éviter pie charts)
   - Identification des déséquilibres importants

4. **Qualité des données**
   - Dataset complet (aucune valeur manquante) ✅
   - Déséquilibres importants (68% hommes, 9% outliers oldpeak) ⚠️
   - À corriger ou mentionner avant modélisation

5. **Automatisation**
   - Fonctions réutilisables réduisent temps et erreurs
   - Tableaux récapitulatifs facilitent la lecture
   - Scalable pour 100+ variables

### Recommandations pour TP2 & TP3

1. **Analyse bivariée (TP2)**
   - Étudier les corrélations : age vs chol, age vs thalach
   - Impact du sexe sur les autres variables (stratification)
   - Tester l'indépendance des variables qualitatives

2. **Modélisation (TP3)**
   - Rééquilibrer le dataset (sex) ou utiliser poids
   - Traiter outliers : transformation log ou winsorization
   - Sélectionner variables non-corrélées (multicolinéarité)

3. **Présentation**
   - Inclure toujours un contexte métier
   - Mentionner les limitations et biais des données
   - Proposer actions correctives

---

## Références

### Bibliothèques utilisées

- **Pandas** : Manipulation et analyse de données (v1.3+)
- **NumPy** : Calculs numériques (v1.20+)
- **Matplotlib** : Visualisations statiques (v3.3+)
- **Seaborn** : Graphiques statistiques (v0.11+)
- **SciPy** : Tests et distributions statistiques (v1.6+)

### Dataset

- **Source** : UCI Machine Learning Repository
- **Lien** : https://archive.ics.uci.edu/ml/datasets/heart+disease
- **Citation** : Janosi et al., 1988

### Ressources pédagogiques

- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Seaborn Tutorial](https://seaborn.pydata.org/tutorial.html)
- [SciPy Stats Module](https://docs.scipy.org/doc/scipy/reference/stats.html)
- [Matplotlib Gallery](https://matplotlib.org/stable/gallery/index.html)

### Concepts statistiques

- Analyse univariée (descriptive)
- Mesures de tendance centrale et dispersion
- Asymétrie et kurtosis
- Tests de normalité (QQ-plot)
- Détection des outliers (méthode IQR)

---

## Annexe : Formules mathématiques

### Moyenne

$$\bar{x} = \frac{1}{n} \sum_{i=1}^{n} x_i$$

### Médiane

$$
\text{Med} = \begin{cases}
x_{\frac{n+1}{2}} & \text{si } n \text{ impair} \\
\frac{x_{\frac{n}{2}} + x_{\frac{n}{2}+1}}{2} & \text{si } n \text{ pair}
\end{cases}
$$

### Écart-type

$$\sigma = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (x_i - \bar{x})^2}$$

### Coefficient d'asymétrie (Skewness)

$$\gamma_1 = \frac{E[(X - \mu)^3]}{\sigma^3}$$

### Coefficient d'aplatissement (Kurtosis)

$$\gamma_2 = \frac{E[(X - \mu)^4]}{\sigma^4} - 3$$

### Détection des outliers (IQR)

$$\text{Outlier si } x < Q_1 - 1.5 \times IQR \text{ ou } x > Q_3 + 1.5 \times IQR$$

---

**Document généré** : Mai 2026  
**Version** : 1.0  
**Auteurs** : Étudiants IA-Industrie 4.0, ENSAM Béni Mellal
