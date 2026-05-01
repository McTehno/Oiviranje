<?php

function getUser($collection) {
    $username = $_GET["username"];
    $filter = ["username" => $username];

    return $collection->findOne($filter);
}

?>