


# =============================================================================
# PARTIE A — Chargement et préparation des données
# =============================================================================

# --- A.1 Importation des bibliothèques ---------------------------------------

import pandas as pd               # Manipulation de tableaux de données (DataFrames)
import seaborn as sns             # Visualisations statistiques (basé sur matplotlib)
import matplotlib.pyplot as plt   # Contrôle fin des graphiques
from scipy import stats           # Tests statistiques et lois de probabilité
from scipy.stats import skew, kurtosis  # Asymétrie et aplatissement

# Paramètres globaux d'affichage
plt.rcParams['figure.figsize'] = (10, 5)
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['axes.labelsize'] = 11

print("=" * 60)
print("TP1 — Analyse univariée — Heart Disease Dataset")
print("=" * 60)
print("✓ Bibliothèques importées avec succès.")


# --- A.2 Chargement du fichier CSV -------------------------------------------

# read_csv() lit un fichier texte séparé par des virgules et crée un DataFrame.
# Un DataFrame = tableau à 2 dimensions (lignes = patients, colonnes = variables).
df = pd.read_csv("Base_Maladie_Cardiaque.csv")

print(f"\nNombre de lignes (patients)   : {df.shape[0]}")
print(f"Nombre de colonnes (variables): {df.shape[1]}")
print(f"\nNoms des colonnes :\n{list(df.columns)}")
print(f"\nTypes détectés automatiquement par pandas :\n{df.dtypes}")
print(f"\nAperçu des 5 premières lignes :")
print(df.head().to_string())


# --- A.3 Conversion des variables catégorielles ------------------------------

# Certaines variables sont stockées comme entiers mais représentent des catégories.
# Exemple : sex = 0 ou 1 (femme/homme), pas une quantité mesurable.
# Les convertir en 'category' évite des calculs erronés (ex: moyenne du sexe).

# Une lambda est une fonction anonyme sur une ligne :
# lambda x: x.astype("category")  ≡  def f(x): return x.astype("category")

liste_variable = ["sex", "cp", "fbs", "restecg", "exang", "slope", "thal", "target"]
df[liste_variable] = df[liste_variable].apply(lambda x: x.astype("category"))

print("\nTypes après conversion :")
print(df.dtypes)

# Vérification des valeurs manquantes
manquants = df.isnull().sum()
total_manquants = manquants.sum()
if total_manquants == 0:
    print("\n✓ Aucune valeur manquante détectée.")
else:
    print(f"\nValeurs manquantes :\n{manquants[manquants > 0]}")

input("\n[Appuyer sur Entrée pour continuer vers la Partie B...]")


# =============================================================================
# PARTIE B — Analyse univariée d'une variable quantitative : age
# =============================================================================

print("\n" + "=" * 60)
print("PARTIE B — Variable quantitative : age")
print("=" * 60)


# --- B.1 Calcul des indicateurs statistiques ---------------------------------

age = df['age']

# Résumé automatique
print("\n--- Résumé automatique (describe) ---")
print(age.describe().round(2))

# Calcul manuel de chaque indicateur
moyenne    = age.mean()
mediane    = age.median()
mode       = age.mode()[0]
ecart_type = age.std()
variance   = age.var()
min_age    = age.min()
max_age    = age.max()
q1         = age.quantile(0.25)
q3         = age.quantile(0.75)
iqr        = q3 - q1
asymetrie  = skew(age)
aplatiss   = kurtosis(age)

print("\n--- Tableau récapitulatif des indicateurs ---")
indicateurs = [
    ("Moyenne",    moyenne,    "Âge moyen des patients"),
    ("Médiane",    mediane,    "La moitié des patients ont moins que cet âge"),
    ("Mode",       mode,       "Âge le plus fréquent dans le dataset"),
    ("Écart-type", ecart_type, "Dispersion moyenne autour de la moyenne"),
    ("Variance",   variance,   "Dispersion au carré"),
    ("Minimum",    min_age,    "Patient le plus jeune"),
    ("Maximum",    max_age,    "Patient le plus âgé"),
    ("Q1",         q1,         "25% des patients ont moins que cet âge"),
    ("Q3",         q3,         "75% des patients ont moins que cet âge"),
    ("IQR",        iqr,        "Étendue centrale (Q3 - Q1)"),
    ("Skewness",   asymetrie,  "≈0 symétrique | >0 queue à droite | <0 queue à gauche"),
    ("Kurtosis",   aplatiss,   "Comparé à une loi normale (référence = 0)"),
]
print(f"\n{'Indicateur':<14} {'Valeur':>8}   Interprétation")
print("-" * 70)
for nom, val, interp in indicateurs:
    print(f"{nom:<14} {val:>8.2f}   {interp}")

