"""
src - Package contenant les scripts d'analyse pour les TPs

Modules:
    - tp1_analysis: Analyse univariée (TP1)
    - tp2_analysis: Analyse bivariée (TP2) [À venir]
    - utils: Fonctions utilitaires partagées
"""

__version__ = "1.0.0"
__author__ = "Étudiants IA-Industrie 4.0, ENSAM Béni Mellal"

from . import utils
from . import tp1_analysis
from . import tp2_analysis

__all__ = ['utils', 'tp1_analysis', 'tp2_analysis']
