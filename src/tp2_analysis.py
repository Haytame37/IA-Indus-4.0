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
    plt.figure(figsize=(11, 7))
    ax = sns.scatterplot(data=df, x=x, y=y, hue=hue, palette='Set2', 
                         edgecolor='white', alpha=0.75, s=100)

    # Régression linéaire
    valid = df[[x, y]].dropna()
    slope, intercept = np.polyfit(valid[x], valid[y], 1)
    line = slope * valid[x] + intercept
    
    # Calcul du coefficient de détermination R²
    residuals = valid[y] - line
    ss_res = np.sum(residuals ** 2)
    ss_tot = np.sum((valid[y] - valid[y].mean()) ** 2)
    r2 = 1 - (ss_res / ss_tot)

    plt.plot(valid[x], line, color='red', linewidth=2.5, zorder=5,
             label=f'y = {slope:.2f}x + {intercept:.1f} (R² = {r2:.3f})')
    
    plt.title(f'{y} en fonction de {x} — Régression linéaire simple', fontsize=13, fontweight='bold')
    plt.xlabel(x, fontsize=11)
    plt.ylabel(y, fontsize=11)
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Nuage de points enregistré : {save_path}")
    plt.show()

    # Tests statistiques
    r, p = stats.pearsonr(valid[x], valid[y])
    print(f"\n  • Corrélation de Pearson (r) = {r:.4f}")
    print(f"  • Coefficient de détermination (R²) = {r2:.4f}")
    print(f"  • p-value = {p:.3g}")
    
    return {
        'slope': slope, 
        'intercept': intercept, 
        'r': r, 
        'r2': r2,
        'p_value': p, 
        'n': len(valid)
    }


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
    """Affiche la distribution numérique selon les catégories avec ANOVA."""
    plt.figure(figsize=(11, 7))
    sns.boxplot(x=category_col, y=numeric_col, data=df, palette='Set2', width=0.6)
    sns.stripplot(x=category_col, y=numeric_col, data=df, color='black', 
                  alpha=0.4, jitter=0.2, size=6)
    
    plt.title(f'{numeric_col} par catégorie de {category_col}', fontsize=13, fontweight='bold')
    plt.xlabel(category_col, fontsize=11)
    plt.ylabel(numeric_col, fontsize=11)
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Boxplot catégoriel enregistré : {save_path}")
    plt.show()

    # Tests statistiques
    groups = [group.dropna() for _, group in df.groupby(category_col)[numeric_col]]
    
    if len(groups) >= 2:
        # ANOVA one-way
        stat, p = stats.f_oneway(*groups)
        print(f"\n  • ANOVA one-way pour {numeric_col} ~ {category_col}")
        print(f"  • F = {stat:.4f}, p = {p:.3g}")
        
        # Statistiques descriptives par groupe
        print(f"\n  Moyennes par groupe:")
        for name, group in df.groupby(category_col)[numeric_col]:
            print(f"    {name}: μ = {group.mean():.2f}, σ = {group.std():.2f}, n = {len(group)}")
        
        return {'F': stat, 'p_value': p, 'groups': len(groups)}
    return None


def contingency_analysis(df, col1, col2):
    """Affiche la table de contingence, chi2 et proportions conditionnelles."""
    table = pd.crosstab(df[col1], df[col2])
    chi2, p, dof, expected = stats.chi2_contingency(table)
    
    print(f"\n  === Table de contingence : {col1} vs {col2} ===")
    print(table)
    print(f"\n  • Chi² = {chi2:.4f}")
    print(f"  • dof = {dof}")
    print(f"  • p-value = {p:.3g}")
    
    # Effet V de Cramér
    n = table.sum().sum()
    min_dim = min(table.shape) - 1
    cramers_v = np.sqrt(chi2 / (n * min_dim)) if min_dim > 0 else np.nan
    print(f"  • V de Cramér = {cramers_v:.4f}")
    
    # Résidus standardisés
    residuals = (table - expected) / np.sqrt(expected)
    print(f"\n  Résidus standardisés (>2 ou <-2 : significatif):")
    print(residuals.round(2).to_string())
    
    return {
        'table': table, 
        'chi2': chi2, 
        'p_value': p, 
        'dof': dof, 
        'expected': expected,
        'cramers_v': cramers_v,
        'residuals': residuals
    }


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
    """Exécute un ensemble complet d'analyses bivariées prédéfinies."""
    print('\n' + '=' * 75)
    print('PARTIE TP2 — Analyse Bivariée Complète'.center(75))
    print('=' * 75)

    if numeric_pairs is None:
        numeric_pairs = [('age', 'chol'), ('age', 'thalach'), ('chol', 'thalach')]
    if categorical_pairs is None:
        categorical_pairs = [('sex', 'target'), ('cp', 'target'), ('thal', 'target')]

    results = {
        'correlations': {}, 
        'regressions': {}, 
        'contingencies': {},
        'anova': {},
        'point_biserial': None
    }

    # 1. Corrélations numériques
    print('\n>>> 1. CORRÉLATIONS NUMÉRIQUES (PEARSON)')
    print('-' * 75)
    corr = compute_correlation_matrix(df)
    plot_correlation_heatmap(df)
    results['correlations']['pearson'] = corr

    # 2. Nuages de points et régressions simples
    print('\n>>> 2. RÉGRESSIONS LINÉAIRES SIMPLES')
    print('-' * 75)
    for x, y in numeric_pairs:
        print(f"\n  Régression : {y} ~ {x}")
        results['regressions'][f'{x}_{y}'] = scatter_with_regression(df, x, y)

    # 3. Comparaisons numériques / catégorielles avec ANOVA
    print('\n>>> 3. COMPARAISONS NUMÉRIQUES / CATÉGORIELLES (ANOVA)')
    print('-' * 75)
    for num in ['age', 'chol', 'thalach']:
        print(f"\n  Analyse de {num} par {num}_target")
        results['anova'][f'{num}_target'] = compare_numeric_by_category(df, num, 'target')
        print(f"\n  Analyse de {num} par {num}_sex")
        results['anova'][f'{num}_sex'] = compare_numeric_by_category(df, num, 'sex')

    # 4. Tables de contingence et associations catégorielles
    print('\n>>> 4. ASSOCIATIONS CATÉGORIELLES (CHI2 & CRAMÉR)')
    print('-' * 75)
    for col1, col2 in categorical_pairs:
        print(f"\n  Association : {col1} ↔ {col2}")
        results['contingencies'][f'{col1}_{col2}'] = contingency_analysis(df, col1, col2)
        plot_contingency_heatmap(df, col1, col2)

    # 5. Corrélations point-bisérielles
    print('\n>>> 5. CORRÉLATIONS POINT-BISÉRIELLE')
    print('-' * 75)
    pb = point_biserial_correlations(df)
    print("\nCorrélations entre variables numériques et binaires:")
    print(pb.round(4).to_string(index=False))
    results['point_biserial'] = pb

    print('\n' + '=' * 75)
    print('TP2 - Analyse bivariée terminée avec succès'.center(75))
    print('=' * 75)
    
    return results


def main():
    """Exécute l'analyse TP2 complète."""
    print("\n" + "█" * 75)
    print("█ " + "TP2 - ANALYSE BIVARIÉE - HEART DISEASE DATASET".center(71) + " █")
    print("█" * 75)
    
    try:
        df = load_data()
        print(f"\n✓ Dataset chargé : {len(df)} patients, {len(df.columns)} variables")
        
        analyze_pairs(df)
        
    except Exception as e:
        print(f"\n✗ Erreur lors de l'exécution : {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
