# Git Intro Project

# 🏠 HBnB Evolution - Part 1

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Description

Projet HBnB Evolution développé dans le cadre du programme Holberton School. Cette partie (Part 1) se concentre sur la conception et la documentation de l'architecture du système.

## 🔄 Diagrammes

Le projet comprend plusieurs diagrammes illustrant l'architecture et les flux de l'application :

### 📊 Documentation des Diagrammes

- **[📈 Business Logic Diagrams](./business_diagrams.md)** - Diagrammes de la logique métier et des services
- **[🔌 API Sequence Diagrams](./diagrams_api.md)** - Diagrammes de séquence des interactions API
- **[📦 Package Diagrams](./diagrams_package.md)** - Diagrammes de la structure des packages

### Diagrammes de Séquence Principaux

Les 4 flux principaux de l'application :
```mermaid
sequenceDiagram
    participant User
    participant API
    participant BusinessLogic
    participant Database

    %% =========================
    %% 1️⃣ REGISTER NEW ACCOUNT
    %% =========================
    rect rgb(230, 230, 250)
    Note over User,Database: REGISTER NEW ACCOUNT
    User->>API: Register new account
    API->>BusinessLogic: Validate & create User
    BusinessLogic->>Database: Save User
    Database-->>BusinessLogic: Confirm Save
    BusinessLogic-->>API: Return Success
    API-->>User: Registration Complete
    end

    %% =========================
    %% 2️⃣ CREATE NEW PLACE
    %% =========================
    rect rgb(230, 255, 230)
    Note over User,Database: CREATE NEW PLACE
    User->>API: Create new Place
    API->>BusinessLogic: Validate & create Place
    BusinessLogic->>Database: Save Place
    Database-->>BusinessLogic: Confirm Save
    BusinessLogic-->>API: Return Success
    API-->>User: Place Created
    end

    %% =========================
    %% 3️⃣ SUBMIT REVIEW
    %% =========================
    rect rgb(255, 240, 220)
    Note over User,Database: SUBMIT REVIEW
    User->>API: Submit Review
    API->>BusinessLogic: Validate & create Review
    BusinessLogic->>Database: Save Review
    Database-->>BusinessLogic: Confirm Save
    BusinessLogic-->>API: Return Success
    API-->>User: Review Submitted
    end

    %% =========================
    %% 4️⃣ REQUEST LIST OF PLACES
    %% =========================
    rect rgb(255, 230, 230)
    Note over User,Database: REQUEST LIST OF PLACES
    User->>API: Request List of Places
    API->>BusinessLogic: Fetch Places based on criteria
    BusinessLogic->>Database: Query Places
    Database-->>BusinessLogic: Return Places
    BusinessLogic-->>API: Return List
    API-->>User: Display Places
    end
```

## 📁 Structure du Projet
```
holbertonschool-hbnb/
└── part1/
    ├── business_diagrams.md    - Diagrammes de logique métier
    ├── diagrams_api.md         - Diagrammes de séquence API
    ├── diagrams_package.md     - Diagrammes de packages
    └── README.md               - Ce fichier
```

## 👥 Auteurs

- **Holberton School** - Projet Académique
- [@Annonym12345](https://github.com/Annonym12345)
- [Mahamadou19-75](https://github.com/Mahamadou19-75)
---

**Note**: Ce projet est réalisé dans un cadre éducatif à Holberton School.
