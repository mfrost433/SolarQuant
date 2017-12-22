
<html>
<head>

<title>solarquant.Admin</title>
<link href='../../css/solarStyle.css' type='text/css' rel='stylesheet'>
<link href='../../css/bootstrap.min.css' type='text/css'
	rel='stylesheet'>
<link href='../../css/bootstrap-theme.min.css' type='text/css'
	rel='stylesheet'>
<script src='../../js/bootstrap.min.js'></script>
<link href='../../includes/calendar.css' rel='stylesheet'
	type='text/css' />
<script language='javascript' src='../../includes/calendar.js'></script>

</head>
<body bgcolor='#ffffff'>
	<script
		src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>

	<link rel="stylesheet"
		href="https://unpkg.com/leaflet@1.2.0/dist/leaflet.css"
		integrity="sha512-M2wvCLH6DSRazYeZRIm1JnYyh22purTM+FDB5CsyxtQJYeKq83arPe5wgbNmcFXGqiSH2XR8dT/fJISVA1r/zQ=="
		crossorigin="" />
	<script src="https://unpkg.com/leaflet@1.2.0/dist/leaflet.js"
		integrity="sha512-lInM/apFSqyy1o6s89K4iQUKg6ppXEgsVxT35HbzUupEVRh2Eu9Wdl4tHj7dZO0s1uvplcYGmt3498TtHq+log=="
		crossorigin=""></script>
	<script type="text/javascript">
	
function deleteRequest(reqId){	
	$.ajax({
		type: "POST",
		url: "deleteTrainingRequest.php",
		data:"value="+reqId,
		success: function(data){
			location.reload();
		}
		});
}

function viewCorrelation(reqId){
		   localStorage.setItem("reqId",reqId);
			location = "../prediction/prediction.php";

}


</script>
	<table cellpadding='10' cellspacing='10' class='table table-striped'
		border='0'>
		<tr class='solar4' bgcolor='#ffffff'>
			<td align='center'>
			
			<th>Request ID</th>
			<th>Node ID</th>
			<th>Source ID</th>
			<th>Request Date</th>
			<th>Status</th>
			<th>Analysis Engine</th>
			<th>Action</th>
		</tr>

<?php
$servername = "localhost";
$username = "solarquant";
$password = "solarquant";
$dbname = "solarquant";

$conn = new mysqli($servername, $username, $password, $dbname);

$query = "SELECT * FROM training_requests";

$result = $conn->query($query);

while ($row = $result->fetch_assoc()) {
    echo "<tr>";
    echo "<td></td>";
    echo "<td>" . $row['REQUEST_ID'] . "</td>";
    echo "<td>" . $row['NODE_ID'] . "</td>";
    echo "<td>" . $row['SOURCE_ID'] . "</td>";
    echo "<td>" . $row['DATE_REQUESTED'] . "</td>";
    echo "<td>" . getStatusButtonByNumber($row['STATUS']) . "</td>";
    echo "<td>" . $row['REQUEST_ENGINE'] . "</td>";
    echo "<td>" . getCorrelationButton($row['STATUS'], $row['REQUEST_ID']) . 
    "  <button type='button' class='btn btn-danger btn-xs' 
            onclick='deleteRequest(" . $row['REQUEST_ID'] . ")'>Delete</button>            
         </td>";
    
    echo "</tr>";
}

function getCorrelationButton($num, $reqId)
{
    $status = "";
    if ($num == 4) {
        $status = " <button type='button' class='btn btn-success btn-xs'
       onclick='viewCorrelation(" . $reqId . ")'>Correlation</button>";
    } else {
        $status = " <button type='button' class='btn btn-warning btn-xs'>Correlation</button>";
    }
    return $status;
}

function getStatusButtonByNumber($num)
{
    $status = "";
    
    switch ($num) {
        case 1:
            $status = "Initial";
            break;
        case 2:
            $status = "Retrieving Data";
            break;
        case 3:
            $status = "Training";
            break;
        case 4:
            $status = "Finished";
            break;
        case 5:
            $status = "Error";
            break;
    }
    return "<button type='button' class='btn btn-warning btn-xs'>$status</button>";
}

?>
</table>
</body>
