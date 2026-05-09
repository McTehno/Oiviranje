<?php
// db/users_sql.php

function find_user_by_id($connection) {
    $userId = $_GET["id"];

    $query = "SELECT * FROM users WHERE id = " . $userId;

    mysqli_query($connection, $query);
}


function find_user_by_email($connection) {
    $email = $_GET['email'];

    $query = 'SELECT * FROM users WHERE email = "' . $email . '"';

    mysqli_query($connection, $query);
}


function find_user_with_double_quote_interpolation($connection) {
    $username = $_GET["username"];

    $query = "SELECT * FROM users WHERE username = $username";

    mysqli_query($connection, $query);
}


function find_user_with_curly_interpolation($connection) {
    $username = $_GET['username'];

    $query = "SELECT * FROM users WHERE username = {$username}";

    mysqli_query($connection, $query);
}
?>