```mermaid

sequenceDiagram
    participant User
    participant API
    participant BusinessLogic
    participant Database

    %% =========================
    %% 1️⃣ REGISTER USER
    %% =========================
    rect rgb(230, 230, 250)
    Note over User,Database: REGISTER USER
    User->>API: POST /register (user info)
    API->>BusinessLogic: validateUserData(user info)
    BusinessLogic->>Database: saveUser(user)
    Database-->>BusinessLogic: confirmation
    BusinessLogic-->>API: success / failure
    API-->>User: 201 Created / 400 Bad Request
    end

    %% =========================
    %% 2️⃣ CREATE PLACE
    %% =========================
    rect rgb(230, 255, 230)
    Note over User,Database: CREATE PLACE
    User->>API: POST /places (place info)
    API->>BusinessLogic: validatePlaceData(place info)
    BusinessLogic->>Database: savePlace(place)
    Database-->>BusinessLogic: confirmation
    BusinessLogic-->>API: success / failure
    API-->>User: 201 Created / 400 Bad Request
    end

    %% =========================
    %% 3️⃣ GET PLACES
    %% =========================
    rect rgb(255, 240, 220)
    Note over User,Database: GET PLACES WITH FILTERS
    User->>API: GET /places?filters
    API->>BusinessLogic: fetchPlaces(filters)
    BusinessLogic->>Database: queryPlaces(filters)
    Database-->>BusinessLogic: list of places
    BusinessLogic-->>API: return places
    API-->>User: 200 OK (place list)
    end
