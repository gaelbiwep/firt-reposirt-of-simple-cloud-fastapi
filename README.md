# API Personnes - FastAPI

Une API simple pour gérer une liste de personnes, leurs amis et leurs informations personnelles.

## Fonctionnalités

✅ **CRUD complet**: Créer, lire, mettre à jour, supprimer des personnes  
✅ **Gestion des amis**: Ajouter/consulter les amis de chaque personne  
✅ **Filtrage**: Par genre, par ville  
✅ **Statistiques**: Obtenir des stats sur les personnes  
✅ **CORS activé**: Prêt pour un frontend web  

## Installation

### 1. Installer Python 3.8+

### 2. Cloner/télécharger le projet

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

## Lancer l'API

```bash
python main.py
```

L'API sera disponible sur **http://localhost:8000**

### Docs interactives Swagger

```
http://localhost:8000/docs
```

## Endpoints disponibles

### Personnes

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/personnes` | Récupère toutes les personnes (avec filtres optionnels) |
| GET | `/personnes/{id}` | Récupère une personne par ID |
| POST | `/personnes` | Crée une nouvelle personne |
| PUT | `/personnes/{id}` | Met à jour une personne |
| DELETE | `/personnes/{id}` | Supprime une personne |

### Amis

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/personnes/{id}/ajouter-ami/{ami_id}` | Ajoute un ami |
| GET | `/personnes/{id}/amis` | Récupère les amis d'une personne |

### Autres

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/stats` | Récupère des statistiques |

## Exemples de requêtes

### Créer une personne

```bash
curl -X POST "http://localhost:8000/personnes" \
  -H "Content-Type: application/json" \
  -d '{
    "nom": "Dupuis",
    "prenom": "Alice",
    "genre": "fille",
    "age": 23,
    "couleur_preferee": "vert",
    "ville": "Marseille",
    "code_postal": "13000"
  }'
```

### Récupérer toutes les personnes

```bash
curl "http://localhost:8000/personnes"
```

### Filtrer par genre

```bash
curl "http://localhost:8000/personnes?genre=fille"
```

### Récupérer une personne

```bash
curl "http://localhost:8000/personnes/1"
```

### Ajouter un ami

```bash
curl -X POST "http://localhost:8000/personnes/1/ajouter-ami/2"
```

## Structure du projet

```
├── main.py          # API RestFul FastAPI
├── requirements.txt # Dépendances Python
└── README.md        # Ce fichier
```

## Déploiement sur le cloud

### Azure App Service

```bash
az webapp up -n mon-app-personnes -g mon-groupe-ressources --runtime python:3.11
```

### Vercel / Railway / Render

Ces plateformes supportent facilement FastAPI. Assure-toi que le `requirements.txt` est à jour.

## Notes

- **Base de données**: Actuellement en mémoire (réinitialise au redémarrage)
- **Production**: Pour la prod, ajoute une vraie base de données (PostgreSQL, MongoDB, Cosmos DB, etc.)
- **Authentification**: À ajouter selon tes besoins (JWT, OAuth, etc.)
