/*Creation des différentes tables
et insertion de données */

-- Table des utilisateurs
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY,
    name VARCHAR(255),
    password VARCHAR(255)
);

-- Données d'utilisateurs d'exemples
INSERT INTO users (id, name, password) VALUES
    (1, 'admin', 'admin'),
    (2, 'alice', 'password'),
    (3, 'bob', 'secret'),
    (4, 'test', 'test');

-- Table des produits
CREATE TABLE IF NOT EXISTS products (
    id INT PRIMARY KEY,
    name VARCHAR(255),
    price FLOAT,
    category VARCHAR(255),
    released BOOLEAN
);

-- Données de produits d'exemples
INSERT INTO products (id, name, price, category, released) VALUES
    (1, 'Keyboard', 49.99, 'Computers', TRUE),
    (2, 'Mouse', 19.99, 'Computers', TRUE),
    (3, 'Coffee mug', 12.50, 'Kitchen', TRUE),
    (5, 'Wireless headphones', 79.99, 'Electronics', TRUE),
    (6, 'Smartphone', 699.00, 'Electronics', TRUE),
    (7, 'USB-C hub', 34.50, 'Electronics', TRUE),
    (8, 'Smartwatch', 149.99, 'Electronics', FALSE),
    (9, 'Portable projector', 249.99, 'Electronics', FALSE),
    (10, 'Chef knife', 39.99, 'Kitchen', TRUE),
    (11, 'Blender', 59.99, 'Kitchen', TRUE),
    (12, 'Cast iron pan', 44.50, 'Kitchen', TRUE),
    (13, 'Espresso machine', 189.00, 'Kitchen', FALSE),
    (14, 'Reusable food container set', 24.99, 'Kitchen', TRUE),
    (15, 'Yoga mat', 29.99, 'Sports', TRUE),
    (16, 'Running shoes', 89.99, 'Sports', TRUE),
    (17, 'Adjustable dumbbells', 129.99, 'Sports', TRUE),
    (18, 'Climbing harness', 74.50, 'Sports', FALSE),
    (19, 'Road bicycle', 899.00, 'Sports', FALSE),
    (20, 'The Great Gatsby', 10.99, 'Books', TRUE),
    (21, 'Clean Code', 42.00, 'Books', TRUE),
    (22, 'The Pragmatic Programmer', 39.99, 'Books', TRUE),
    (23, 'Advanced PostgreSQL', 54.99, 'Books', FALSE),
    (24, 'Introduction to Algorithms', 89.99, 'Books', TRUE);

-- Table des sessions
CREATE TABLE IF NOT EXISTS sessions (
    SSID VARCHAR(255)
);