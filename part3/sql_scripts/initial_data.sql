-- ============================================================
--  Task 9 — Initial data
--  Admin user + default amenities
--  Password hash = bcrypt("admin1234")
-- ============================================================

INSERT OR IGNORE INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW',
    TRUE,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

INSERT OR IGNORE INTO amenities (id, name, created_at, updated_at) VALUES
    ('a1b2c3d4-0001-0000-0000-000000000001', 'WiFi',            CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('a1b2c3d4-0002-0000-0000-000000000002', 'Swimming Pool',   CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('a1b2c3d4-0003-0000-0000-000000000003', 'Air Conditioning',CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('a1b2c3d4-0004-0000-0000-000000000004', 'Parking',         CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('a1b2c3d4-0005-0000-0000-000000000005', 'Kitchen',         CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
