<!DOCTYPE HTML PUBLIC ""> 
<html>
<head>
	<title>PHP form select box example</title>
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
		$branch = $_POST['formBranch'];
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
			
			session_start();
			$_SESSION['chosen_branch'] = $branch;
			echo "going ". $Doctor;
					
			//dynamic redirect
			header("Location:select_Doctor.php");
			// end method 2

			exit();
		}
	}
?>







<form action="<?php echo htmlentities($_SERVER['PHP_SELF']); ?>" method="post">
	<label for='formBranch'>Select Branch</label><br>
	
	
	
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
			
			//query
			$result=$conn->query("SELECT DISTINCT Branch  FROM Doctors");

			if($result->num_rows > 0){
				$select= '<select name="formBranch">';
				while($rs = $result->fetch_assoc()){
					$select=$select.'<option value="'.$rs['Branch'].'">'. $rs['Branch'] .'</option>';
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
