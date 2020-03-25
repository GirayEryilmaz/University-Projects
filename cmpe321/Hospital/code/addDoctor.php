<!DOCTYPE HTML PUBLIC ""> 
<html>
<head>
	<title>Hospital</title>
<!-- define some style elements-->
<style>
label,a 
{
	font-family : Arial, Helvetica, sans-serif;
	font-size : 12px; 
}

</style>	
</head>

<body>
<?php

	session_start();
        
    if(!isset($_SESSION['Role']) or  $_SESSION['Role']!=1){
		die("unauthorized access");
	}
	
	if(isset($_POST['formSubmit'])) 
	{	
		
		$branch = $_POST['formDoctor'];
		echo $branch . " ==>  ";
		$name = $_POST['FName'];
		$lastName = $_POST['LName'];
		$errorMessage = "";
		
		if(empty($branch)) 
		{
			$errorMessage = "<li>You forgot to select a branch!</li>";
		}
		
		if($errorMessage != "") 
		{
			echo("<p>There was an error with your form:</p>\n");
			echo("<ul>" . $errorMessage . "</ul>\n");
		} 
		else 
		{
			
		
				
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
				
				$sql = "INSERT INTO Doctors(Name, Surname, Branch) " .
					"VALUES('" . $_POST['FName'] . "' ,'" . $_POST['LName'] ."', '" . $branch . "')";
				

				if ($conn->query($sql) === TRUE) {
					echo "Doctor added <br />";
					//$msg = "Please <a href = 'http://localhost/Hospital/login_Hospital.php'>log in</a> to make an appointment <br />";
					//echo $msg;
					
				} else {
					echo "Error while registering to the system: " . $conn->error;
				}

			}


			

			exit();
		}
	}
?>







<form action="<?php echo htmlentities($_SERVER['PHP_SELF']); ?>" method="post">
	<label for='formDoctor'>Select Doctor</label><br>
	<?
	
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
			
			//session_start();
			//$branch = $_SESSION['chosen_branch'] ;


			//query 
			//$result=$conn->query("SELECT DISTINCT  Branch FROM Doctors");
			$result=$conn->query("SELECT BranchName FROM Branches");
			//echo "SELECT *  FROM Doctors WHERE Branch = ' " . $branch . "'"  ;
			
			if($result->num_rows > 0){
				$select= "<select name='formDoctor'>";
				while($rs = $result->fetch_assoc()){
					$select=$select.'<option value="'.$rs['BranchName'].'">'. $rs['BranchName'].'</option>';
				}
			}
			$select=$select.'</select>';
			echo $select;
		}
	?>
	
	
	<p>First name: <input type="text" name="FName" value = "" /></p>
	<p>Last name: <input type="text" name="LName" value = "" /></p>
	 
	<input type="submit" name="formSubmit" value="Submit" />
</form>

</body>
</html>
