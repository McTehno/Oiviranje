<?php

// Ta datoteka združuje vse 3 simulirane ranljivosti (SQL, HQL, Command Injection), 
// da se preveri obnašanje programa za vse primere naenkrat v PHP okolju.

function simulate_sql_injection() {
    $user_id = $_GET["id"];
    // Združevanje v SQL stavek
    $query = "SELECT * FROM users WHERE id='" . $user_id . "'";
}

function simulate_hql_injection($session) {
    $user_id = $_POST["id"];
    // HQL/ORM pattern za Injection
    $hql_query = "FROM accounts WHERE custID='" . $user_id . "'";
    $session->createQuery($hql_query);
}

function simulate_command_injection() {
    $domain = $_REQUEST["domain"];
    // Ranljivo izvajanje ukazov operacijskega sistema
    $cmd = "ping -c 4 " . $domain;
    shell_exec($cmd);
}

?>