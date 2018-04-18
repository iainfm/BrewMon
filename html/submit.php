<html>
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

print "<br>";
while (list($probe_id, $probe_name) = each($_GET)) {
   $sql = "UPDATE BrewMon SET probe_name='$probe_name' WHERE probe_id='$probe_id'";
   print "$sql";

   if ($con->query($sql) === TRUE) {
      print "[OK]<br>";
   } else {
      print "[$con->error]<br>";
   }
}
$con->close();
header('Location: /');
?>
</body>
</html>
