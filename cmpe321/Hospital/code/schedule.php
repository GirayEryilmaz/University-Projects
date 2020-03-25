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
				$sql = "SELECT * FROM appointments WHERE date = '" . $appDate . "' AND " . "time = '" . $appTime. "' AND DoctorID = ".  $_SESSION['chosen_doctorID'] ;
				//echo $sql;

				if ($conn->query($sql)->num_rows  > 0) {
					
					echo "that time is occopied please try another slot";
					
				} else {
					
					
					
					$sql = "INSERT INTO appointments (date, time, DoctorID, PatientID) " .
						"VALUES('" . $appDate . "', '" . $appTime ."','". $_SESSION['chosen_doctorID'] ."','".$_SESSION['userID']. "')";
					//echo $sql;

					if ($conn->query($sql) === TRUE) {
						echo "Appointed successfully <br />";
						$msg = "Return to <a href = 'http://localhost/Hospital/homepage_Hospital_pt.php'>homepage</a> <br />";
						echo $msg;
						$msg = "or logout <a href = 'http://localhost/Hospital/logout_Hospital.php'>logout</a> <br />";
						echo $msg;
						
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

	<p>Date: <input type="date" name="appDate"/></p>
	<p>Select a time:<input type="time" step="300" name="usr_time"/></p>
	<p><input type="submit" name = "formSubmit" value = "scheduled"/></p>
</form>

	


</body>
</html>
