"""
TP2 - Analyse Bivariée des Données (Heart Disease Dataset)

Module : tp2_analysis.py
Description : Analyse bivariée professionnelle, tests d'association,
             corrélations et régressions simples.

Auteur : Étudiants IA-Industrie 4.0
Date : 2026
Version : 1.0
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from pathlib import Path

from .tp1_analysis import load_and_prepare_data

# Configuration graphique
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['font.size'] = 10
sns.set_style('whitegrid')

DATA_DIR = Path(__file__).parent.parent / 'data'
CSV_FILE = DATA_DIR / 'Base_Maladie_Cardiaque.csv'


def load_data(filepath=None):
    """Charge le dataset et prépare les variables catégorielles."""
    if filepath is None:
        filepath = CSV_FILE
    return load_and_prepare_data(filepath)


def numeric_columns(df):
    """Retourne la liste des variables quantitatives."""
    return df.select_dtypes(include=['number']).columns.tolist()


def categorical_columns(df):
    """Retourne la liste des variables qualitatives."""
    return df.select_dtypes(include=['category', 'object']).columns.tolist()


def compute_correlation_matrix(df, variables=None, method='pearson'):
    """Calcule la matrice de corrélation pour les variables quantitatives."""
    if variables is None:
        variables = numeric_columns(df)
    corr = df[variables].corr(method=method)
    print(f"\n=== Matrice de corrélation ({method}) ===")
    print(corr.round(3))
    return corr


def plot_correlation_heatmap(df, variables=None, method='pearson', save_path=None):
    """Affiche une heatmap de corrélation pour les variables quantitatives."""
    if variables is None:
        variables = numeric_columns(df)
    corr = df[variables].corr(method=method)

    plt.figure(figsize=(12, 10))
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='vlag', center=0,
                linewidths=0.5, square=True)
    plt.title(f'Matrice de corrélation ({method})')
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Heatmap enregistrée : {save_path}")
    plt.show()
    return corr


def scatter_with_regression(df, x, y, hue=None, save_path=None):
    """Affiche un nuage de points et une droite de régression simple."""
    plt.figure(figsize=(10, 6))
    ax = sns.scatterplot(data=df, x=x, y=y, hue=hue, palette='Set2', edgecolor='w', alpha=0.75)

    valid = df[[x, y]].dropna()
    slope, intercept = np.polyfit(valid[x], valid[y], 1)
    line = slope * valid[x] + intercept

    plt.plot(valid[x], line, color='red', linewidth=2,
             label=f'y = {slope:.2f}x + {intercept:.1f}')
    plt.title(f'{y} en fonction de {x} — Régression linéaire simple')
    plt.xlabel(x)
    plt.ylabel(y)
    plt.legend()
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Nuage de points enregistré : {save_path}")
    plt.show()

    r, p = stats.pearsonr(valid[x], valid[y])
    print(f"Coefficient de corrélation de Pearson (r) = {r:.3f}, p = {p:.3g}")
    return {'slope': slope, 'intercept': intercept, 'r': r, 'p_value': p}


def point_biserial_correlations(df, numeric_cols=None, binary_cols=None):
    """Calcule la corrélation point-bisérielle pour variables numériques vs binaires."""
    if numeric_cols is None:
        numeric_cols = numeric_columns(df)
    if binary_cols is None:
        binary_cols = [c for c in categorical_columns(df)
                       if df[c].nunique() == 2]
    results = []
    for num in numeric_cols:
        for cat in binary_cols:
            try:
                stat, p = stats.pointbiserialr(df[cat].cat.codes, df[num])
                results.append({'numeric': num, 'binary': cat, 'r_pb': stat, 'p_value': p})
            except Exception:
                continue
    return pd.DataFrame(results)


def compare_numeric_by_category(df, numeric_col, category_col, save_path=None):
    """Affiche la distribution numérique selon les catégories."""
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=category_col, y=numeric_col, data=df, palette='Set2')
    sns.stripplot(x=category_col, y=numeric_col, data=df, color='black', alpha=0.3, jitter=0.2)
    plt.title(f'{numeric_col} par catégorie de {category_col}')
    plt.xlabel(category_col)
    plt.ylabel(numeric_col)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Boxplot catégoriel enregistré : {save_path}")
    plt.show()

    groups = [group.dropna() for _, group in df.groupby(category_col)[numeric_col]]
    if len(groups) >= 2:
        stat, p = stats.f_oneway(*groups)
        print(f"ANOVA one-way pour {numeric_col} ~ {category_col} : F = {stat:.3f}, p = {p:.3g}")
        return {'F': stat, 'p_value': p}
    return None


def contingency_analysis(df, col1, col2):
    """Affiche la table de contingence et le test du chi2."""
    table = pd.crosstab(df[col1], df[col2])
    chi2, p, dof, expected = stats.chi2_contingency(table)
    print(f"\n=== Table de contingence : {col1} vs {col2} ===")
    print(table)
    print(f"\nChi2 = {chi2:.2f}, dof = {dof}, p = {p:.3g}")
    return {'table': table, 'chi2': chi2, 'p_value': p, 'dof': dof, 'expected': expected}


def plot_contingency_heatmap(df, col1, col2, save_path=None):
    """Affiche la table de contingence sous forme de heatmap."""
    table = pd.crosstab(df[col1], df[col2])
    plt.figure(figsize=(8, 6))
    sns.heatmap(table, annot=True, fmt='d', cmap='Blues')
    plt.title(f'Table de contingence : {col1} vs {col2}')
    plt.xlabel(col2)
    plt.ylabel(col1)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Heatmap de contingence enregistrée : {save_path}")
    plt.show()
    return table


def analyze_pairs(df, numeric_pairs=None, categorical_pairs=None):
    """Exécute un ensemble d'analyse bivariée prédéfinies."""
    print('\n' + '=' * 70)
    print('PARTIE TP2 — Analyse Bivariée'.center(70))
    print('=' * 70)

    if numeric_pairs is None:
        numeric_pairs = [('age', 'chol'), ('age', 'thalach'), ('chol', 'thalach')]
    if categorical_pairs is None:
        categorical_pairs = [('sex', 'target'), ('cp', 'target'), ('thal', 'target')]

    results = {'correlations': {}, 'regressions': {}, 'contingencies': {}}

    print('\n>>> Corrélations numériques')
    corr = compute_correlation_matrix(df)
    plot_correlation_heatmap(df)
    results['correlations']['pearson'] = corr

    print('\n>>> Nuages de points et régressions simples')
    for x, y in numeric_pairs:
        results['regressions'][f'{x}_{y}'] = scatter_with_regression(df, x, y)

    print('\n>>> Relations numériques / catégorielles')
    for num in ['age', 'chol', 'thalach']:
        results[f'box_{num}_target'] = compare_numeric_by_category(df, num, 'target')
        results[f'box_{num}_sex'] = compare_numeric_by_category(df, num, 'sex')

    print('\n>>> Tables de contingence et associations catégorielles')
    for col1, col2 in categorical_pairs:
        results['contingencies'][f'{col1}_{col2}'] = contingency_analysis(df, col1, col2)
        plot_contingency_heatmap(df, col1, col2)

    print('\n>>> Corrélations point-bisérielles')
    pb = point_biserial_correlations(df)
    print(pb.round(3).to_string(index=False))
    results['point_biserial'] = pb

    return results


def main():
    """Exécute l'analyse TP2 complète."""
    df = load_data()
    analyze_pairs(df)
    print('\n' + '=' * 70)
    print('TP2 - Analyse bivariée terminée')
    print('=' * 70)


if __name__ == '__main__':
    main()