# Réponse analyse
print("\n--- Interprétation ---")
diff = abs(moyenne - mediane)
print(f"Moyenne ({moyenne:.1f}) vs Médiane ({mediane:.1f}) → écart = {diff:.1f} ans")
if diff < 2:
    print("→ Distribution quasi-symétrique (moyenne ≈ médiane).")
elif moyenne > mediane:
    print("→ Queue à droite : quelques patients âgés tirent la moyenne vers le haut.")
else:
    print("→ Queue à gauche : quelques patients jeunes tirent la moyenne vers le bas.")

print(f"IQR = {iqr:.0f} ans → 50% des patients ont entre {q1:.0f} et {q3:.0f} ans.")
print(f"Seuil outlier bas  : Q1 - 1.5×IQR = {q1 - 1.5*iqr:.1f} ans")
print(f"Seuil outlier haut : Q3 + 1.5×IQR = {q3 + 1.5*iqr:.1f} ans")


# --- B.2 Visualisations graphiques -------------------------------------------

# ── Histogramme ──────────────────────────────────────────────────────────────
print("\nAffichage : Histogramme de l'âge...")
plt.figure(figsize=(10, 5))
sns.histplot(df['age'], bins=20, kde=False, color='steelblue', edgecolor='white')
plt.axvline(moyenne, color='red', linestyle='--', linewidth=1.5,
            label=f'Moyenne = {moyenne:.1f}')
plt.axvline(mediane, color='orange', linestyle='--', linewidth=1.5,
            label=f'Médiane = {mediane:.1f}')
plt.title("Histogramme de l'âge des patients")
plt.xlabel("Âge (années)")
plt.ylabel("Nombre de patients")
plt.legend()
plt.tight_layout()
plt.show()

# ── Boxplot ───────────────────────────────────────────────────────────────────
print("Affichage : Boxplot de l'âge...")
plt.figure(figsize=(10, 4))
sns.boxplot(x=df['age'], color='lightblue', width=0.4,
            flierprops=dict(marker='o', markerfacecolor='red', markersize=5))
plt.title("Boxplot de l'âge des patients")
plt.xlabel("Âge (années)")
plt.tight_layout()
plt.show()

# ── Courbe de densité KDE ────────────────────────────────────────────────────
# KDE = Kernel Density Estimate : version lissée de l'histogramme.
# La surface sous la courbe = 1 (densité de probabilité). Pas de choix de bins.
print("Affichage : Courbe KDE de l'âge...")
plt.figure(figsize=(10, 5))
sns.kdeplot(df['age'], fill=True, color='seagreen', alpha=0.6)
plt.axvline(moyenne, color='red', linestyle='--', linewidth=1.5,
            label=f'Moyenne = {moyenne:.1f}')
plt.title("Courbe de densité (KDE) de l'âge des patients")
plt.xlabel("Âge (années)")
plt.ylabel("Densité")
plt.legend()
plt.tight_layout()
plt.show()

# ── Violin plot ───────────────────────────────────────────────────────────────
# Combine boxplot + KDE : la largeur à chaque niveau = densité de patients.
print("Affichage : Violin plot de l'âge...")
plt.figure(figsize=(10, 5))
sns.violinplot(x=df['age'], color='lightcoral', inner='box')
plt.title("Violin plot de l'âge des patients")
plt.xlabel("Âge (années)")
plt.tight_layout()
plt.show()

# ── QQ Plot ───────────────────────────────────────────────────────────────────
# Compare les quantiles observés aux quantiles d'une loi normale théorique.
# Si les points suivent la droite → distribution proche d'une loi normale.
print("Affichage : QQ Plot de l'âge...")
plt.figure(figsize=(7, 6))
(osm, osr), (slope_val, intercept, r) = stats.probplot(df['age'], dist="norm")
plt.plot(osm, osr, 'o', color='steelblue', markersize=4, alpha=0.7,
         label='Données observées')
plt.plot(osm, slope_val * osm + intercept, 'r-', linewidth=1.5,
         label='Droite normale théorique')
