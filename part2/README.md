# Git Intro Project

HBnB — Part 2 : Business Logic & API Endpoints
Description
Implémentation de la couche Présentation et Logique Métier de l'application HolbertonBnB,
en utilisant Python, Flask et Flask-RESTx.

Architecture
part2/
├── app/
│   ├── __init__.py              ← Factory Flask + Flask-RESTx
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── users.py         ← GET / POST / PUT  /api/v1/users
│   │       ├── amenities.py     ← GET / POST / PUT  /api/v1/amenities
│   │       ├── places.py        ← GET / POST / PUT  /api/v1/places
│   │       └── reviews.py       ← GET / POST / PUT / DELETE  /api/v1/reviews
│   ├── models/
│   │   ├── base_model.py        ← id, created_at, updated_at
│   │   ├── user.py
│   │   ├── amenity.py
│   │   ├── place.py
│   │   └── review.py
│   ├── persistence/
│   │   └── repository.py        ← Repository (ABC) + InMemoryRepository
│   └── services/
│       └── facade.py            ← HBnBFacade (singleton)
├── config.py
├── requirements.txt
├── run.py
└── test_models.py

Patterns utilisés
Facade
Tous les endpoints API communiquent uniquement avec HBnBFacade.
La façade coordonne les modèles et les repositories.
API → HBnBFacade → InMemoryRepository → Modèles
Repository (ABC)
InMemoryRepository implémente l'interface Repository.
En Part 3, on crée SQLAlchemyRepository sans toucher à la façade.

Installation
bashpip install -r requirements.txt
Lancer le serveur
bashpython run.py
Swagger UI disponible sur : http://localhost:5000/api/v1/doc

Endpoints
MéthodeEndpointDescriptionGET/api/v1/users/Liste tous les usersPOST/api/v1/users/Crée un userGET/api/v1/users/{id}Récupère un userPUT/api/v1/users/{id}Modifie un userGET/api/v1/amenities/Liste tous les équipementsPOST/api/v1/amenities/Crée un équipementGET/api/v1/amenities/{id}Récupère un équipementPUT/api/v1/amenities/{id}Modifie un équipementGET/api/v1/places/Liste tous les logementsPOST/api/v1/places/Crée un logementGET/api/v1/places/{id}Récupère un logement (+owner +amenities)PUT/api/v1/places/{id}Modifie un logementGET/api/v1/places/{id}/reviewsListe les avis d'un logementGET/api/v1/reviews/Liste tous les avisPOST/api/v1/reviews/Crée un avisGET/api/v1/reviews/{id}Récupère un avisPUT/api/v1/reviews/{id}Modifie un avisDELETE/api/v1/reviews/{id}Supprime un avis ← seul DELETE

Exemples cURL
bash# 1. Créer un user
curl -X POST http://localhost:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Alice","last_name":"Martin","email":"alice@test.com","password":"secret"}'

# 2. Créer un équipement
curl -X POST http://localhost:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -d '{"name":"WiFi"}'

# 3. Créer un logement (remplace <user_id> et <amenity_id>)
curl -X POST http://localhost:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Studio Paris","description":"Vue sur tour Eiffel","price":80,"latitude":48.8566,"longitude":2.3522,"owner_id":"<user_id>","amenities":["<amenity_id>"]}'

# 4. Créer un avis
curl -X POST http://localhost:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -d '{"text":"Parfait !","rating":5,"place_id":"<place_id>","user_id":"<user_id>"}'

# 5. Supprimer un avis
curl -X DELETE http://localhost:5000/api/v1/reviews/<review_id>

Tests
bashpython test_models.py
40 tests couvrant :

Validation des modèles (User, Amenity, Place, Review)
Logique métier via la façade
Tests black-box de tous les endpoints REST


Auteur
Holberton School — Projet HBnB Part 2

@Annonym12345
@Mahamadou19-75
