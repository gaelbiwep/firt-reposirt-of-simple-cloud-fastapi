#!/usr/bin/env python3
"""
Script pour lancer MongoDB et FastAPI ensemble
"""

import subprocess
import time
import sys
import os
from pathlib import Path

def run_command(cmd, name):
    """Exécute une commande"""
    try:
        print(f"\n▶️ Démarrage de {name}...")
        if sys.platform == "win32":
            subprocess.Popen(cmd, shell=True)
        else:
            subprocess.Popen(cmd, shell=True)
        print(f"✅ {name} démarré!")
    except Exception as e:
        print(f"❌ Erreur lors du démarrage de {name}: {e}")
        return False
    return True

def check_mongodb():
    """Vérifie si MongoDB est accessible"""
    try:
        from pymongo import MongoClient
        client = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=2000)
        client.admin.command('ping')
        return True
    except:
        return False

def main():
    print("""
    ╔═══════════════════════════════════╗
    ║  FRIENDS API - MongoDB + FastAPI  ║
    ╚═══════════════════════════════════╝
    """)

    # Vérifie MongoDB
    print("🔍 Vérification de MongoDB...")
    
    # Une première vérification
    if not check_mongodb():
        print("📝 Démarrage du service MongoDB...")
        if sys.platform == "win32":
            subprocess.run(["powershell", "-Command", "mongod"], 
                         stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL)
        time.sleep(3)

    # Nouvelle tentative
    if check_mongodb():
        print("✅ MongoDB est connecté et prêt!")
    else:
        print("""
        ❌ Impossible de se connecter à MongoDB!
        
        Solutions:
        1️⃣ Installe MongoDB Community: https://www.mongodb.com/try/download/community
        2️⃣ Lance manuellement: mongod
        3️⃣ Ou vois le fichier MONGODB_SETUP.md
        """)
        input("Appuie sur Entrée pour quitter...")
        sys.exit(1)

    # Lance FastAPI
    print("""
    ╔══════════════════════════════════╗
    ║  🚀 Démarrage de FastAPI         ║
    ╚══════════════════════════════════╝
    
    📍 API URL:  http://localhost:8000
    📚 Docs:     http://localhost:8000/docs
    📊 ReDoc:    http://localhost:8000/redoc
    
    Appuie sur Ctrl+C pour arrêter
    """)

    try:
        subprocess.run([sys.executable, "main_mongodb.py"])
    except KeyboardInterrupt:
        print("\n\n👋 API arrêtée!")
        sys.exit(0)

if __name__ == "__main__":
    main()