plt.title("QQ Plot de l'âge des patients")
plt.xlabel("Quantiles théoriques (loi normale)")
plt.ylabel("Quantiles observés")
plt.legend()
plt.tight_layout()
plt.show()
print(f"Coefficient de corrélation avec la droite normale : r = {r:.4f}")
print("→ Plus r est proche de 1, plus la distribution est normale.")

print("\n--- Réponses aux questions B ---")
print("Q1 : L'histogramme montre une distribution quasi-symétrique centrée")
print("     autour de 54-57 ans. Les patients jeunes (<40) sont rares.")
print("Q2 : Le boxplot peut révéler quelques outliers (points rouges).")
print("Q3 : Le QQ plot confirme une distribution proche de la normale si r > 0.99.")
print("Q4 : L'histogramme est le plus accessible pour un non-spécialiste.")

input("\n[Appuyer sur Entrée pour continuer vers la Partie C...]")


# =============================================================================
# PARTIE C — Analyse univariée d'une variable qualitative : sex
# =============================================================================

print("\n" + "=" * 60)
print("PARTIE C — Variable qualitative : sex")
print("=" * 60)
print("Pour une variable qualitative, on travaille avec des")
print("fréquences et proportions, pas avec des moyennes.")


# --- C.1 Résumé numérique ----------------------------------------------------

variable   = df['sex']
freq_abs   = variable.value_counts()
proportion = variable.value_counts(normalize=True) * 100
mode_sex   = variable.mode()[0]

print("\n--- Fréquences absolues ---")
print(freq_abs.rename(index={0: 'Femme (0)', 1: 'Homme (1)',
                              '0': 'Femme (0)', '1': 'Homme (1)'}))

print("\n--- Proportions (%) ---")
print(proportion.rename(index={0: 'Femme (0)', 1: 'Homme (1)',
                                '0': 'Femme (0)', '1': 'Homme (1)'}).round(1))

print(f"\nMode (catégorie dominante) : {mode_sex}")
print("→ Homme" if str(mode_sex) in ['1', 1] else "→ Femme")
print("→ Le dataset est déséquilibré : les hommes sont sur-représentés.")
print("  Ce biais doit être mentionné dans toute interprétation.")


# --- C.2 Représentations graphiques ------------------------------------------

# ── Diagramme en barres (countplot) ──────────────────────────────────────────
print("\nAffichage : Diagramme en barres (sexe)...")
plt.figure(figsize=(7, 5))
ax = sns.countplot(x='sex', data=df, palette='Set2',
                   order=df['sex'].value_counts().index)
for p in ax.patches:
    ax.annotate(f'{int(p.get_height())}',
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='bottom', fontsize=11)
labels = ['Femme (0)', 'Homme (1)'] if str(df['sex'].value_counts().index[0]) in ['0', 0] \
         else ['Homme (1)', 'Femme (0)']
ax.set_xticklabels(labels)
plt.title("Répartition du sexe des patients")
plt.xlabel("Sexe")
plt.ylabel("Nombre de patients")
plt.tight_layout()
plt.show()

# ── Barres avec proportions ---------------------------------------------------
print("Affichage : Barres proportions (sexe)...")
proportions_vals = df['sex'].value_counts(normalize=True) * 100
cats = [str(k) for k in proportions_vals.index]
vals_plot = list(proportions_vals.values)
labels_plot = ['Femme (0)' if c in ['0', 0] else 'Homme (1)' for c in cats]

plt.figure(figsize=(7, 5))
ax2 = sns.barplot(x=labels_plot, y=vals_plot, palette='Set2')
for p in ax2.patches:
    ax2.annotate(f'{p.get_height():.1f}%',
                 (p.get_x() + p.get_width() / 2., p.get_height()),
                 ha='center', va='bottom', fontsize=11)
plt.title("Proportions du sexe des patients")
plt.xlabel("Sexe")
plt.ylabel("Proportion (%)")
plt.ylim(0, 100)
plt.tight_layout()
plt.show()

# ── Pie chart + Donut ---------------------------------------------------------
print("Affichage : Pie chart et Donut (sexe)...")
vals_pie = df['sex'].value_counts()
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

ax1.pie(vals_pie.values, labels=['Homme', 'Femme'],
        autopct='%1.1f%%', startangle=90,
        colors=['#66b3ff', '#ff9999'], textprops={'fontsize': 11})
