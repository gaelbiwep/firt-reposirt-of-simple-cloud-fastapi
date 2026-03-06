from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId

# ============= CONNEXION MONGODB =============

# Configuration MongoDB locale
MONGODB_URL = "mongodb://localhost:27017"
DATABASE_NAME = "friends_db"
COLLECTION_NAME = "personnes"

# Connexion à MongoDB
try:
    client = MongoClient(MONGODB_URL)
    # Teste la connexion
    client.admin.command('ping')
    print("✅ Connecté à MongoDB!")
except Exception as e:
    print(f"❌ Erreur de connexion MongoDB: {e}")
    print("Assure-toi que MongoDB est lancé: mongod")

db = client[DATABASE_NAME]
personnes_collection = db[COLLECTION_NAME]

# Initialisation de l'app FastAPI
app = FastAPI(title="FRIENDS API MongoDB", description="API pour gérer les personnes avec MongoDB")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============= MODELS DE DONNEES =============

class Personne(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    nom: str
    prenom: str
    genre: str  # "M" ou "F"
    age: int
    couleur_preferee: str
    ville: str
    code_postal: Optional[str] = None
    amis_ids: List[str] = []
    date_creation: Optional[str] = None

    class Config:
        populate_by_name = True
        

class PersonneUpdate(BaseModel):
  id: Optional[str] = Field(default=None, alias="_id")
  nom: str
  prenom: str
  genre: str
  age: int
  couleur_preferee: str
  ville: str
  code_postal: Optional[str] = None


class PersonneCreate(BaseModel):
    #id: Optional[str] = Field(default=None, alias="_id")
    nom: str
    prenom: str
    genre: str
    age: int
    couleur_preferee: str
    ville: str
    code_postal: Optional[str] = None

# ============= FONCTIONS UTILITAIRES =============

def personne_helper(personne) -> dict:
    """Convertit un document MongoDB en dictionnaire Pydantic"""
    return {
        "_id": str(personne["_id"]),
        "nom": personne["nom"],
        "prenom": personne["prenom"],
        "genre": personne["genre"],
        "age": personne["age"],
        "couleur_preferee": personne["couleur_preferee"],
        "ville": personne["ville"],
        "code_postal": personne.get("code_postal"),
        "amis_ids": [str(ami_id) if isinstance(ami_id, ObjectId) else ami_id for ami_id in personne.get("amis_ids", [])],
        "date_creation": personne.get("date_creation"),
    }

# ============= ENDPOINTS =============

@app.on_event("startup")
async def startup_event():
    """Au démarrage, ajoute des données de test si la collection est vide"""
    count = personnes_collection.count_documents({})
    if count == 0:
        print("📝 Ajout des données de test...")
        donnees_test = [
            {
                "nom": "Dupont",
                "prenom": "Marie",
                "genre": "F",
                "age": 25,
                "couleur_preferee": "rose",
                "ville": "Paris",
                "code_postal": "75001",
                "amis_ids": [],
                "date_creation": datetime.now().isoformat()
            },
            {
                "nom": "Martin",
                "prenom": "Jean",
                "genre": "M",
                "age": 26,
                "couleur_preferee": "bleu",
                "ville": "Lyon",
                "code_postal": "69000",
                "amis_ids": [],
                "date_creation": datetime.now().isoformat()
            },
            {
                "nom": "Bernard",
                "prenom": "Sophie",
                "genre": "F",
                "age": 24,
                "couleur_preferee": "violet",
                "ville": "Paris",
                "code_postal": "75002",
                "amis_ids": [],
                "date_creation": datetime.now().isoformat()
            },
        ]
        result = personnes_collection.insert_many(donnees_test)
        print(f"✅ {len(result.inserted_ids)} personnes ajoutées à la base de données")
@app.get("/")
async def welcome_message():
    """Route d'accueil"""
    count = personnes_collection.count_documents({})
    return {
        "message": "Bienvenue sur FRIENDS API avec MongoDB",
        "version": "1.0.2",
        "status": "✅ MongoDB connecté",
        "total_persons": count,
        "endpoints": {
            "GET /personnes/all_personnes/": "Récupère toutes les personnes",
            "GET /personnes/person_by_id/{id}": "Récupère une personne par ID",
            "POST /personnes/create/": "Crée une nouvelle personne",
            "PUT /personnes/update/{id}": "Met à jour une personne",
            "DELETE /personnes/delete/{id}": "Supprime une personne",
            "POST /personnes/{id}/ajouter-ami/{ami_id}": "Ajoute un ami",
            "GET /personnes/{id}/amis": "Récupère les amis",
        }
    }

@app.get("/personnes/all_personnes/", response_model=List[Personne])
async def get_all_personnes():
    """
    Récupère toutes les personnes.
    """
    personnes = []
    for personne in personnes_collection.find():
        personnes.append(personne_helper(personne))
    return personnes

@app.get("/personnes/person_by_id/{personne_id}", response_model=Personne)
async def get_personne(personne_id: str):
    """Récupère une personne par son ID"""
    try:
        personne = personnes_collection.find_one({"_id": ObjectId(personne_id)})
        if not personne:
            raise HTTPException(status_code=404, detail="Personne non trouvée")
        return personne_helper(personne)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"ID invalide: {str(e)}")

