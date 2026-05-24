"""
generate_dataset.py
-------------------
Génère un dataset synthétique de 1500 tâches labellisées pour entraîner
le modèle de prédiction d'impact de FocusCore.

Règles métier :
  - Haut impact  : Deep Work + aligné objectif + effort > 1h
  - Moyen impact : Apprentissage / Communication / Créativité / urgence élevée
  - Faible impact: Admin / Perso + non aligné + effort < 30min

Un bruit de 10% simule l'ambiguïté réelle des données humaines.
"""

import random
import pandas as pd
import numpy as np

random.seed(42)
np.random.seed(42)

DESCRIPTIONS = {
    "Deep Work": [
        "Concevoir l'architecture du module d'authentification JWT",
        "Implémenter le pipeline de prétraitement des données textuelles",
        "Développer l'algorithme de scoring d'impact des tâches",
        "Refactoriser le module de gestion des utilisateurs",
        "Créer les endpoints REST pour la gestion des objectifs",
        "Intégrer le modèle ML dans l'API FastAPI",
        "Optimiser les requêtes SQL pour la table des tâches",
        "Concevoir le schéma de base de données avec les relations",
        "Développer le composant React du tableau de bord principal",
        "Implémenter la validation des données avec Pydantic",
        "Écrire les tests unitaires pour le module de scoring",
        "Mettre en place le système de cache avec Redis",
        "Configurer le pipeline CI/CD avec GitHub Actions",
        "Analyser les features importantes du modèle Random Forest",
        "Implémenter le système de notification en temps réel",
        "Concevoir l'interface de capture rapide des tâches",
        "Développer la logique de détection du bruit de fond",
        "Intégrer le système d'authentification OAuth2",
        "Optimiser les performances de rendu du frontend React",
        "Créer les visualisations analytiques avec Recharts",
        "Construire le modèle de prédiction de durée des tâches",
        "Implémenter le moteur de recommandation de priorités",
        "Développer le module d'export des données utilisateur",
        "Concevoir l'architecture microservices de l'application",
        "Écrire la logique de synchronisation des objectifs",
        "Refactoriser le module de traitement des événements asynchrones",
        "Concevoir le système de gestion des permissions multi-rôles",
        "Implémenter le module de détection d'anomalies dans les logs",
        "Développer l'algorithme de clustering des tâches similaires",
        "Construire le pipeline d'intégration continue avec tests automatisés",
        "Implémenter le système de pagination et filtrage avancé de l'API",
        "Créer le moteur de règles pour la détection du bruit de fond",
        "Développer le module de backup automatique de la base de données",
        "Optimiser le bundle Webpack pour réduire le temps de chargement",
        "Concevoir le système de gestion des sessions utilisateur sécurisées",
        "Implémenter le rate limiting sur les endpoints critiques de l'API",
        "Développer le module d'analyse des patterns de productivité",
        "Construire l'interface de configuration avancée du modèle ML",
        "Écrire les tests d'intégration pour le pipeline de prédiction",
        "Implémenter la gestion des erreurs globale avec logging structuré",
    ],
    "Admin": [
        "Répondre aux emails non urgents de la semaine",
        "Mettre à jour le fichier de suivi des dépenses mensuelles",
        "Remplir le formulaire d'inscription au stage",
        "Archiver les anciens documents de projet",
        "Mettre à jour le profil LinkedIn avec les nouvelles compétences",
        "Payer la facture internet du mois en cours",
        "Organiser et trier le dossier des téléchargements",
        "Nettoyer la boîte mail et supprimer les spams",
        "Renouveler l'abonnement à l'environnement de développement",
        "Imprimer les documents nécessaires pour la soutenance",
        "Réserver la salle de réunion pour vendredi prochain",
        "Compléter le rapport mensuel d'activités académiques",
        "Envoyer le compte-rendu de la dernière réunion",
        "Scanner et archiver les contrats et conventions",
        "Mettre à jour le tableau de bord des dépenses",
        "Classer les reçus et justificatifs dans le bon dossier",
        "Vérifier et corriger les erreurs dans le planning hebdomadaire",
        "Remplir le formulaire d'évaluation de fin de semestre",
        "Mettre à jour les informations de contact dans l'annuaire",
        "Transférer les anciens fichiers vers le nouveau cloud storage",
        "Renouveler les accès VPN expirés pour les collaborateurs",
        "Préparer le récapitulatif des heures travaillées du mois",
        "Mettre à jour les métadonnées des fichiers de documentation",
        "Soumettre la demande de remboursement des frais de déplacement",
        "Vérifier l'état des sauvegardes automatiques du serveur",
        "Compléter la fiche de suivi des livrables du projet",
        "Envoyer la liste de présence à l'administration",
        "Mettre à jour le registre des accès aux ressources partagées",
        "Rédiger le compte-rendu administratif du sprint terminé",
    ],
    "Communication": [
        "Préparer la démonstration du MVP pour les parties prenantes",
        "Présenter l'avancement du projet à l'équipe pédagogique",
        "Appeler le client pour valider les spécifications fonctionnelles",
        "Préparer les slides de soutenance du mini-projet IA",
        "Rédiger la documentation technique complète de l'API",
        "Présenter le prototype FocusCore lors de la soutenance",
        "Organiser une session de feedback avec les utilisateurs bêta",
        "Rédiger l'abstract du rapport de stage d'initiation",
        "Préparer un pitch de 3 minutes pour présenter HayTech",
        "Répondre aux questions du jury lors de la soutenance",
        "Envoyer le rapport d'avancement hebdomadaire au superviseur",
        "Animer la réunion de synchronisation avec les collaborateurs",
        "Préparer le rapport final de soutenance IA-Indus-4.0",
        "Rédiger le guide utilisateur de l'application FocusCore",
        "Organiser la démonstration live du modèle ML devant le jury",
        "Présenter les métriques de performance du Random Forest",
        "Rédiger la section résultats et discussion du rapport",
        "Préparer la FAQ pour l'utilisation de l'API publique",
        "Créer une vidéo de démo de 2 minutes pour le portfolio",
        "Rédiger les commentaires de code pour la revue technique",
        "Préparer le backlog présenté lors de la réunion de sprint",
        "Animer le workshop de présentation des nouvelles features",
        "Rédiger le post LinkedIn annonçant la sortie du projet",
        "Préparer les notes de version pour le release v2.0",
        "Rédiger le rapport de stage complet avec méthodologie",
        "Préparer la présentation des résultats de benchmark du modèle",
        "Animer la session de démo pour les étudiants du module",
    ],
    "Apprentissage": [
        "Lire la documentation officielle de scikit-learn sur Random Forest",
        "Suivre le tutoriel avancé FastAPI sur la gestion des middlewares",
        "Étudier les techniques de feature engineering pour le NLP",
        "Regarder le cours en ligne sur les transformers de Hugging Face",
        "Lire l'article de recherche sur la méthode d'Eisenhower appliquée",
        "Pratiquer les exercices Python sur les séries temporelles",
        "Étudier les design patterns d'architecture microservices",
        "Revoir les fondamentaux du machine learning supervisé",
        "Lire la documentation React sur les hooks avancés useReducer",
        "Suivre le tutoriel sur Docker et la containerisation d'applications",
        "Étudier les métriques d'évaluation des modèles de classification",
        "Lire la documentation Pydantic pour la validation des données",
        "Comprendre les principes du Transfer Learning en NLP",
        "Étudier les techniques d'optimisation GridSearchCV et RandomizedSearch",
        "Lire la documentation sur les pipelines sklearn avancés",
        "Suivre le cours sur le déploiement de modèles ML avec Docker",
        "Étudier les méthodes d'interprétabilité SHAP et LIME",
        "Pratiquer les exercices de data augmentation pour texte",
        "Lire l'article sur les Random Forests et leur variance",
        "Étudier les patterns d'architecture Clean Architecture en Python",
        "Suivre le cours sur le testing avancé avec pytest et fixtures",
        "Comprendre les principes du cross-validation stratifié",
        "Étudier les techniques de gestion mémoire pour les grands datasets",
        "Lire la documentation PostgreSQL sur les indexes composites",
        "Suivre le workshop sur les bonnes pratiques Git Flow",
        "Comprendre les algorithmes de détection d'outliers statistiques",
        "Étudier les fondamentaux du traitement du langage naturel",
        "Lire le paper sur l'architecture BERT et ses applications",
    ],
    "Perso": [
        "Nettoyer et réorganiser l'espace de travail physique",
        "Faire une séance de sport pour maintenir l'énergie",
        "Préparer les repas de la semaine pour gagner du temps",
        "Appeler la famille pour prendre des nouvelles",
        "Lire un chapitre du livre de développement personnel en cours",
        "Méditer 10 minutes pour clarifier les priorités du lendemain",
        "Ranger et organiser la chambre et le bureau",
        "Faire les courses de la semaine en une seule fois",
        "Prendre une courte pause de 20 minutes pour recharger",
        "Rédiger les objectifs personnels du trimestre suivant",
        "Faire un bilan de la semaine dans le journal de bord",
        "Organiser une sortie pour décompresser après la soutenance",
    ],
    "Créativité": [
        "Concevoir la charte graphique et le système de couleurs de l'app",
        "Créer les maquettes UI/UX du tableau de bord avec Figma",
        "Imaginer et esquisser les icônes personnalisées pour les catégories",
        "Rédiger le naming et le positionnement de marque du produit",
        "Concevoir les micro-animations d'interface pour améliorer l'UX",
        "Créer un prototype interactif de la landing page en Figma",
        "Rédiger le storytelling du projet pour la présentation finale",
        "Concevoir un logo original pour FocusCore en SVG",
        "Idéer les nouvelles fonctionnalités pour la roadmap v3.0",
        "Rédiger un article de blog technique sur le projet FocusCore",
        "Créer une illustration vectorielle pour la page d'accueil",
        "Concevoir la palette de couleurs du mode clair de l'application",
        "Brainstormer les use cases innovants pour l'IA de productivité",
        "Rédiger les user stories créatives pour les personas utilisateurs",
        "Concevoir l'architecture de l'expérience utilisateur de l'onboarding",
        "Créer un motion design pour la présentation de soutenance",
        "Imaginer le concept de gamification pour la gestion des tâches",
        "Rédiger le manifeste produit et les valeurs de FocusCore",
        "Concevoir les templates de visualisation des données analytiques",
        "Créer les assets visuels pour le portfolio de projet académique",
    ],
}

