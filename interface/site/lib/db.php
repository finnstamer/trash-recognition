<?php


function getPDO(){
    include(__DIR__ . "/env.php");
    (new DotEnv(__DIR__ . "/../.env"))->load();
    return new PDO("mysql:dbname=id19113998_classification;host=localhost", DotEnv::get("DB_USERNAME"), DotEnv::get("DB_PASSWORD"));
}


?>