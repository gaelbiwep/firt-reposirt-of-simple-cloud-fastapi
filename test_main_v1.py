from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Initialisation de l'app FastAPI
app = FastAPI(title="FRIENDS API", description="API pour gérer les personnes, leurs amis et infos")

# Configuration CORS pour permettre au frontend de communiquer
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============= MODELS DE DONNEES =============

class Personne(BaseModel):
    id: int
    nom: str
    prenom: str
    genre: str  # "M" ou "F"
    age: int
    couleur_preferee: str
    ville: str  # Lieu d'habitation
    code_postal: Optional[str] = None
    amis_ids: List[int] = []  # IDs des copains/copines
    date_creation: Optional[str] = None

class PersonneCreate(BaseModel):
    nom: str
    prenom: str
    genre: str
    age: int
    couleur_preferee: str
    ville: str
    code_postal: Optional[str] = None

# ============= BASE DE DONNEES EN MEMOIRE =============

# En production, utilise MongoDB, PostgreSQL ou Cosmos DB
personnes_db: List[Personne] = [
    Personne(
        id=1,
        nom="Dupont",
        prenom="Marie",
        genre="F",
        age=25,
        couleur_preferee="rose",
        ville="Paris",
        code_postal="75001",
        amis_ids=[2, 3],
        date_creation=datetime.now().isoformat()
    ),
    Personne(
        id=2,
        nom="Martin",
        prenom="Jean",
        genre="M",
        age=26,
        couleur_preferee="bleu",
        ville="Lyon",
        code_postal="69000",
        amis_ids=[1],
        date_creation=datetime.now().isoformat()
    ),
    Personne(
        id=3,
        nom="Bernard",
        prenom="Sophie",
        genre="M",
        age=24,
        couleur_preferee="violet",
        ville="Paris",
        code_postal="75002",
        amis_ids=[1],
        date_creation=datetime.now().isoformat()
    ),
]

# ============= ENDPOINTS =============

@app.get("/")
async def root():
    """Route d'accueil"""
    return {
        "message": "Bienvenue sur FRIENDS API ",
        "version": "1.0.1",
        "endpoints": {
            "GET /personnes": "Récupère toutes les personnes",
            "GET /personnes/{id}": "Récupère une personne par ID",
            "POST /personnes": "Crée une nouvelle personne",
            "PUT /personnes/{id}": "Met à jour une personne",
            "DELETE /personnes/{id}": "Supprime une personne",
            "POST /personnes/{id}/ajouter-ami/{ami_id}": "Ajoute un ami",
        }
    }

@app.get("/personnes", response_model=List[Personne])
async def get_personnes(genre: Optional[str] = None, ville: Optional[str] = None):
    """
    Récupère toutes les personnes.
    Filtres optionnels: genre, ville
    """
    resultats = personnes_db
    
    if genre:
        resultats = [p for p in resultats if p.genre.lower() == genre.title()]
    if ville:
        resultats = [p for p in resultats if p.ville.lower() == ville.lower()]
    
    return resultats

@app.get("/personnes/{personne_id}", response_model=Personne)
async def get_personne(personne_id: int):
    """Récupère une personne par son ID"""
    personne = next((p for p in personnes_db if p.id == personne_id), None)
    if not personne:
        raise HTTPException(status_code=404, detail="Personne non trouvée")
    return personne

@app.post("/personnes", response_model=Personne)
async def create_personne(personne: PersonneCreate):
    """Crée une nouvelle personne"""
    # Génère un nouvel ID
    new_id = max([p.id for p in personnes_db], default=0) + 1
    
    new_personne = Personne(
        id=new_id,
        nom=personne.nom,
        prenom=personne.prenom,
        genre=personne.genre,
        age=personne.age,
        couleur_preferee=personne.couleur_preferee,
        ville=personne.ville,
        code_postal=personne.code_postal,
        date_creation=datetime.now().isoformat()
    )
    
    personnes_db.append(new_personne)
    return new_personne

@app.put("/personnes/{personne_id}", response_model=Personne)
async def update_personne(personne_id: int, personne: PersonneCreate):
    """Met à jour une personne existante"""
    personne_existante = next((p for p in personnes_db if p.id == personne_id), None)
    if not personne_existante:
        raise HTTPException(status_code=404, detail="Personne non trouvée")
    
    personne_existante.nom = personne.nom
    personne_existante.prenom = personne.prenom
    personne_existante.genre = personne.genre
    personne_existante.age = personne.age
    personne_existante.couleur_preferee = personne.couleur_preferee
    personne_existante.ville = personne.ville
    personne_existante.code_postal = personne.code_postal
    
    return personne_existante

@app.delete("/personnes/{personne_id}")
async def delete_personne(personne_id: int):
    """Supprime une personne"""
    global personnes_db
    personne = next((p for p in personnes_db if p.id == personne_id), None)
    if not personne:
        raise HTTPException(status_code=404, detail="Personne non trouvée")
    
    personnes_db = [p for p in personnes_db if p.id != personne_id]
    
    return {"message": f"Personne {personne_id} supprimée"}

@app.post("/personnes/{personne_id}/ajouter-ami/{ami_id}")
async def ajouter_ami(personne_id: int, ami_id: int):
    """Ajoute un ami à une personne"""
    personne = next((p for p in personnes_db if p.id == personne_id), None)
    ami = next((p for p in personnes_db if p.id == ami_id), None)
    
    if not personne:
        raise HTTPException(status_code=404, detail="Personne non trouvée")
    if not ami:
        raise HTTPException(status_code=404, detail="Ami non trouvé")
    
    if ami_id not in personne.amis_ids:
        personne.amis_ids.append(ami_id)
    
    return {"message": f"{ami.prenom} {ami.nom} ajouté aux amis de {personne.prenom}"}

@app.get("/personnes/{personne_id}/amis", response_model=List[Personne])
async def get_amis(personne_id: int):
    """Récupère la liste des amis d'une personne"""
    personne = next((p for p in personnes_db if p.id == personne_id), None)
    if not personne:
        raise HTTPException(status_code=404, detail="Personne non trouvée")
    
    amis = [p for p in personnes_db if p.id in personne.amis_ids]
    return amis

@app.get("/stats")
async def get_stats():
    """Retourne des statistiques sur les personnes"""
    return {
        "total_personnes": len(personnes_db),
        "filles": len([p for p in personnes_db if p.genre.lower() == "F"]),
        "garçons": len([p for p in personnes_db if p.genre.lower() == "M"]),
        "age_moyen": sum([p.age for p in personnes_db]) / len(personnes_db) if personnes_db else 0,
        "villes": list(set([p.ville for p in personnes_db])),
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="192.168.1.25", port=1000)
