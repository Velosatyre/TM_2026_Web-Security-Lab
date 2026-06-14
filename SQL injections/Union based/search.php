<?php
$db = new SQLite3('lab.db');

$id = $_GET['id'];

$query = "SELECT id, username, email
          FROM users
          WHERE id = $id";

echo "<pre>Query: $query</pre>";

$result = $db->query($query);

while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
    echo htmlspecialchars($row['id']) . " | ";
    echo htmlspecialchars($row['username']) . " | ";
    echo htmlspecialchars($row['email']) . "<br>";
}
?>