# FocusCore v2.0 — Gestionnaire de tâches piloté par l'IA

> Mini-projet académique **IA-Indus-4.0**
> Stack : FastAPI · scikit-learn · Random Forest · React · Vite · react-router-dom

---

## Structure du projet

```
focuscore/
├── backend/
│   ├── generate_dataset.py   — 1500 tâches synthétiques, 6 catégories
│   ├── train.py              — Pipeline sklearn + GridSearchCV (RF 200–300 arbres)
│   ├── main.py               — API FastAPI /predict + /health
│   └── requirements.txt
└── frontend/focuscore-ui/
    └── src/
        ├── main.jsx           — BrowserRouter (react-router-dom)
        ├── App.jsx            — Routes : / → Landing, /app → Dashboard
        ├── LandingPage.jsx    — Landing page avec hero + démo live + how-it-works
        ├── SideBar.jsx        — Sidebar collapsible (localStorage fc_sidebar)
        └── Dashboard.jsx      — Dashboard principal, vraie API, 6 catégories
```

---

## Lancement

### 1. Backend — entraîner le modèle

```bash
cd backend
pip install -r requirements.txt

python generate_dataset.py    # génère tasks_dataset.csv (1500 lignes)
python train.py               # entraîne → model.pkl + label_encoder.pkl + metrics.json
uvicorn main:app --reload --port 8000
```

### 2. Frontend

```bash
cd frontend/focuscore-ui
npm install                   # installe react-router-dom et les autres dépendances
npm run dev                   # http://localhost:5173
```

---

## Catégories d'impact

| Catégorie       | Score base | Poids dataset | Alignement obj. |
|-----------------|-----------|---------------|-----------------|
| Deep Work       | 40        | 28%           | 78%             |
| Créativité      | 28        | 10%           | 60%             |
| Apprentissage   | 22        | 15%           | 55%             |
| Communication   | 18        | 17%           | 65%             |
| Admin           | 5         | 20%           | 18%             |
| Perso           | 0         | 10%           | 8%              |

## API — Endpoint principal

```http
POST http://localhost:8000/predict
Content-Type: application/json

{
  "description": "Implémenter le module JWT",
  "category": "Deep Work",
  "urgency": 4,
  "effort_hours": 2.0,
  "goal_aligned": true
}
```

Réponse :
```json
{
  "impact_class": "Haut",
  "impact_score": 88,
  "confidence": 0.91,
  "probabilities": { "Haut": 0.91, "Moyen": 0.07, "Faible": 0.02 },
  "explanation": "Impact fort prédit avec 91% de confiance — travail de concentration profonde, aligné sur l'objectif actif."
}
```

---

## Routes frontend

| Route  | Composant      | Description                        |
|--------|----------------|------------------------------------|
| `/`    | LandingPage    | Hero, démo live, features, CTA     |
| `/app` | Dashboard      | Formulaire + liste + sidebar       |
