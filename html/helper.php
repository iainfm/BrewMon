<?php
header("Content-Type: text/plain");
?>
<?php
$server = "localhost";
$user   = "brewmonuser";
$pass   = "beerbeerbeer";
$dbname = "brewDB";

$con = new mysqli($server, $user, $pass, $dbname);
if ($con->connect_error) {
   die("Connection failed: " . $con->connect_error);
}

$sql  = "SELECT * FROM BrewMon WHERE probe_active=1 AND probe_name != '-' ORDER BY probe_name";
$rows = $con->query($sql);
$array = [];
if ($rows->num_rows > 0) {
   while($row = $rows->fetch_assoc()) {
      $array[$row["probe_id"]]['probe_name'] = $row["probe_name"];
      $array[$row["probe_id"]]['last_temp'] = (float) $row["last_temp"];
   }
   print json_encode($array);
}
else {
   $array["No probes"] = 0;
   print json_encode($array);
}
?>
