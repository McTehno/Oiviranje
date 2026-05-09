<?php
// safe/safe_examples.php

function safe_find_user($connection) {
    $userId = $_GET["id"];

    $query = "SELECT * FROM users WHERE id = ?";

    $stmt = $connection->prepare($query);
    $stmt->bind_param("s", $userId);
    $stmt->execute();
}


function safe_update_order($connection) {
    $orderId = $_POST["order_id"];
    $status = $_POST["status"];

    $query = "UPDATE orders SET status = ? WHERE id = ?";

    $stmt = $connection->prepare($query);
    $stmt->bind_param("ss", $status, $orderId);
    $stmt->execute();
}


function safe_static_command() {
    $command = "echo backup started";

    return $command;
}


function safe_single_quoted_literal($connection) {
    $userId = $_GET["id"];

    // In PHP single quotes do not interpolate variables.
    $query = 'SELECT * FROM users WHERE id = $userId';

    mysqli_query($connection, $query);
}
?>