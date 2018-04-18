<html>
<head>
<link rel="stylesheet" type="text/css" href="adminstyles.css">
</head>
<body>
<?php
$server = "localhost";
$user   = "brewmonuser";
$pass   = "beerbeerbeer";
$dbname = "brewDB";

$con = new mysqli($server, $user, $pass, $dbname);
if ($con->connect_error) {
   die("Connection failed: " . $con->connect_error);
}

$sql  = "SELECT * FROM BrewMon WHERE probe_active=1";
$rows = $con->query($sql);

if ($rows->num_rows > 0) {
   echo "<table border=1>";
   echo "<th>Probe ID</th><th>Name</th>";
   while($row = $rows->fetch_assoc()) {
      echo "<form action='submit.php' method='get'>";
      echo "<tr>";
      echo "<td>" . $row["probe_id"] . "</td>";
      echo "<td>";
      echo "<input type='text' name=" . $row["probe_id"];
      echo " value='" . $row["probe_name"];
      echo "'></td>";
      # echo "<td>";
      # echo $row["probe_active"];
      # echo "</td>";
      echo "</tr>";
   }
   echo "<tr><td>";
   echo "<input type='submit'>";
   echo "</td></tr>";
   echo "</table>";
   echo "</form>";
}

?>
</body>
</html>
