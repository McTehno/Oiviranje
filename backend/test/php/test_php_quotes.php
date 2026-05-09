<?php
// test/php/test_php_quotes.php

function vulnerable_sql_double_quotes_concat($connection) {
    $userId = $_GET["id"];
    $query = "SELECT * FROM users WHERE id = " . $userId;
    mysqli_query($connection, $query);
}


function vulnerable_sql_single_quotes_concat($connection) {
    $userId = $_GET['id'];
    $query = 'SELECT * FROM users WHERE id = ' . $userId;
    mysqli_query($connection, $query);
}


function vulnerable_sql_double_quotes_interpolation($connection) {
    $userId = $_GET["id"];
    $query = "SELECT * FROM users WHERE id = $userId";
    mysqli_query($connection, $query);
}


function vulnerable_sql_curly_interpolation($connection) {
    $userId = $_GET['id'];
    $query = "SELECT * FROM users WHERE id = {$userId}";
    mysqli_query($connection, $query);
}


function safe_sql_prepared_statement($connection) {
    $userId = $_GET["id"];

    $query = "SELECT * FROM users WHERE id = ?";
    $stmt = $connection->prepare($query);
    $stmt->bind_param("s", $userId);
    $stmt->execute();
}


function safe_single_quoted_literal($connection) {
    $userId = $_GET["id"];
    $query = 'SELECT * FROM users WHERE id = $userId';
    mysqli_query($connection, $query);
}
?>