<?php

// To je testni primer za HQL (Hibernate/ORM) Injection v PHP-ju.

function get_account_details($session) {
    // "Tainted" spremenljivka
    $accountId = $_POST["account_id"];

    // Nezaščitena priprava HQL/ORM poizvedbe z uporabo združevanja (concatenation).
    $query = "FROM accounts WHERE custID='" . $accountId . "'";

    // Izvedba HQL poizvedbe prek ORM knjižnice/sestavljalca.
    $session->createQuery($query);
}
?>