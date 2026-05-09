<?php
// index.php

require_once "db/users_sql.php";
require_once "db/orders_sql.php";
require_once "system/command_tools.php";
require_once "safe/safe_examples.php";

function run_demo($connection) {
    find_user_by_id($connection);
    search_orders($connection);
    ping_host();
    safe_find_user($connection);
}
?>