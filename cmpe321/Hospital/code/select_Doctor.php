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
	if(isset($_POST['formSubmit'])) 
	{
		//echo $_POST['formSubmit'];
		$doctorID = $_POST['formDoctor'];
		$errorMessage = "";
		
		if(empty($doctorID)) 
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
			
			echo "going ". $doctorID;
			session_start();
			$_SESSION['chosen_doctorID']  = $doctorID;
			
			//dynamic redirect
			header("Location:schedule.php");
			

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
			
			session_start();
			$branch = $_SESSION['chosen_branch'] ;


			//query 
			$result=$conn->query("SELECT *  FROM Doctors WHERE Branch = '" . $branch . "'"  );
			//echo "SELECT *  FROM Doctors WHERE Branch = ' " . $branch . "'"  ;
			
			if($result->num_rows > 0){
				$select= "<select name='formDoctor'>";
				while($rs = $result->fetch_assoc()){
					$select=$select.'<option value="'.$rs['ID'].'">'. $rs['Name']. ' '. $rs['Surname'] .'</option>';
				}
			}
			$select=$select.'</select>';
			echo $select;
		}
	?>
	
	
	
	 
	<input type="submit" name="formSubmit" value="Submit" />
</form>

</body>
</html>
