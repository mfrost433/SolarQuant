<?php


if(isset($_POST['value']))
{
    $nodeId = $_POST['value'];
    $servername = "localhost";
    $username = "solarquant";
    $password = "solarquant";
    $dbname = "solarquant";
    
    $conn = new mysqli($servername, $username, $password, $dbname);
    
    $query = "select sourceId from node_source where node_id=".$nodeId;

    exit;
}

?>
