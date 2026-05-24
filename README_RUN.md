# FocusCore — Instructions d'exécution rapide

Ce fichier complète `README.md` avec des instructions pratiques pour lancer le projet localement, des exemples d'appel API et des notes utiles.

## Backend (FastAPI)

1. Positionnez-vous dans le dossier backend :

```powershell
cd FocusCore\backend
```

2. (optionnel) activer votre virtualenv :

```powershell
# si vous avez créé un venv
& .\venv\Scripts\Activate.ps1
```

3. Installer les dépendances Python :

```powershell
pip install -r requirements.txt
```

4. (optionnel) générer le dataset si vous ne l'avez pas :

```powershell
python generate_dataset.py
```

5. Entraînement rapide (sans GridSearch) :

```powershell
python -c "from train import train; train(tune=False)"
```

6. Entraînement complet (avec GridSearch, peut être long) :

```powershell
python train.py
```

7. Lancer le serveur API :

```powershell
uvicorn main:app --reload --port 8000
```

- Docs interactives : http://localhost:8000/docs

## Frontend (React / Vite)

```powershell
cd ..\frontend\focuscore-ui
npm install
npm run dev
# Ouvrir http://localhost:5173
```

## Emplacement des modèles

- Si vous ne voulez pas réentraîner, placez `model.pkl` et `label_encoder.pkl` dans `FocusCore/backend/`.
- Le serveur FastAPI charge ces fichiers au démarrage.

## Exemples d'appel API

PowerShell (`Invoke-RestMethod`):

```powershell
$payload = @{ description = "Implémenter le module JWT"; category = "Deep Work"; urgency = 4; effort_hours = 2.0; goal_aligned = $true } | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/predict" -Method POST -ContentType "application/json" -Body $payload
```

curl :

```powershell
curl -X POST "http://localhost:8000/predict" -H "Content-Type: application/json" -d '{"description":"Implémenter le module JWT","category":"Deep Work","urgency":4,"effort_hours":2.0,"goal_aligned":true}'
```

## Comportements UI notables

- Le `Dashboard` bloque l'ajout d'une tâche classée `Faible` si des tâches `Haut` sont en attente (demande de confirmation).
- `SideBar` persistée via `localStorage` (clé `fc_sidebar`).
- Landing page : widget de démonstration live.

## Conseils rapides

- Utilisez `train(tune=False)` pour tests rapides.
- Vérifiez que `model.pkl` existe avant de lancer `uvicorn` si vous ne réentraînez pas.
- Pour production, pensez à Dockeriser et ajouter CI, gestion des secrets et monitoring.

---

Si vous voulez, je peux :

- intégrer ces sections directement dans `FocusCore/README.md`,
- générer un `docker-compose.yml` pour backend+frontend,
- ajouter un test minimal `pytest` pour l'endpoint `/predict`.

Dites-moi ce que vous préférez.