ax1.set_title("Pie chart — Sexe des patients")

ax2.pie(vals_pie.values, labels=['Homme', 'Femme'],
        autopct='%1.1f%%', startangle=90,
        colors=['#66b3ff', '#ff9999'],
        wedgeprops={'width': 0.5}, textprops={'fontsize': 11})
ax2.set_title("Donut chart — Sexe des patients")

plt.tight_layout()
plt.show()

print("\n--- Réponses aux questions C ---")
print("Q1 : Les hommes sont la catégorie dominante (~68% du dataset).")
print("Q2 : Le countplot (barres) est le plus lisible : hauteurs comparables")
print("     directement, effectifs lisibles, clair pour tout public.")
print("Q3 : Le pie chart est déconseillé avec 4+ catégories ou des proportions")
print("     proches (ex: 30/35/35%). Les angles sont difficiles à distinguer.")

input("\n[Appuyer sur Entrée pour continuer vers la Partie D...]")


# =============================================================================
# PARTIE D — Automatisation de l'analyse
# =============================================================================

print("\n" + "=" * 60)
print("PARTIE D — Automatisation (fonctions Python)")
print("=" * 60)
print("Principe DRY : Don't Repeat Yourself.")
print("On écrit le code une fois et on l'applique à toutes les variables.")


# --- D.1 Récupération automatique des variables quantitatives ----------------

liste_variable_quanti = df.select_dtypes(include=['number']).columns.tolist()
print(f"\nVariables quantitatives détectées : {liste_variable_quanti}")
print(f"Nombre : {len(liste_variable_quanti)}")


# --- D.2 Fonction de statistiques descriptives -------------------------------

def statDesc(base):
    """
    Calcule les statistiques descriptives de toutes les variables quantitatives.

    Paramètre : base (DataFrame)
    Retourne  : DataFrame avec une ligne par variable, une colonne par indicateur
    """
    quanti = base.select_dtypes(include=['number']).columns.tolist()

    return pd.DataFrame({
        "N"        : base[quanti].count(),
        "Moyenne"  : base[quanti].mean().round(2),
        "Std"      : base[quanti].std().round(2),
        "Variance" : base[quanti].var().round(2),
        "Min"      : base[quanti].min(),
        "Q1"       : base[quanti].quantile(0.25),
        "Médiane"  : base[quanti].quantile(0.50),
        "Q3"       : base[quanti].quantile(0.75),
        "Max"      : base[quanti].max(),
        "IQR"      : (base[quanti].quantile(0.75) - base[quanti].quantile(0.25)).round(2),
        "Skewness" : base[quanti].apply(skew).round(3),
        "Kurtosis" : base[quanti].apply(kurtosis).round(3),
    })


print("\n=== Test de statDesc() ===")
print(statDesc(df).to_string())


# --- D.3 Fonction de génération automatique des graphiques -------------------

def graphique_quanti(base, variables=None):
    """
    Génère 3 graphiques (histogramme, boxplot, KDE) pour chaque variable
    quantitative. Version améliorée : graphiques côte à côte + annotation skewness.

    Paramètres :
        base      : DataFrame source
        variables : liste de colonnes (None = toutes les quantitatives)
    """
    if variables is None:
        variables = base.select_dtypes(include=['number']).columns.tolist()

    for col in variables:
        fig, axes = plt.subplots(1, 3, figsize=(16, 4))
        fig.suptitle(f"Analyse univariée — {col}", fontsize=13,
                     fontweight='bold', y=1.02)

        # Histogramme
        sns.histplot(base[col], bins=25, color="steelblue",
                     ax=axes[0], edgecolor='white')
        axes[0].axvline(base[col].mean(), color='red',
                        linestyle='--', linewidth=1.3,
                        label=f"Moy={base[col].mean():.1f}")
        axes[0].axvline(base[col].median(), color='orange',
                        linestyle='--', linewidth=1.3,
                        label=f"Med={base[col].median():.1f}")
        axes[0].set_title("Histogramme")
        axes[0].set_xlabel(col)
        axes[0].legend(fontsize=9)

        # Boxplot
        sns.boxplot(x=base[col], color="lightgreen", ax=axes[1],
                    flierprops=dict(marker='o', markerfacecolor='red',
                                    markersize=4))
        axes[1].set_title("Boxplot")
        axes[1].set_xlabel(col)

        # KDE
        sns.kdeplot(base[col], fill=True, color="darkorange",
                    alpha=0.6, ax=axes[2])
        axes[2].set_title("Courbe de densité (KDE)")
        axes[2].set_xlabel(col)
        axes[2].set_ylabel("Densité")

        plt.tight_layout()
        plt.show()

        # Résumé textuel
        sk = skew(base[col].dropna())
        print(f"  {col} → Skewness = {sk:.3f}", end="")
        print(" (symétrique)" if abs(sk) < 0.5
              else " (queue à droite)" if sk > 0
              else " (queue à gauche)")
        print()


