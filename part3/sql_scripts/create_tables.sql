-- ============================================================
--  Task 9 — HBnB database schema
--  Creates all tables and relationships
-- ============================================================

-- Users
CREATE TABLE IF NOT EXISTS users (
    id         VARCHAR(36)  PRIMARY KEY,
    first_name VARCHAR(50)  NOT NULL,
    last_name  VARCHAR(50)  NOT NULL,
    email      VARCHAR(120) NOT NULL UNIQUE,
    password   VARCHAR(128) NOT NULL,
    is_admin   BOOLEAN      NOT NULL DEFAULT FALSE,
    created_at DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Places
CREATE TABLE IF NOT EXISTS places (
    id          VARCHAR(36)  PRIMARY KEY,
    title       VARCHAR(100) NOT NULL,
    description TEXT,
    price       FLOAT        NOT NULL CHECK (price >= 0),
    latitude    FLOAT        NOT NULL CHECK (latitude  BETWEEN -90  AND  90),
    longitude   FLOAT        NOT NULL CHECK (longitude BETWEEN -180 AND 180),
    owner_id    VARCHAR(36)  NOT NULL,
    created_at  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Reviews
CREATE TABLE IF NOT EXISTS reviews (
    id         VARCHAR(36) PRIMARY KEY,
    text       TEXT        NOT NULL,
    rating     INTEGER     NOT NULL CHECK (rating BETWEEN 1 AND 5),
    place_id   VARCHAR(36) NOT NULL,
    user_id    VARCHAR(36) NOT NULL,
    created_at DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (place_id, user_id),
    FOREIGN KEY (place_id) REFERENCES places(id)  ON DELETE CASCADE,
    FOREIGN KEY (user_id)  REFERENCES users(id)   ON DELETE CASCADE
);

-- Amenities
CREATE TABLE IF NOT EXISTS amenities (
    id         VARCHAR(36) PRIMARY KEY,
    name       VARCHAR(50) NOT NULL UNIQUE,
    created_at DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Place <-> Amenity  (many-to-many)
CREATE TABLE IF NOT EXISTS place_amenity (
    place_id   VARCHAR(36) NOT NULL,
    amenity_id VARCHAR(36) NOT NULL,
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id)   REFERENCES places(id)    ON DELETE CASCADE,
    FOREIGN KEY (amenity_id) REFERENCES amenities(id) ON DELETE CASCADE
);
