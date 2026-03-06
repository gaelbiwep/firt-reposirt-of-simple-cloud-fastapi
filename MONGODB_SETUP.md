# Configuration MongoDB Local pour FastAPI

## 📋 Prérequis

Assure-toi que **MongoDB** est installé sur ta machine.

### 1️⃣ Installer MongoDB Community Edition

**Sur Windows:**
- Télécharge MongoDB Community Edition: https://www.mongodb.com/try/download/community
- Lance l'installateur `.msi`
- MongoDB s'installe par défaut dans: `C:\Program Files\MongoDB\Server\7.0\`

**Ou via Chocolatey:**
```bash
choco install mongodb-community
```

### 2️⃣ Vérifier l'installation

```bash
mongod --version
```

---

## 🚀 Lancer MongoDB en local

### Option 1: Démarrer le service MongoDB (recommandé)

**Sur Windows:**
```bash
# MongoDB démarre automatiquement après installation
# Vérifie que le service est actif:
Get-Service -Name "MongoDB" | Get-Service
```

### Option 2: Lancer MongoDB manuellement

```bash
# Accès au dossier MongoDB
cd "C:\Program Files\MongoDB\Server\7.0\bin"

# Lance MongoDB
mongod
```

**Output attendu:**
```
[initandlisten] waiting for connections on port 27017
```

✅ MongoDB tourne maintenant sur `mongodb://localhost:27017`

---

## 🔌 Tester la connexion

### Via MongoDB Compass (GUI)

1. **Télécharge MongoDB Compass**: https://www.mongodb.com/products/tools/compass
2. Lance Compass
3. Clique **Connect** (la connexion locale est par défaut)
4. Tu devrais voir la database **friends_db** 

### Via terminal mongosh

```bash
# Si mongosh est installé
mongosh

# Dans le shell MongoDB:
> show dbs
> use friends_db
> db.personnes.find()
```

---

## 🎯 Utiliser avec FastAPI

### 1️⃣ Assure-toi que MongoDB tourne

```bash
mongod
```

### 2️⃣ Lance l'API FastAPI

```bash
python main_mongodb.py
```

**Output attendu:**
```
✅ Connecté à MongoDB!
📝 Ajout des données de test...
✅ 3 personnes ajoutées à la base de données
```

### 3️⃣ Teste l'API

```bash
# Récupère toutes les personnes
curl http://localhost:8000/personnes

# Récupère les stats
curl http://localhost:8000/stats

# Crée une personne
curl -X POST http://localhost:8000/personnes \
  -H "Content-Type: application/json" \
  -d '{
    "nom": "Dupuis",
    "prenom": "Alice",
    "genre": "F",
    "age": 23,
    "couleur_preferee": "vert",
    "ville": "Marseille",
    "code_postal": "13000"
  }'
```

---

## 📊 Visualiser les données

### Option 1: MongoDB Compass (GUI facile)

1. Télécharge et ouvre [MongoDB Compass](https://www.mongodb.com/products/tools/compass)
2. Tu verras automatiquement `friends_db` et la collection `personnes`

### Option 2: Terminal mongosh

```bash
mongosh

# Voir toutes les databases
> show dbs

# Utiliser la database
> use friends_db

# Voir les collections
> show collections

# Voir tous les documents
> db.personnes.find()

# Voir un document avec format lisible
> db.personnes.find().pretty()

# Quitter
> exit
```

---

## 🔧 Configuration (si nécessaire)

Si tu dois changer l'URL MongoDB dans le code:

**Fichier: `main_mongodb.py` ligne 13**

```python
# Par défaut (localhost):
MONGODB_URL = "mongodb://localhost:27017"

# Ou avec authentification:
MONGODB_URL = "mongodb://username:password@localhost:27017"
```

---

## 🐛 Troubleshooting

### ❌ Erreur: "Connection refused"
- **Solution**: Lance le service MongoDB avec `mongod`

### ❌ Erreur: "MongoClient error"
- **Solution**: Installe `pymongo` avec `pip install pymongo`

### ❌ Port 27017 déjà utilisé
```bash
# Trouve le processus qui utilise le port
netstat -ano | findstr :27017

# Tue le processus (remplace PID)
taskkill /PID [PID] /F

# Ou change le port dans mongod:
mongod --port 27018
```

---

## 📝 Note importante

Cette API **stocke les données** dans MongoDB, contrairement à la version en mémoire (`test_main_v1.py`).

✅ Les données **persistent** même après redémarrage de l'API
❌ Les données en mémoire sont perdues au redémarrage
