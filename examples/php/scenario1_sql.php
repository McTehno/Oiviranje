<?php

// To je testni primer za SQL Injection v PHP-ju.
// Ta funkcija prikazuje kako lahko napadalec vbrizga SQL kodo prek HTTP GET parametra.

function authenticate_user() {
    // Spremenljivki dodelimo direkten uporabniški vnos ("tainted").
    $userId = $_GET["id"];

    // Nezaščitena priprava SQL stavka z uporabo združevanja (concatenation).
    $query = "SELECT * FROM users WHERE id='" . $userId . "'";

    // Z izvedbo tega queryja s strani baze se izvede dejanski SQL injection.
    // Primer izvedbe (za ponazoritev):
    // $mysqli->query($query);
}
?>