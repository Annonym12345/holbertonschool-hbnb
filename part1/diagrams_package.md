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
