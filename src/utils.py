"""
utils.py - Fonctions utilitaires pour les TPs

Contient des fonctions réutilisables partagées entre les TPs.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


def get_project_root():
    """Retourne le chemin racine du projet."""
    return Path(__file__).parent.parent


def ensure_data_directory():
    """Crée le répertoire data/ s'il n'existe pas."""
    data_dir = get_project_root() / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def setup_plotting():
    """Configure les paramètres globaux pour matplotlib et seaborn."""
    plt.rcParams['figure.figsize'] = (10, 6)
    plt.rcParams['axes.titlesize'] = 13
    plt.rcParams['axes.labelsize'] = 11
    plt.rcParams['font.size'] = 10
    sns.set_style("whitegrid")
    sns.set_palette("husl")


def save_figure(fig, filename, directory=None):
    """
    Sauvegarde une figure matplotlib.
    
    Args:
        fig: Figure matplotlib
        filename (str): Nom du fichier (avec extension)
        directory (Path or str): Répertoire de sauvegarde (défaut: outputs/)
    """
    if directory is None:
        directory = get_project_root() / "outputs"
    
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    
    filepath = directory / filename
    fig.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"✓ Figure sauvegardée : {filepath}")
    return filepath


def print_section(title, level=1):
    """Affiche un titre de section formaté."""
    if level == 1:
        print("\n" + "=" * 70)
        print(title.center(70))
        print("=" * 70)
    elif level == 2:
        print(f"\n--- {title} ---")
    else:
        print(f"\n{title}")


class DataAnalyzer:
    """Classe base pour l'analyse de données."""
    
    def __init__(self, df):
        """
        Initialise l'analyseur.
        
        Args:
            df (pd.DataFrame): DataFrame à analyser
        """
        self.df = df
        self.quantitative_cols = df.select_dtypes(include=['number']).columns.tolist()
        self.qualitative_cols = df.select_dtypes(include=['category', 'object']).columns.tolist()
    
    def summary(self):
        """Affiche un résumé du DataFrame."""
        print(f"Shape: {self.df.shape}")
        print(f"Colonnes quantitatives: {self.quantitative_cols}")
        print(f"Colonnes qualitatives: {self.qualitative_cols}")
        print(f"Valeurs manquantes: {self.df.isnull().sum().sum()}")
