"""
TP1 - Analyse Univariée des Données (Heart Disease Dataset)

Module : tp1_analysis.py
Description : Analyse exploratoire univariée complète avec visualisations.

Auteur : Étudiants IA-Industrie 4.0
Date : 2026
Version : 1.0

Contenu :
    - Partie A : Chargement et préparation des données
    - Partie B : Analyse d'une variable quantitative (age)
    - Partie C : Analyse d'une variable qualitative (sex)
    - Partie D : Automatisation via des fonctions réutilisables
    - Partie E : Détection des outliers
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import skew, kurtosis
from pathlib import Path

# ============================================================================
# Configuration globale
# ============================================================================

# Configuration matplotlib
plt.rcParams['figure.figsize'] = (10, 5)
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['font.size'] = 10
sns.set_style("whitegrid")

# Chemin de données
DATA_DIR = Path(__file__).parent.parent / "data"
CSV_FILE = DATA_DIR / "Base_Maladie_Cardiaque.csv"


# ============================================================================
# PARTIE A - Chargement et préparation des données
# ============================================================================

def load_and_prepare_data(filepath):
    """
    Charge le CSV et prépare les données.
    
    Args:
        filepath (str or Path): Chemin vers le fichier CSV
        
    Returns:
        pd.DataFrame: DataFrame préparé avec types appropriés
    """
    print("=" * 70)
    print("PARTIE A — Chargement et préparation des données")
    print("=" * 70)
    
    # Charger les données
    df = pd.read_csv(filepath)
    
    print(f"\n✓ Données chargées avec succès")
    print(f"  • Nombre de lignes (patients)   : {df.shape[0]}")
    print(f"  • Nombre de colonnes (variables): {df.shape[1]}")
    print(f"\n  Colonnes : {list(df.columns)}")
    print(f"\nAperçu des 5 premières lignes :")
    print(df.head().to_string())
    
    # Conversion des variables catégorielles
    categorical_vars = ["sex", "cp", "fbs", "restecg", "exang", "slope", "thal", "target"]
    df[categorical_vars] = df[categorical_vars].apply(lambda x: x.astype("category"))
    
    print(f"\n✓ Variables catégorielles converties")
    print(f"\nTypes de données :")
    print(df.dtypes)
    
    # Vérification des valeurs manquantes
    missing = df.isnull().sum()
    if missing.sum() == 0:
        print(f"\n✓ Aucune valeur manquante détectée")
    else:
        print(f"\nValeurs manquantes :\n{missing[missing > 0]}")
    
    return df


# ============================================================================
# PARTIE B - Analyse d'une variable quantitative
# ============================================================================

def analyze_quantitative_variable(series, var_name="age"):
    """
    Analyse complète d'une variable quantitative.
    
    Args:
        series (pd.Series): Série de données à analyser
        var_name (str): Nom de la variable pour les titres
        
    Returns:
        dict: Dictionnaire avec tous les indicateurs statistiques
    """
    print("\n" + "=" * 70)
    print(f"PARTIE B — Variable quantitative : {var_name}")
    print("=" * 70)
    
    # Calcul des indicateurs
    stats_dict = {
        'Moyenne': series.mean(),
        'Médiane': series.median(),
        'Mode': series.mode()[0] if len(series.mode()) > 0 else None,
        'Écart-type': series.std(),
        'Variance': series.var(),
        'Minimum': series.min(),
        'Maximum': series.max(),
        'Q1': series.quantile(0.25),
        'Q3': series.quantile(0.75),
        'IQR': series.quantile(0.75) - series.quantile(0.25),
        'Asymétrie (Skewness)': skew(series),
        'Aplatissement (Kurtosis)': kurtosis(series),
    }
    
    # Affichage formaté
    print(f"\n--- Tableau récapitulatif des indicateurs ---")
    print(f"\n{'Indicateur':<25} {'Valeur':>12}   Interprétation")
    print("-" * 80)
    for key, value in stats_dict.items():
        if isinstance(value, float):
            print(f"{key:<25} {value:>12.2f}")
        else:
            print(f"{key:<25} {value:>12}")
    
    # Interprétation
    mean = stats_dict['Moyenne']
    median = stats_dict['Médiane']
    skewness = stats_dict['Asymétrie (Skewness)']
    
    print(f"\n--- Interprétation ---")
    print(f"Moyenne ({mean:.1f}) vs Médiane ({median:.1f})")
    diff = abs(mean - median)
    if diff < 2:
        print("→ Distribution quasi-symétrique (moyenne ≈ médiane)")
    elif mean > median:
        print("→ Queue à droite : quelques valeurs élevées tirent la moyenne vers le haut")
    else:
        print("→ Queue à gauche : quelques valeurs basses tirent la moyenne vers le bas")
    
    print(f"\nSkewness = {skewness:.3f}")
    if abs(skewness) < 0.5:
        print("→ Distribution symétrique (tests paramétriques applicables)")
    elif skewness > 0:
        print("→ Asymétrie positive (queue à droite)")
    else:
        print("→ Asymétrie négative (queue à gauche)")
    
    return stats_dict


def plot_quantitative_variable(series, var_name="age", save_path=None):
    """
    Génère 4 graphiques pour une variable quantitative.
    
    Args:
        series (pd.Series): Série de données
        var_name (str): Nom de la variable
        save_path (str): Chemin pour sauvegarder (optionnel)
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f"Analyse univariée — {var_name}", fontsize=14, fontweight='bold')
    
    mean = series.mean()
    median = series.median()
    
    # Histogramme
    sns.histplot(series, bins=25, kde=False, color='steelblue', 
                 ax=axes[0, 0], edgecolor='white')
    axes[0, 0].axvline(mean, color='red', linestyle='--', linewidth=1.5,
                       label=f'Moyenne = {mean:.1f}')
    axes[0, 0].axvline(median, color='orange', linestyle='--', linewidth=1.5,
                       label=f'Médiane = {median:.1f}')
    axes[0, 0].set_title("Histogramme")
    axes[0, 0].set_xlabel(var_name)
    axes[0, 0].set_ylabel("Fréquence")
    axes[0, 0].legend()
    
    # Boxplot
    sns.boxplot(x=series, color='lightgreen', ax=axes[0, 1],
                flierprops=dict(marker='o', markerfacecolor='red', markersize=5))
    axes[0, 1].set_title("Boxplot")
    axes[0, 1].set_xlabel(var_name)
    
    # KDE
    sns.kdeplot(series, fill=True, color='darkorange', alpha=0.6, ax=axes[1, 0])
    axes[1, 0].axvline(mean, color='red', linestyle='--', linewidth=1.5,
                       label=f'Moyenne = {mean:.1f}')
    axes[1, 0].set_title("Courbe de densité (KDE)")
    axes[1, 0].set_xlabel(var_name)
    axes[1, 0].set_ylabel("Densité")
    axes[1, 0].legend()
    
    # QQ Plot
    (osm, osr), (slope_val, intercept, r) = stats.probplot(series, dist="norm")
    axes[1, 1].plot(osm, osr, 'o', color='steelblue', markersize=4, alpha=0.7)
    axes[1, 1].plot(osm, slope_val * osm + intercept, 'r-', linewidth=1.5)
    axes[1, 1].set_title(f"QQ Plot (r = {r:.4f})")
    axes[1, 1].set_xlabel("Quantiles théoriques")
    axes[1, 1].set_ylabel("Quantiles observés")
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Graphique sauvegardé : {save_path}")
    
    plt.show()


