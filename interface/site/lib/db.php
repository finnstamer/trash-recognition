<?php


function getPDO(bool $nesting = false){
    $add = ($nesting) ? "../" : "";
    include($add . "lib/env.php");
    (new DotEnv(__DIR__ . DIRECTORY_SEPARATOR . $add .".env"))->load();
    return new PDO("mysql:dbname=id19113998_classification;host=localhost", DotEnv::get("DB_USERNAME"), DotEnv::get("DB_PASSWORD"));
}


?>