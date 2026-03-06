@echo off
REM Script pour démarrer MongoDB et FastAPI sur Windows

echo.
echo ================================
echo   FRIENDS API - MongoDB Setup
echo ================================
echo.

REM Vérifie si MongoDB est installé
echo Vérification de MongoDB...
mongod --version >nul 2>&1

if %errorlevel% neq 0 (
    echo.
    echo ❌ MongoDB n'est pas installé!
    echo.
    echo Télécharge MongoDB Community Edition:
    echo https://www.mongodb.com/try/download/community
    echo.
    pause
    exit /b 1
)

echo ✅ MongoDB trouvé!
echo.

REM Lance MongoDB en arrière-plan
echo Démarrage de MongoDB...
start "MongoDB" mongod
timeout /t 2

REM Attends que MongoDB soit prêt
echo Vérification de la connexion à MongoDB...
mongosh --eval "db.adminCommand('ping')" >nul 2>&1

if %errorlevel% neq 0 (
    echo.
    echo ⏳ MongoDB se lance... (attendre 5 secondes)
    timeout /t 5
)

echo ✅ MongoDB est prêt!
echo.

REM Lance l'API FastAPI
echo Démarrage de FastAPI...
echo.
echo 🚀 L'API démarre sur http://localhost:8000
echo 📚 Docs disponibles sur http://localhost:8000/docs
echo.
echo Appuie sur Ctrl+C pour arrêter
echo.

python main_mongodb.py
