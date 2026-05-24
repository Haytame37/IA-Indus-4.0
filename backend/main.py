"""
main.py
-------
Serveur FastAPI qui charge le modèle ML entraîné et expose
un endpoint /predict pour scorer l'impact d'une tâche en temps réel.

Usage :
    uvicorn main:app --reload --port 8000

Docs interactives : http://localhost:8000/docs
"""

import json
from contextlib import asynccontextmanager
from typing import Literal

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# ------------------------------------------------------------------
# Types — Créativité ajoutée comme 6ème catégorie
# ------------------------------------------------------------------
CategoryType = Literal["Deep Work", "Admin", "Communication", "Apprentissage", "Perso", "Créativité"]
ImpactClass = Literal["Haut", "Moyen", "Faible"]

# Score de base par classe (centre de la plage)
CLASS_BASE_SCORES: dict[str, int] = {"Haut": 85, "Moyen": 55, "Faible": 15}

# ------------------------------------------------------------------
# Chargement du modèle au démarrage (pattern lifespan FastAPI)
# ------------------------------------------------------------------
ml_models: dict = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Charge le modèle une seule fois au démarrage du serveur."""
    try:
        ml_models["pipeline"] = joblib.load("model.pkl")
        ml_models["label_encoder"] = joblib.load("label_encoder.pkl")
        with open("metrics.json", encoding="utf-8") as f:
            ml_models["metrics"] = json.load(f)
        print("Modèle chargé avec succès.")
        print(f"Classes d'impact : {list(ml_models['pipeline'].classes_)}")
    except FileNotFoundError as e:
        raise RuntimeError(
            f"Fichier introuvable : {e}. Lance d'abord generate_dataset.py puis train.py."
        )
    yield
    ml_models.clear()


# ------------------------------------------------------------------
# Application
# ------------------------------------------------------------------
app = FastAPI(
    title="FocusCore ML API",
    description="Prédiction de l'impact d'une tâche via Random Forest (6 catégories).",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ------------------------------------------------------------------
# Schémas Pydantic
# ------------------------------------------------------------------
class TaskInput(BaseModel):
    description: str = Field(
        ...,
        min_length=3,
        max_length=500,
        examples=["Implémenter le module d'authentification JWT"],
    )
    category: CategoryType = Field(..., examples=["Deep Work"])
    urgency: int = Field(..., ge=1, le=5, examples=[3])
    effort_hours: float = Field(..., ge=0.1, le=24.0, examples=[2.0])
    goal_aligned: bool = Field(..., examples=[True])


class PredictionResponse(BaseModel):
    impact_class: ImpactClass
    impact_score: int = Field(..., ge=0, le=100)
    confidence: float = Field(..., ge=0.0, le=1.0)
    probabilities: dict[str, float]
    explanation: str


class HealthResponse(BaseModel):
    status: str
    model: str
    version: str
    accuracy: float
    f1_macro: float
    classes: list[str]


# ------------------------------------------------------------------
# Logique de prédiction
# ------------------------------------------------------------------
def build_explanation(task: TaskInput, impact_class: str, confidence: float) -> str:
    """Génère une explication lisible de la prédiction."""
    reasons = []

    if task.category == "Deep Work":
        reasons.append("travail de concentration profonde")
    elif task.category == "Créativité":
        reasons.append("travail créatif à haute valeur")  # Créativité
    if task.goal_aligned:
        reasons.append("aligné sur l'objectif actif")
    if task.urgency >= 4:
        reasons.append("échéance urgente")
    if task.effort_hours >= 2.0:
        reasons.append("effort significatif (≥2h)")
    if not task.goal_aligned and task.category in ("Admin", "Perso"):
        reasons.append("non lié à l'objectif principal")

    level = {"Haut": "fort", "Moyen": "moyen", "Faible": "faible"}[impact_class]
    base = f"Impact {level} prédit avec {confidence*100:.0f}% de confiance"

    if reasons:
        return base + " — " + ", ".join(reasons) + "."
    return base + "."


# ------------------------------------------------------------------
# Endpoints
# ------------------------------------------------------------------
@app.post("/predict", response_model=PredictionResponse, tags=["ML"])
def predict(task: TaskInput):
    """
    Prédit la classe d'impact d'une tâche (Haut / Moyen / Faible)
    et retourne le score numérique, la confiance et une explication.
    Supporte 6 catégories : Deep Work, Admin, Communication,
    Apprentissage, Perso, Créativité.
    """
    pipeline = ml_models.get("pipeline")
    le = ml_models.get("label_encoder")

    if pipeline is None:
        raise HTTPException(status_code=503, detail="Modèle non chargé.")

    try:
        category_enc = int(le.transform([task.category])[0])

        X = pd.DataFrame([{
            "description": task.description,
            "category_enc": category_enc,
            "urgency": task.urgency,
            "effort_hours": task.effort_hours,
            "goal_aligned": int(task.goal_aligned),
        }])

        impact_class: str = pipeline.predict(X)[0]
        proba_array = pipeline.predict_proba(X)[0]
        classes: list[str] = list(pipeline.classes_)

        probabilities = {
            cls: round(float(p), 3)
            for cls, p in zip(classes, proba_array)
        }
        confidence = round(float(max(proba_array)), 3)

        # Score numérique : base de la classe + ajustement par confiance
        base = CLASS_BASE_SCORES[impact_class]
        adjustment = int((confidence - 0.6) * 25)
        impact_score = max(0, min(100, base + adjustment))

        return PredictionResponse(
            impact_class=impact_class,
            impact_score=impact_score,
            confidence=confidence,
            probabilities=probabilities,
            explanation=build_explanation(task, impact_class, confidence),
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de prédiction : {str(e)}")


@app.get("/health", response_model=HealthResponse, tags=["Système"])
def health():
    """Vérifie que l'API est opérationnelle et retourne les métriques du modèle."""
    metrics = ml_models.get("metrics", {})
    pipeline = ml_models.get("pipeline")

    return HealthResponse(
        status="ok",
        model="RandomForestClassifier",
        version="2.0.0",
        accuracy=metrics.get("accuracy", 0.0),
        f1_macro=metrics.get("f1_macro", 0.0),
        classes=list(pipeline.classes_) if pipeline else [],
    )


@app.get("/", tags=["Système"])
def root():
    return {
        "message": "FocusCore ML API",
        "version": "2.0.0",
        "docs": "/docs",
        "predict_endpoint": "POST /predict",
        "categories": ["Deep Work", "Admin", "Communication", "Apprentissage", "Perso", "Créativité"],
    }
