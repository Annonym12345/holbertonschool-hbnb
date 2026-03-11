# Git Intro Project

HBnB — Part 3 : Authentication, Authorization & Database Persistence

Holberton School — AirBnB Clone Project
Part 3 adds JWT authentication, role-based access control, and SQLAlchemy persistence to the REST API built in Part 2.


Table of Contents

Project Overview
Architecture
File Structure
Technologies
Setup & Installation
Configuration
API Endpoints
Authentication
Database
ER Diagram
Tasks Summary


Project Overview
HBnB Part 3 extends the RESTful API from Part 2 with:

Password hashing using bcrypt
JWT authentication via flask-jwt-extended
Role-based access control (authenticated users vs. administrators)
SQLAlchemy ORM replacing the in-memory repository
SQLite database for development
SQL scripts for schema creation and initial data


Architecture
The project follows a 3-layer architecture with the Facade Pattern:
Client (HTTP)
      ↓
Presentation Layer   →  app/api/v1/namespaces/
      ↓                 (users, places, reviews, amenities, auth)
Facade Layer         →  app/services/facade.py
      ↓                 (HBnBFacade — single entry point)
Persistence Layer    →  app/persistence/repository.py
      ↓                 (SQLAlchemyRepository)
Models               →  app/models/
                        (User, Place, Review, Amenity, BaseModel)

File Structure
part3/
├── run.py                              # Entry point
├── config.py                           # Dev / Test / Prod configs
├── requirements.txt
├── sql_scripts/
│   ├── schema.sql                      # Task 9 — table creation + initial data
│   └── er_diagram.md                   # Task 10 — Mermaid ER diagram
└── app/
    ├── __init__.py                     # Task 0 — Application Factory
    ├── models/
    │   ├── base_model.py               # Task 6 — SQLAlchemy BaseModel
    │   ├── user.py                     # Task 1 — bcrypt password hashing
    │   ├── amenity.py                  # Task 7 — SQLAlchemy mapping
    │   ├── place.py                    # Task 7+8 — mapping + relationships
    │   └── review.py                   # Task 7+8 — mapping + relationships
    ├── persistence/
    │   └── repository.py               # Task 5 — SQLAlchemyRepository
    ├── services/
    │   └── facade.py                   # Tasks 5+6 — HBnBFacade + UserRepository
    └── api/v1/namespaces/
        ├── auth.py                     # Task 2 — JWT login endpoint
        ├── users.py                    # Tasks 3+4 — protected + admin endpoints
        ├── amenities.py                # Task 4 — admin-only write access
        ├── places.py                   # Task 3 — ownership checks
        └── reviews.py                  # Task 3 — ownership + restrictions

Technologies
PackageVersionRoleFlask3.0.3Web frameworkFlask-RESTx1.3.0REST API + Swagger UIFlask-SQLAlchemy3.1.1ORM / database layerFlask-Bcrypt1.0.1Password hashingFlask-JWT-Extended4.6.0JWT authenticationSQLAlchemy2.0.30SQL toolkit

Setup & Installation
bash# 1. Clone and enter the directory
cd ~/holbertonschool-hbnb/part3

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the server (creates development.db automatically)
python run.py
Swagger UI is available at: http://127.0.0.1:5000/api/v1/

Configuration
Defined in config.py. Three environments are available:
EnvironmentDatabaseDebugdevelopment (default)sqlite:///development.dbTruetestingsqlite:///:memory:Falseproduction$DATABASE_URLFalse
Environment variables:
bashexport SECRET_KEY="your-secret-key"
export JWT_SECRET_KEY="your-jwt-secret"
export DATABASE_URL="sqlite:///development.db"
The factory is called in run.py:
pythonapp = create_app('development')

API Endpoints
Authentication
MethodURLAccessDescriptionPOST/api/v1/auth/loginPublicLogin — returns JWT token
Users
MethodURLAccessDescriptionGET/api/v1/users/PublicList all usersPOST/api/v1/users/Admin onlyCreate a userGET/api/v1/users/{id}PublicGet user by idPUT/api/v1/users/{id}Authenticated (own) / Admin (any)Update user
Amenities
MethodURLAccessDescriptionGET/api/v1/amenities/PublicList all amenitiesPOST/api/v1/amenities/Admin onlyCreate amenityGET/api/v1/amenities/{id}PublicGet amenity by idPUT/api/v1/amenities/{id}Admin onlyUpdate amenity
Places
MethodURLAccessDescriptionGET/api/v1/places/PublicList all placesPOST/api/v1/places/AuthenticatedCreate placeGET/api/v1/places/{id}PublicGet place (with owner + amenities)PUT/api/v1/places/{id}Owner / AdminUpdate placeGET/api/v1/places/{id}/reviewsPublicList reviews for a place
Reviews
MethodURLAccessDescriptionGET/api/v1/reviews/PublicList all reviewsPOST/api/v1/reviews/AuthenticatedCreate reviewGET/api/v1/reviews/{id}PublicGet review by idPUT/api/v1/reviews/{id}Author / AdminUpdate reviewDELETE/api/v1/reviews/{id}Author / AdminDelete review

Authentication
Login
bashcurl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "yourpassword"}'
Response:
json{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
Using the token
bashcurl -X POST http://localhost:5000/api/v1/places/ \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "Nice flat", "price": 80.0, "latitude": 48.8, "longitude": 2.3, "owner_id": "<user_id>"}'
Access rules
ActionRuleCreate/update amenitiesAdmin only (is_admin: true in JWT)Create userAdmin onlyUpdate own profileAny authenticated user (no email/password change)Update any user (incl. email & password)Admin onlyCreate/update/delete placesOwner or AdminCreate reviewAuthenticated — cannot review own place, no duplicateUpdate/delete reviewAuthor or Admin

Database
The database is initialized automatically on python run.py via db.create_all().
To reset and use raw SQL instead:
bashsqlite3 instance/development.db < sql_scripts/schema.sql
The schema creates:

users — with bcrypt-hashed passwords
places — linked to owner via owner_id FK
reviews — linked to place + user, unique constraint (place_id, user_id)
amenities
place_amenity — many-to-many join table

Initial data inserted by schema.sql:

5 amenities: WiFi, Swimming Pool, Air Conditioning, Parking, Kitchen


ER Diagram
See sql_scripts/er_diagram.md (renders automatically on GitHub).
users        ||--o{  places        : owns
users        ||--o{  reviews       : writes
places       ||--o{  reviews       : has
places       }o--o{  amenities     : place_amenity (many-to-many)
