<?php
// system/command_tools.php

function ping_host() {
    $host = $_GET["host"];

    $command = "ping " . $host;

    system($command);
}


function list_directory() {
    $folder = $_GET["folder"];

    $command = "ls " . $folder;

    shell_exec($command);
}


function backup_file() {
    $filename = $_POST["file"];

    $backupCommand = "cp " . $filename . " /tmp/backup/";

    exec($backupCommand);
}


function show_file() {
    $file = $_GET["file"];

    $command = "cat " . $file;

    passthru($command);
}
?>