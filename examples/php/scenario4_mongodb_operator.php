<?php
function getUserByRole($collection) {
    # tainted user input
    $inputRole = $_GET["role"];
    
    # shranjujemo input v spremenljivko, ki se uporablja v MongoDB operaciji
    $queryFilter = ["role" => ['$ne' => $inputRole]];

    # klicemo MongoDB metodo findOne z nasim filterjem, ki vsebuje uporabnikov input
    return $collection->findOne($queryFilter);
}
?>