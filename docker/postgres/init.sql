CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

INSERT INTO users (id, name, password) VALUES
    (1, 'admin', 'admin'),
    (2, 'alice', 'password'),
    (3, 'bob', 'secret'),
    (4, 'test', 'test')
ON CONFLICT (id) DO NOTHING;

CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    category VARCHAR(255) NOT NULL,
    released BOOLEAN NOT NULL DEFAULT TRUE
);

INSERT INTO products (id, name, price, category, released) VALUES
    (1, 'Keyboard', 49.99, 'Computers', TRUE),
    (2, 'Mouse', 19.99, 'Computers', TRUE),
    (3, 'Coffee mug', 12.50, 'Kitchen', TRUE),
    (4, 'Secret product', 999.99, 'Hidden', FALSE)
ON CONFLICT (id) DO NOTHING;
