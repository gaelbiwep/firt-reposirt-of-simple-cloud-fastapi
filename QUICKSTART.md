# 📱 FastAPI avec MongoDB - Guide Complet

## 📂 Fichiers du projet

| Fichier | Description |
|---------|-------------|
| `test_main_v1.py` | Version en mémoire (données perdues au redémarrage) |
| `main_mongodb.py` | **NOUVELLE VERSION avec MongoDB** ✅ |
| `requirements.txt` | Dépendances Python |
| `MONGODB_SETUP.md` | Guide détaillé MongoDB |
| `start_api.py` | Script Python pour lancer tout |
| `start_api.bat` | Script Windows pour lancer tout |
| `index.html` | Testeur web interactif |

---

## 🚀 Démarrage rapide (3 étapes)

### 1️⃣ Installer MongoDB

**Windows (le plus simple):**
- Télécharge: https://www.mongodb.com/try/download/community
- Lance le `.msi` et suit les étapes
- MongoDB démarre automatiquement après installation ✅

**Ou via PowerShell:**
```powershell
choco install mongodb-community
```

### 2️⃣ Vérifier MongoDB tourne

```bash
mongod
```

**Attendu:**
```
[initandlisten] waiting for connections on port 27017
```

Laisse cette fenêtre ouverte! 

### 3️⃣ Lancer l'API

**Option A - En Python:**
```bash
cd c:\test\test_fastapi_cloud
python main_mongodb.py
```

**Option B - Avec le script:**
```bash
python start_api.py
```

**Output attendu:**
```
✅ Connecté à MongoDB!
📝 Ajout des données de test...
✅ 3 personnes ajoutées à la base de données
```

---

## 🔗 Accéder à l'API

### Dans le navigateur:

- **Accueil** → http://localhost:8000
- **Docs interactives** → http://localhost:8000/docs ⭐ (Recommandé)
- **ReDoc** → http://localhost:8000/redoc
- **Testeur Web** → Ouvre `index.html` dans ton navigateur

### En ligne de commande (curl):

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
    "ville": "Marseille"
  }'
```

---

## 📊 Visualiser les données MongoDB

### Via MongoDB Compass (GUI - le plus facile)

1. Télécharge: https://www.mongodb.com/products/tools/compass
2. Lance Compass
3. Clique **Connect**
4. Tu vois: `localhost:27017` → `friends_db` → `personnes`

### Via terminal mongosh

```bash
mongosh

# Dans le shell:
> show dbs
> use friends_db
> db.personnes.find()
> db.personnes.find().pretty()
> exit
```

---

## 🔄 Différences: En mémoire vs MongoDB

| Feature | En mémoire | MongoDB |
|---------|-----------|---------|
| Fichier | `test_main_v1.py` | `main_mongodb.py` |
| Données persistent | ❌ Non | ✅ Oui |
| Redémarrage | Les données disparaissent | Les données restent |
| Performance | Rapide (petit dataset) | Rapide (gros dataset) |
| Cloud-ready | ⚠️ Non | ✅ Oui |
| Point de vue production | Non | ✅ Recommandé |

---

## 🎯 Prochaines étapes

### Pour déployer sur le cloud:

**Azure Cosmos DB (MongoDB API):**
```bash
# 1. Créer une ressource Cosmos DB
az cosmosdb create \
  --name friends-api \
  --resource-group ma-ressource \
  --kind MongoDB

# 2. Récupérer la connection string
az cosmosdb keys list --name friends-api

# 3. Mettre à jour main_mongodb.py
MONGODB_URL = "mongodb+srv://..."
```

**MongoDB Atlas (Cloud gratuit):**
```bash
# Via https://www.mongodb.com/cloud/atlas
# Crée un cluster gratuit
# Récupère la connection string
# Mets à jour: MONGODB_URL = "mongodb+srv://..."
```

---

## 🐛 Troubleshooting

### ❌ `Connection refused on 27017`
```bash
# Lance MongoDB:
mongod
```

### ❌ `ModuleNotFoundError: No module named 'pymongo'`
```bash
pip install pymongo
```

### ❌ `Port 27017 already in use`
```bash
# Tue le processus ancien:
taskkill /IM mongod.exe

# Ou change le port dans main_mongodb.py:
MONGODB_URL = "mongodb://localhost:27018"
```

### ❌ Les données ne s'enregistrent pas
1. Vérifie que MongoDB tourne: `mongod`
2. Vérifie que tu utilises `main_mongodb.py` (pas `test_main_v1.py`)
3. Regarde dans MongoDB Compass

---

## 📝 Structure du code

### Models Pydantic
```python
class Personne(BaseModel):
    id: Optional[str]  # _id de MongoDB
    nom: str
    prenom: str
    genre: str  # "M" ou "F"
    age: int
    couleur_preferee: str
    ville: str
    code_postal: Optional[str]
    amis_ids: List[str]  # ObjectIds des amis
    date_creation: Optional[str]
```

### Endpoints disponibles
```
GET    /                              # Infos API
GET    /personnes                      # Lister (filtres optionnels)
GET    /personnes/{id}                 # Obtenir une personne
POST   /personnes                      # Créer
PUT    /personnes/{id}                 # Modifier
DELETE /personnes/{id}                 # Supprimer
POST   /personnes/{id}/ajouter-ami/{ami_id}  # Ajouter ami
GET    /personnes/{id}/amis            # Voir les amis
GET    /stats                          # Statistiques
```

---

## 🌍 Déploiement (Optionnel)

### Render.com (gratuit):
```bash
# 1. Push sur GitHub
git push

# 2. Connecte Render.com
# 3. Utilise MongoDB Atlas pour la DB
```

### Railway (gratuit):
```bash
# railway login
# railway link
# railway up
```

### Vercel + Serverless:
Plus complexe, nécessite une refactor

---

## 📚 Ressources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [MongoDB](https://www.mongodb.com/)
- [PyMongo](https://pymongo.readthedocs.io/)
- [Azure Cosmos DB](https://azure.microsoft.com/services/cosmos-db/)

---

**Besoin d'aide?** Vois `MONGODB_SETUP.md` pour plus de détails! 🚀
