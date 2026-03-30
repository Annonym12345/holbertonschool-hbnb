-- ============================================================
--  Task 9 — CRUD test queries
-- ============================================================

-- READ all users
SELECT id, first_name, last_name, email, is_admin FROM users;

-- READ all amenities
SELECT id, name FROM amenities;

-- CREATE a test user (password = test1234)
INSERT OR IGNORE INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
VALUES (
    'aaaabbbb-cccc-dddd-eeee-ffffffffffff',
    'Test', 'User', 'test@hbnb.io',
    '$2b$12$testhashedpassword000000000000000000000000000000000000',
    FALSE,
    CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
);

-- CREATE a test place
INSERT OR IGNORE INTO places (id, title, description, price, latitude, longitude, owner_id, created_at, updated_at)
VALUES (
    'p1111111-1111-1111-1111-111111111111',
    'Test Place', 'A test place in Paris',
    100.0, 48.8566, 2.3522,
    'aaaabbbb-cccc-dddd-eeee-ffffffffffff',
    CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
);

-- CREATE a review
INSERT OR IGNORE INTO reviews (id, text, rating, place_id, user_id, created_at, updated_at)
VALUES (
    'r1111111-1111-1111-1111-111111111111',
    'Great stay!', 5,
    'p1111111-1111-1111-1111-111111111111',
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
);

-- READ reviews for a place
SELECT r.id, r.text, r.rating, u.email
FROM reviews r
JOIN users u ON r.user_id = u.id
WHERE r.place_id = 'p1111111-1111-1111-1111-111111111111';

-- UPDATE a place price
UPDATE places SET price = 150.0, updated_at = CURRENT_TIMESTAMP
WHERE id = 'p1111111-1111-1111-1111-111111111111';

-- DELETE test review
DELETE FROM reviews WHERE id = 'r1111111-1111-1111-1111-111111111111';

-- Verify delete
SELECT COUNT(*) AS remaining FROM reviews WHERE id = 'r1111111-1111-1111-1111-111111111111';
