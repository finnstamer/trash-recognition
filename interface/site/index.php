<?php

include "lib/db.php";

$pdo = getPDO();
$stm = $pdo->prepare("SELECT * FROM log ORDER BY id DESC LIMIT 1");
$stm->execute();
$rows = $stm->fetchAll();
$row= $rows[0];

?>

<html>
    <body>
        <p>Last classification at: <?php echo $row["time"]?></p>
        <p>Last image: </p>
        <image src=""></image>
        <p>Last image classified as: <?php echo $row["classified"]?></p>
        <p>Last image classified with: <?php echo $row["confidence"] . "%"?></p>
    </body>
</html>

<script>


</script>