# --- D.4 Fonction finale combinée --------------------------------------------

def statDescFinal(base, variables=None):
    """
    Fonction complète : génère les graphiques ET retourne le tableau de stats.

    Paramètres :
        base      : DataFrame source
        variables : liste de colonnes (None = toutes les quantitatives)
    Retourne : DataFrame des statistiques descriptives
    """
    print("=" * 60)
    print("ANALYSE UNIVARIÉE COMPLÈTE — VARIABLES QUANTITATIVES")
    print("=" * 60)
    graphique_quanti(base, variables)
    print("\n=== Tableau récapitulatif des statistiques ===\n")
    result = statDesc(base)
    print(result.to_string())
    return result


# --- D.5 Amélioration : détection automatique des outliers -------------------

def detecter_outliers(base):
    """
    Amélioration personnelle : détecte les outliers via la méthode IQR
    pour chaque variable quantitative.

    Règle : valeur suspecte si hors de [Q1 - 1.5×IQR, Q3 + 1.5×IQR]

    Paramètre : base (DataFrame)
    Retourne  : DataFrame avec le nombre et % d'outliers par variable
    """
    quanti = base.select_dtypes(include=['number']).columns.tolist()
    resultats = []

    for col in quanti:
        q1_c  = base[col].quantile(0.25)
        q3_c  = base[col].quantile(0.75)
        iqr_c = q3_c - q1_c
        borne_bas  = q1_c - 1.5 * iqr_c
        borne_haut = q3_c + 1.5 * iqr_c

        mask     = (base[col] < borne_bas) | (base[col] > borne_haut)
        outliers = base.loc[mask, col]
        n        = len(outliers)
        pct      = round(n / len(base) * 100, 1)

        resultats.append({
            "Variable"    : col,
            "Borne basse" : round(borne_bas, 2),
            "Borne haute" : round(borne_haut, 2),
            "Nb outliers" : n,
            "% dataset"   : pct,
            "Min outlier" : round(outliers.min(), 1) if n > 0 else "—",
            "Max outlier" : round(outliers.max(), 1) if n > 0 else "—",
        })

    df_out = pd.DataFrame(resultats).set_index("Variable")
    return df_out


# ── Tests des fonctions ───────────────────────────────────────────────────────
print("\nTest de graphique_quanti() sur toutes les variables quantitatives...")
graphique_quanti(df)

print("\n=== Détection des outliers (méthode IQR) ===")
print(detecter_outliers(df).to_string())


# =============================================================================
# CONCLUSION GÉNÉRALE
# =============================================================================

print("\n" + "=" * 60)
print("CONCLUSION GÉNÉRALE DU TP1")
print("=" * 60)
print("""
Ce TP1 nous a permis de réaliser une analyse exploratoire univariée
complète du Heart Disease Dataset.

Points clés :

1. Préparation des données
   → Distinguer le type Python (int/float) de la nature statistique
     (quantitative/qualitative) est indispensable avant toute analyse.

2. Variable age (quantitative continue)
   → Distribution quasi-normale, centrée autour de 54-55 ans.
   → Faible asymétrie → tests paramétriques applicables en TP3.
   → Quelques outliers aux extrêmes, à surveiller.

3. Variable sex (qualitative nominale)
   → Déséquilibre important : ~68% d'hommes dans le dataset.
   → Ce biais doit être mentionné dans toutes les analyses suivantes.

4. Automatisation (Partie D)
   → Les fonctions statDesc, graphique_quanti et detecter_outliers
     réduisent le temps d'analyse et limitent les erreurs humaines.

Prochaine étape (TP2) :
   → Étudier les relations ENTRE les variables (analyse bivariée).
   → Comment age, chol, thalach évoluent-ils selon la maladie ?
""")
