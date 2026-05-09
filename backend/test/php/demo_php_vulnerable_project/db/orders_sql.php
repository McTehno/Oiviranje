<?php
// db/orders_sql.php

function search_orders($connection) {
    $userId = $_GET["user_id"];
    $status = $_GET["status"];
    $sortBy = $_GET["sort_by"];

    $selectedUser = $userId;
    $selectedStatus = $status;
    $orderColumn = $sortBy;

    $tableName = "orders";
    $baseQuery = "SELECT * FROM " . $tableName;

    $whereClause =
        " WHERE user_id = " . $selectedUser .
        " AND status = '" . $selectedStatus . "'";

    $orderClause = " ORDER BY " . $orderColumn;

    $query = $baseQuery . $whereClause . $orderClause;

    mysqli_query($connection, $query);
}


function update_order_status($connection) {
    $orderId = $_POST["order_id"];
    $newStatus = $_POST["status"];

    $query = "UPDATE orders SET status = '" . $newStatus . "' WHERE id = " . $orderId;

    mysqli_query($connection, $query);
}


function delete_order($connection) {
    $orderId = $_GET["order_id"];

    $query = "DELETE FROM orders WHERE id = " . $orderId;

    mysqli_query($connection, $query);
}
?>