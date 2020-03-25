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
		
		
		if(isset($_POST['formSubmit'])) 
		{
			
			$name = $_POST['FName'];
			$lastName = $_POST['LName'];
			$password = $_POST['Password'];
			$errorMessage = "";
		
			if(empty($name) or empty($password) or empty($lastName)) 
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
				// Insert the record
				$sql = "INSERT INTO users(Username, Password, Role) " .
					"VALUES('" . $_POST['FName'] . " " . $_POST['LName'] ."', '" . $_POST['Password'] ."', 2" . ")";
				//echo $sql;

				if ($conn->query($sql) === TRUE) {
					echo "Registered successfully <br />";
					$msg = "Please <a href = 'http://localhost/Hospital/login_Hospital.php'>log in</a> to make an appointment <br />";
					echo $msg;
					
				} else {
					echo "Error while registering to the system: " . $conn->error;
				}

				exit();
			}
		}

	}
	$conn->close();
?>







<form action="<?php echo htmlentities($_SERVER['PHP_SELF']); ?>" method="post">
	<p>First name: <input type="text" name="FName" value = "" /></p>
	<p>Last name: <input type="text" name="LName" value = "" /></p>
	<p>Password: <input type="text" name="Password" value = "" /></p>
	<p><input type="submit" name = "formSubmit" value = "register"/></p>
</form>

	


</body>
</html>
