<?php
$db = new SQLite3('lab.db');

$db->exec("
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT,
    email TEXT
);
");

$db->exec("
INSERT INTO users (username,email)
VALUES
('alice','alice@example.com'),
('bob','bob@example.com'),
('charlie','charlie@example.com');
");

echo "Database created.";