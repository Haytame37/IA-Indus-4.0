# TP2 - Rapport Détaillé : Analyse Bivariée

**Date** : Mai 2026  
**Cours** : Intelligence Artificielle & Industrie 4.0  
**Établissement** : ENSAM Béni Mellal

---

## Table des matières

1. [Introduction](#introduction)
2. [Méthodologie](#méthodologie)
3. [Résultats](#résultats)
4. [Interprétations](#interprétations)
5. [Conclusions](#conclusions)
6. [Références](#références)

---

## Introduction

Ce TP2 poursuit l'étude du Heart Disease Dataset en s'intéressant aux relations *bivariées* entre variables. L'objectif est de comprendre comment deux variables évoluent ensemble, d'identifier des associations significatives et de préparer une base solide pour TP3.

### Objectifs

- Étudier les corrélations entre variables quantitatives
- Tester des régressions simples sur des relations clés
- Mesurer l'association entre variables qualitatives
- Analyser l'effet des variables catégorielles sur les variables numériques
- Produire une documentation claire et professionnelle

---

## Méthodologie

### 1. Chargement et préparation des données

Le dataset est chargé depuis `data/Base_Maladie_Cardiaque.csv`. Les colonnes catégorielles ont été converties en type `category` afin de garantir une interprétation correcte.

### 2. Corrélation entre variables quantitatives

Les relations numériques sont analysées à l'aide de :

- Matrice de corrélation de Pearson
- Heatmap de corrélation
- Nuages de points avec droite de régression linéaire simple

### 3. Régressions simples

La régression linéaire simple est appliquée aux couples :

- `age` vs `chol`
- `age` vs `thalach`
- `chol` vs `thalach`

La pente, l'ordonnée à l'origine et le coefficient de corrélation de Pearson sont calculés.

### 4. Variable quantitative vs variable qualitative

Pour les variables quantitatives clés (`age`, `chol`, `thalach`), nous comparons la distribution selon :

- `target` (0 = sain, 1 = malade)
- `sex` (0 = femme, 1 = homme)

Nous utilisons :

- Boxplots comparatifs
- Tests ANOVA one-way

### 5. Variables qualitatives associées

Les associations catégorielles sont évaluées avec :

- Tables de contingence
- Test du chi2
- Heatmaps de contingence

---

## Résultats

### A. Corrélations numériques

#### Matrice de corrélation (Pearson)

La matrice de corrélation met en évidence plusieurs relations importantes :

- `age` / `chol` : corrélation positive modérée
- `age` / `thalach` : corrélation négative
- `chol` / `thalach` : corrélation négative légère

La heatmap complète visualise ces relations de manière claire.

### B. Régressions simples

#### `age` vs `chol`
- Le coefficient de régression indique qu'une augmentation de l'âge est associée à une légère hausse du cholestérol.
- Le coefficient de corrélation de Pearson renseigne la qualité de la relation.

#### `age` vs `thalach`
- Relation négative : plus l'âge augmente, plus la fréquence cardiaque maximale tend à diminuer.

#### `chol` vs `thalach`
- Relation négative : les patients ayant un cholestérol élevé tendent à atteindre une fréquence cardiaque maximale plus faible.

### C. Analyse numérique par catégorie

#### Tableau de bord pour `target`

Les distributions de `age`, `chol`, et `thalach` sont comparées entre patients sains et malades.

- `age` : tendance à être plus élevé chez les patients malades
- `chol` : tendance à être plus élevé chez les patients malades
- `thalach` : tendance à être plus faible chez les patients malades

Les tests ANOVA permettent de valider si ces différences sont significatives.

#### Tableau de bord pour `sex`

La comparaison par sexe montre :

- Des différences de `thalach` et `chol` selon le sexe
- Un déséquilibre hommes/femmes qui doit être pris en compte

### D. Associations catégorielles

Les tables de contingence ont été calculées pour :

- `sex` vs `target`
- `cp` vs `target`

Le test du chi2 indique si l'association est significative.

---

## Interprétations

### Corrélations utiles

- `age` et `chol` sont liées, ce qui confirme l'importance de prendre en compte l'âge dans l'analyse du cholestérol.
- `age` et `thalach` montrent une relation inverse, cohérente avec la physiologie cardiaque.

### Impact des catégories sur la cible

- L'association entre `cp` et `target` est particulièrement intéressante : le type de douleur thoracique permet de distinguer les patients sains des patients malades.
- L'association entre `sex` et `target` doit être étudiée avec prudence car le dataset est déséquilibré.

### Questions pour TP3

- Les variables numériques les plus corrélées avec `target` sont de bons candidats pour la modélisation.
- Les variables qualitatives fortement associées à `target` devraient être codées et évaluées dans les modèles.

---

## Conclusions

### Bilan

TP2 a permis de structurer l'étude bivariée avec :

- Une analyse de corrélation complète
- Des régressions simples interprétables
- Une approche statistique robuste pour les variables catégorielles
- Une préparation solide pour TP3

### Recommandations

- Conserver `age`, `chol` et `thalach` dans les explorations de modèles
- Tester `cp`, `sex` et `target` dans des modèles de classification
- Corriger le déséquilibre de sexe avant une modélisation finale

---

## Références

- `scipy.stats.pearsonr` pour les corrélations de Pearson
- `scipy.stats.f_oneway` pour l'ANOVA
- `scipy.stats.chi2_contingency` pour l'association catégorielle

---

**Document généré** : Mai 2026  
**Version** : 1.0  
**Auteurs** : Étudiants IA-Industrie 4.0, ENSAM Béni Mellal