# ============================================================================
# PARTIE C - Analyse d'une variable qualitative
# ============================================================================

def analyze_qualitative_variable(series, var_name="sex"):
    """
    Analyse complète d'une variable qualitative.
    
    Args:
        series (pd.Series): Série de données
        var_name (str): Nom de la variable
        
    Returns:
        dict: Dictionnaire avec fréquences et proportions
    """
    print("\n" + "=" * 70)
    print(f"PARTIE C — Variable qualitative : {var_name}")
    print("=" * 70)
    
    freq_abs = series.value_counts()
    freq_prop = series.value_counts(normalize=True) * 100
    mode_val = series.mode()[0] if len(series.mode()) > 0 else None
    
    print(f"\n--- Fréquences absolues et relatives ---")
    print(f"\n{'Catégorie':<20} {'Fréquence':>10} {'Proportion':>10}")
    print("-" * 45)
    for cat in freq_abs.index:
        print(f"{str(cat):<20} {freq_abs[cat]:>10} {freq_prop[cat]:>9.1f}%")
    
    print(f"\nMode (catégorie dominante) : {mode_val}")
    print(f"Nombre de catégories : {len(freq_abs)}")
    
    return {'frequencies': freq_abs, 'proportions': freq_prop, 'mode': mode_val}


def plot_qualitative_variable(series, var_name="sex", save_path=None):
    """
    Génère graphiques pour une variable qualitative.
    
    Args:
        series (pd.Series): Série de données
        var_name (str): Nom de la variable
        save_path (str): Chemin pour sauvegarder (optionnel)
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle(f"Analyse univariée — {var_name}", fontsize=14, fontweight='bold')
    
    # Countplot
    sns.countplot(x=series, palette='Set2', ax=axes[0])
    axes[0].set_title("Diagramme en barres (Effectifs)")
    axes[0].set_xlabel(var_name)
    axes[0].set_ylabel("Effectif")
    for p in axes[0].patches:
        axes[0].annotate(f'{int(p.get_height())}',
                        (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='bottom')
    
    # Pie chart
    values = series.value_counts()
    axes[1].pie(values.values, labels=values.index, autopct='%1.1f%%',
               startangle=90)
    axes[1].set_title("Répartition (Proportions)")
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Graphique sauvegardé : {save_path}")
    
    plt.show()


# ============================================================================
# PARTIE D - Automatisation via des fonctions
# ============================================================================

def statistics_summary(df):
    """
    Génère un tableau récapitulatif de toutes les variables quantitatives.
    
    Args:
        df (pd.DataFrame): DataFrame source
        
    Returns:
        pd.DataFrame: Tableau avec toutes les statistiques
    """
    print("\n" + "=" * 70)
    print("PARTIE D — Tableau récapitulatif automatisé")
    print("=" * 70)
    
    quantitative_vars = df.select_dtypes(include=['number']).columns.tolist()
    
    stats_df = pd.DataFrame({
        "N": df[quantitative_vars].count(),
        "Moyenne": df[quantitative_vars].mean().round(2),
        "Std": df[quantitative_vars].std().round(2),
        "Min": df[quantitative_vars].min(),
        "Q1": df[quantitative_vars].quantile(0.25).round(2),
        "Médiane": df[quantitative_vars].quantile(0.50).round(2),
        "Q3": df[quantitative_vars].quantile(0.75).round(2),
        "Max": df[quantitative_vars].max(),
        "IQR": (df[quantitative_vars].quantile(0.75) - 
                df[quantitative_vars].quantile(0.25)).round(2),
        "Skewness": df[quantitative_vars].apply(skew).round(3),
        "Kurtosis": df[quantitative_vars].apply(kurtosis).round(3),
    })
    
    print("\n" + stats_df.to_string())
    return stats_df


# ============================================================================
# PARTIE E - Détection des outliers
# ============================================================================

def detect_outliers_iqr(df):
    """
    Détecte les outliers via la méthode IQR.
    
    Args:
        df (pd.DataFrame): DataFrame source
        
    Returns:
        pd.DataFrame: Tableau résumé des outliers
    """
    print("\n" + "=" * 70)
    print("PARTIE E — Détection des outliers (méthode IQR)")
    print("=" * 70)
    
    quantitative_vars = df.select_dtypes(include=['number']).columns.tolist()
    results = []
    
    for col in quantitative_vars:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        
        outliers_mask = (df[col] < lower_bound) | (df[col] > upper_bound)
        n_outliers = outliers_mask.sum()
        pct_outliers = (n_outliers / len(df)) * 100
        
        results.append({
            'Variable': col,
            'Borne basse': round(lower_bound, 2),
            'Borne haute': round(upper_bound, 2),
            'Nb outliers': n_outliers,
            '% dataset': round(pct_outliers, 1),
        })
    
    outliers_df = pd.DataFrame(results).set_index('Variable')
    print("\n" + outliers_df.to_string())
    return outliers_df


# ============================================================================
# Fonction principale
# ============================================================================

def main():
    """Exécute l'analyse complète."""
    
    # Charger les données
    df = load_and_prepare_data(CSV_FILE)
    
    # Analyse de 'age'
    analyze_quantitative_variable(df['age'], 'age')
    plot_quantitative_variable(df['age'], 'age')
    
    # Analyse de 'sex'
    analyze_qualitative_variable(df['sex'], 'sex')
    plot_qualitative_variable(df['sex'], 'sex')
    
    # Tableau récapitulatif
    statistics_summary(df)
    
    # Détection outliers
    detect_outliers_iqr(df)
    
    print("\n" + "=" * 70)
    print("✓ ANALYSE COMPLÈTE TERMINÉE")
    print("=" * 70)


if __name__ == "__main__":
    main()
