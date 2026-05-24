@echo off
title FocusCore - Demarrage

echo.
echo  =============================================
echo    FOCUSCORE - Demarrage automatique
echo  =============================================
echo.

:: ── Verifier Python ──────────────────────────────────────
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python non trouve. Installe Python 3.10+ depuis python.org
    pause
    exit /b
)

:: ── Verifier Node ────────────────────────────────────────
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Node.js non trouve. Installe Node.js depuis nodejs.org
    pause
    exit /b
)

:: ── Backend ──────────────────────────────────────────────
echo [1/4] Creation de l'environnement Python...
cd /d "%~dp0backend"

if not exist "venv\" (
    python -m venv venv
    echo     Environnement cree.
) else (
    echo     Environnement existant detecte.
)

echo [2/4] Installation des dependances Python...
call venv\Scripts\activate.bat
pip install -r requirements.txt -q

echo [3/4] Generation du dataset et entrainement du modele...
if not exist "model.pkl" (
    python generate_dataset.py
    python train.py
    echo     Modele entraine et sauvegarde.
) else (
    echo     Modele deja entraine, on passe.
)

echo [4/4] Lancement du backend et du frontend...
echo.
echo  Backend  : http://localhost:8000
echo  Frontend : http://localhost:5173
echo  API docs : http://localhost:8000/docs
echo.
echo  Ferme cette fenetre pour tout arreter.
echo.

:: Lance le backend dans ce terminal
start "FocusCore Backend" cmd /k "cd /d %~dp0backend && venv\Scripts\activate && uvicorn main:app --reload --port 8000"

:: Lance le frontend dans un nouveau terminal
start "FocusCore Frontend" cmd /k "cd /d %~dp0frontend\focuscore-ui && npm install -q && npm run dev"

:: Attend 4 secondes puis ouvre le navigateur
timeout /t 4 /nobreak >nul
start http://localhost:5173

echo Navigateur ouvert sur http://localhost:5173
pause