@app.post("/personnes/create/", response_model=Personne)
async def create_personne(personne: PersonneCreate):
    """Crée une nouvelle personne"""
    nouvelle_personne = {
        "nom": personne.nom.title(),
        "prenom": personne.prenom.title(),
        "genre": personne.genre.upper(),
        "age": personne.age,
        "couleur_preferee": personne.couleur_preferee,
        "ville": personne.ville,
        "code_postal": personne.code_postal,
        "amis_ids": [],
        "date_creation": datetime.now().isoformat()
    }
    
    result = personnes_collection.insert_one(nouvelle_personne)
    nouvelle_personne["_id"] = result.inserted_id
    
    return personne_helper(nouvelle_personne)

@app.put("/personnes/update/", response_model=Personne)
async def update_personne(personne: PersonneUpdate):
    """Met à jour une personne existante"""
    try:
        personne_data = {
            "person_id":personne.id,
            "nom": personne.nom,
            "prenom": personne.prenom,
            "genre": personne.genre.upper(),
            "age": personne.age,
            "couleur_preferee": personne.couleur_preferee,
            "ville": personne.ville,
            "code_postal": personne.code_postal,
        }
        
        result = personnes_collection.find_one_and_update(
            {"_id": ObjectId(personne.id)},
            {"$set": personne_data},
            return_document=True
        )
        
        if not result:
            raise HTTPException(status_code=404, detail="Personne non trouvée")
        
        return personne_helper(result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur: {str(e)}")

@app.delete("/personnes/delete/{personne_id}")
async def delete_personne(personne_id: str):
    """Supprime une personne"""
    try:
        result = personnes_collection.delete_one({"_id": ObjectId(personne_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Personne non trouvée")
        
        return {"message": f"Personne {personne_id} supprimée"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur: {str(e)}")

@app.post("/personnes/{personne_id}/ajouter-ami/{ami_id}")
async def ajouter_ami(personne_id: str, ami_id: str):
    """Ajoute un ami à une personne"""
    try:
        # Vérifie que les deux personnes existent
        personne = personnes_collection.find_one({"_id": ObjectId(personne_id)})
        ami = personnes_collection.find_one({"_id": ObjectId(ami_id)})
        
        if not personne:
            raise HTTPException(status_code=404, detail="Personne non trouvée")
        if not ami:
            raise HTTPException(status_code=404, detail="Ami non trouvé")
        
        # Ajoute l'ami si pas déjà dans la liste
        ami_object_id = ObjectId(ami_id)
        if ami_object_id not in personne.get("amis_ids", []):
            personnes_collection.update_one(
                {"_id": ObjectId(personne_id)},
                {"$push": {"amis_ids": ami_object_id}}
            )
        
        return {"message": f"{ami['prenom']} {ami['nom']} ajouté aux amis"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur: {str(e)}")

@app.get("/personnes/{personne_id}/amis", response_model=List[Personne])
async def get_amis(personne_id: str):
    """Récupère la liste des amis d'une personne"""
    try:
        personne = personnes_collection.find_one({"_id": ObjectId(personne_id)})
        if not personne:
            raise HTTPException(status_code=404, detail="Personne non trouvée")
        
        amis_ids = personne.get("amis_ids", [])
        amis = []
        for ami_id in amis_ids:
            ami = personnes_collection.find_one({"_id": ami_id})
            if ami:
                amis.append(personne_helper(ami))
        
        return amis
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur: {str(e)}")

@app.get("/stats")
async def get_stats():
    """Retourne des statistiques sur les personnes"""
    total = personnes_collection.count_documents({})
    filles = personnes_collection.count_documents({"genre": "F"})
    garcons = personnes_collection.count_documents({"genre": "M"})
    
    # Calcul de l'âge moyen
    pipeline = [
        {"$group": {"_id": None, "age_moyen": {"$avg": "$age"}}}
    ]
    result = list(personnes_collection.aggregate(pipeline))
    age_moyen = result[0]["age_moyen"] if result else 0
    
    # Récupère toutes les villes uniques
    villes = personnes_collection.distinct("ville")
    
    return {
        "total_personnes": total,
        "filles": filles,
        "garçons": garcons,
        "age_moyen": round(age_moyen, 2),
        "villes": villes,
        "status": "✅ MongoDB"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="192.168.1.25", port=1000)
