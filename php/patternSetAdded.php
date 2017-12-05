<?php

$file = '/var/www/html/solarquant/php/log.txt';



$current = date('Y-m-d H:i:s');

file_put_contents($file, $current."\n", FILE_APPEND);


$servername = "localhost";
$username = "solarquant";
$password = "solarquant";
$dbname = "solarquant";

$conn = new mysqli($servername, $username, $password, $dbname);

$val = 'Null';
$cDate  = date('Y-m-d H:i:s');

file_put_contents($file, $date."\n", FILE_APPEND);

$node = trim($_REQUEST['nodeId']);

$source = trim($_REQUEST['sourceId']);
$initState = "1";
$engine = $_REQUEST['analysisEngine'];

file_put_contents($file, $node."\n", FILE_APPEND);
file_put_contents($file, $source."\n", FILE_APPEND);
file_put_contents($file, $engine."\n", FILE_APPEND);


$query = "INSERT INTO training_requests VALUES($val, $node, '$source','$cDate',$initState, '$engine')";
file_put_contents($file, $query, FILE_APPEND);
if($conn->query($query) === TRUE){
    file_put_contents($file, 'good', FILE_APPEND);
}else{
    file_put_contents($file, 'bad', FILE_APPEND);
}


?>
