<?php

// To je testni primer za Command Injection v PHP-ju.

function ping_user_domain() {
    // Pridobimo naslov, ki ga je vpisal uporabnik.
    $domain = $_REQUEST["domain"];

    // Sestavimo sistemski ukaz
    $cmd = "nslookup " . $domain;

    // Pošljemo operacijskemu sistemu na izvedbo s command injection ranljivostjo.
    system($cmd);
}
?>