<!DOCTYPE HTML PUBLIC ""> 
<html>
<head>
	<title>Register</title>
	
</head>

<body>

<?php
	$servername = "localhost";
	$username = "root";
	$password = "";
	$dbname = "Hospital";

	// Create connection
	$conn = new mysqli($servername, $username, $password, $dbname);

	// Check connection
	if ($conn->connect_error) {
		die("Connection failed: " . $conn->connect_error);
	}else{
		
		session_start();
		
		
		
		if(isset($_POST['formSubmit'])) 
		{
			
			$appDate = $_POST['appDate'];
			$appTime = $_POST['usr_time'];

			$errorMessage = "";
		
			if(empty($appDate) or empty($appTime)) 
			{
				$errorMessage = "<li>You need to fill them all!</li>";
			}
			
			if($errorMessage != "") 
			{
				echo("<p>There was an error with your form:</p>\n");
				echo("<ul>" . $errorMessage . "</ul>\n");
			} 
			else 
			{
				//echo "i am here";
				// 
				
				$sql = "SELECT * FROM appointments WHERE ID = " . $_POST['id'];
				$result = $conn->query($sql);
				$row = $result->fetch_assoc();
				$ID_of_Doc = $row["DoctorID"];
				
				if($row["PatientID"] != $_SESSION['userID']){
					die("unauthorised!");
				}
				
				$sql = "SELECT * FROM appointments WHERE date = '" . $appDate . "' AND " . "time = '" . $appTime. "' AND DoctorID = ".  $ID_of_Doc ;
				
				//echo "id = " . $_POST['id']; 
				//echo $sql;

				$result = $conn->query($sql);
				if ($result->num_rows  > 0) {
					
					echo "that time is occopied please try another slot";
					
				} else {
					

					
					$sql = "INSERT INTO appointments (date, time, DoctorID, PatientID) " .
						"VALUES('" . $appDate . "', '" . $appTime ."','". $ID_of_Doc ."','".$_SESSION['userID']. "')";
					//echo $sql;

					if ($conn->query($sql) === TRUE) {
						echo "Appointed successfully <br />";
						$msg = "Return to <a href = 'http://localhost/Hospital/homepage_Hospital_pt.php'>homepage</a> <br />";
						echo $msg;
						$msg = "or logout <a href = 'http://localhost/Hospital/logout_Hospital.php'>logout</a> <br />";
						echo $msg;
						
						//delete old app.
						$sql = "DELETE FROM appointments WHERE ID = " . $_POST['id'];

						if ($conn->query($sql) === TRUE) {
							//echo "Done! <br />";
							//echo "<a href = 'homepage_Hospital_pt.php'>Go to homepage</a>";
						} else {
							echo "Error deleting record: " . $conn->error;
						}
						
						
					} else {
						echo "Error while registering to the system: " . $conn->error;
					}
				}

				exit();
			}
		}

	}
	$conn->close();
?>







<form action="<?php echo htmlentities($_SERVER['PHP_SELF']); ?>" method="post">
	<? echo "hey there"?>
	<p><input type="hidden" name="id" value = <?php echo $_GET['id']?> /></p>
	<p>new Date: <input type="date" name="appDate"/></p>
	<p>Select a new time:<input type="time" step="300" name="usr_time"/></p>
	<p><input type="submit" name = "formSubmit" value = "scheduled"/></p>
</form>

	


</body>
</html>
