import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import skew, kurtosis

# Charger le fichier CSV dans un DataFrame
df = pd.read_csv("Base_Maladie_Cardiaque.csv")

# Voir les 5 premières lignes
print("les 5 premières lignes sont : ",df.head())
print("*******************")
# Dimensions : (nb_lignes, nb_colonnes)
print("les dimensions sont : ",df.shape)
print("*******************")
# Noms des colonnes
print(df.columns)
print("*******************")

# Variables à convertir en catégories
liste_vars = ["sex", "cp", "fbs", "restecg",
             "exang", "slope", "thal", "target"]

# lambda = fonction anonyme courte
# x → x.astype("category") s'applique à chaque colonne
df[liste_vars] = df[liste_vars].apply(lambda x: x.astype("category"))

df.dtypes  # vérifier les types

age = df['age']
print(age.describe())
print("*******************")

moyenne    = age.mean()
mediane    = age.median()
q1         = age.quantile(0.25)
q3         = age.quantile(0.75)
iqr        = q3 - q1
asymetrie  = skew(age)
aplatiss   = kurtosis(age)

print(f"Moyenne : {moyenne:.2f}")
print(f"Médiane : {mediane:.2f}")
print(f"Q1 : {q1:.2f}")
print(f"Q3 : {q3:.2f}")
print(f"IQR : {iqr:.2f}")
print(f"Asymétrie : {asymetrie:.2f}")
print(f"Aplatissement : {aplatiss:.2f}")
print("*******************")

# Histogramme
plt.figure(figsize=(10, 6))
sns.histplot(df['age'], bins=20, kde=False, color='blue')
plt.title("Distribution de l'âge des patients")
plt.show()

# Boxplot : détecte visuellement les outliers Comment lire un boxplot ?
# La boîte centrale contient 50% des données (de Q1 à Q3).
# Le trait du milieu = la médiane.
# Les moustaches s'étendent jusqu'à 1.5×IQR.
# Les points au-delà des moustaches = outliers potentiels.
print("*******************")
plt.figure(figsize=(8, 6))
sns.boxplot(x=df['age'], color='lightblue')
plt.show()

# KDE : densité lissée (pas de bins à choisir)
print("*******************")
plt.figure(figsize=(10, 6))
sns.kdeplot(df['age'], fill=True, color='green')
plt.show()

# QQ Plot : si les points ≈ la droite → normalité
stats.probplot(df['age'], dist="norm", plot=plt)
plt.show()

#Pourquoi utiliser plusieurs graphiques pour la même variable ?
#Chaque graphique révèle un aspect différent : 
#l'histogramme montre les fréquences brutes, 
#le KDE la forme lissée, le boxplot les outliers, 
#le QQ plot la normalité.
#Ensemble, ils donnent une image complète.

# Résumé numérique d'une variable qualitative

#Ce qu'on calcule pour une variable qualitative
#On ne peut pas calculer de moyenne ou d'écart-type. 
# On travaille avec :
#Fréquence absolue Nombre d'observations par catégorie
#Proportion (%) Part relative de chaque catégorie
#Mode La catégorie la plus fréquente

variable = df['sex']

freq_abs  = variable.value_counts()
proportion = variable.value_counts(normalize=True) * 100
mode      = variable.mode()[0]

print(freq_abs)
print(proportion)
print(f"Mode : {mode}")

# Diagramme en barres
sns.countplot(x='sex', data=df, palette='Set2')
plt.title("Répartition du sexe des patients")
plt.show()

# Diagramme circulaire (pie chart)
df['sex'].value_counts().plot.pie(autopct='%1.1f%%')
plt.show()

#Bar plot vs Pie chart — quand choisir lequel ?
#Le bar plot est toujours recommandé quand il y a 3 catégories ou plus 
# : l'œil compare mieux les hauteurs que les angles.
#Le pie chart est acceptable seulement avec 2-3 catégories et
# quand les proportions sont très différentes.
# Il devient illisible avec beaucoup de catégories similaires.