CATEGORIES = list(DESCRIPTIONS.keys())

# Poids normalisés — somme = 1.0
CATEGORY_WEIGHTS = [0.28, 0.20, 0.17, 0.15, 0.10, 0.10]

PREFIXES = [
    "Finaliser ", "Revoir ", "Améliorer ", "Compléter ", "Mettre à jour ",
    "Tester ", "Valider ", "Corriger ", "Nettoyer ", "Préparer ",
]


def compute_impact_score(category: str, urgency: int, effort_hours: float, goal_aligned: bool) -> int:
    score = 0
    cat_scores = {
        "Deep Work":     40,
        "Créativité":    28,
        "Apprentissage": 22,
        "Communication": 18,
        "Admin":          5,
        "Perso":          0,
    }
    score += cat_scores.get(category, 0)
    if goal_aligned:
        score += 30
    if effort_hours >= 2.0:
        score += 18
    elif effort_hours >= 1.0:
        score += 12
    elif effort_hours >= 0.5:
        score += 6
    score += (urgency - 1) * 3
    return min(score, 100)


def classify(score: int) -> str:
    if score >= 60:
        return "Haut"
    elif score >= 30:
        return "Moyen"
    return "Faible"


def generate_dataset(n_samples: int = 1500, noise_rate: float = 0.10) -> pd.DataFrame:
    rows = []

    for _ in range(n_samples):
        category = random.choices(CATEGORIES, weights=CATEGORY_WEIGHTS)[0]

        description = random.choice(DESCRIPTIONS[category])
        if random.random() < 0.25:
            prefix = random.choice(PREFIXES)
            description = prefix + description[0].lower() + description[1:]

        urgency = random.choices([1, 2, 3, 4, 5], weights=[0.12, 0.28, 0.32, 0.18, 0.10])[0]

        effort_ranges = {
            "Deep Work":     (0.5, 4.0),
            "Communication": (0.5, 2.5),
            "Apprentissage": (0.5, 2.0),
            "Admin":         (0.1, 0.8),
            "Perso":         (0.1, 1.0),
            "Créativité":    (0.5, 3.0),
        }
        low, high = effort_ranges[category]
        effort_hours = round(random.uniform(low, high), 1)

        goal_probs = {
            "Deep Work":     0.78,
            "Communication": 0.65,
            "Créativité":    0.60,
            "Apprentissage": 0.55,
            "Admin":         0.18,
            "Perso":         0.08,
        }
        goal_aligned = random.random() < goal_probs[category]

        score = compute_impact_score(category, urgency, effort_hours, goal_aligned)
        impact_class = classify(score)

        # Bruit réaliste réduit à 10%
        if random.random() < noise_rate:
            impact_class = random.choice(["Haut", "Moyen", "Faible"])

        rows.append({
            "description": description,
            "category": category,
            "urgency": urgency,
            "effort_hours": effort_hours,
            "goal_aligned": int(goal_aligned),
            "impact_class": impact_class,
        })

    df = pd.DataFrame(rows)

    print(f"\n{'='*50}")
    print(f"Dataset généré — {len(df)} exemples")
    print("="*50)
    print("\nDistribution des classes d'impact :")
    for cls, count in df["impact_class"].value_counts().items():
        bar = "█" * (count // 15)
        print(f"  {cls:<8} {count:>5} ({count/len(df)*100:.1f}%)  {bar}")

    print("\nDistribution des catégories :")
    for cat, count in df["category"].value_counts().items():
        bar = "█" * (count // 10)
        print(f"  {cat:<16} {count:>5} ({count/len(df)*100:.1f}%)  {bar}")

    return df


if __name__ == "__main__":
    df = generate_dataset(n_samples=1500, noise_rate=0.10)
    df.to_csv("tasks_dataset.csv", index=False)
    print("\nFichier sauvegardé : tasks_dataset.csv")
