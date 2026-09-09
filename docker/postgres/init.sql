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
    (4, 'Secret product', 999.99, 'Hidden', FALSE);

-- Table des sessions
CREATE TABLE IF NOT EXISTS sessions (
    SSID VARCHAR(255)
);