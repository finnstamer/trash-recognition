<?php

include "../lib/db.php";

function buildResponse(array $array, int $code = 200){
    header("HTTP 1.1 " . $code);
    die(json_encode($array));
}

function getOrThrow(string $key) {
    if (!isset($_POST[$key])){
        buildResponse(["error" => true, "msg" => "Required data for " . $key], 401);
    }
    return $_POST[$key];
}

if (!isset($_POST["pw"]) || $_POST["pw"] != "test"){
    buildResponse(["msg" => "Required password is incorrect"]);
}

$task = getOrThrow("task");

if ($task == "new"){
    $classified = getOrThrow("classified");
    $conf = getOrThrow("confidence");
    $pdo = getPDO(1);
    $statement = $pdo->prepare(
        "INSERT INTO log (image, classified, confidence) VALUES (:image, :classified, :confidence)"
    );
    $statement->execute(["image" => "", "classified" => $classified, "confidence" => $conf]);
    
}



?>