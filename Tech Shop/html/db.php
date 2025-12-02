<?php
$conn = null;
$max_retries = 5;
$retry_delay = 2;

for ($i = 0; $i < $max_retries; $i++) {
    $conn = @new mysqli("db", "ctf_player", "player_pass", "shop_db");
    if (!$conn->connect_error) {
        break;
    }
    sleep($retry_delay);
}

if ($conn->connect_error) {
    die("Database unavailable. Please try again later.");
}

$conn->set_charset("utf8mb4");
?>
