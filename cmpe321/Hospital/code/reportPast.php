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
		
		$branch = $_POST['selectBranch'];
		echo $branch . " ==>  ";

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
				

	
				//to do
				
				
							  //connect to database
				  //$connection = mysqli_connect("hostname", "user", "password", "db", "port");

				$sql = "call past('" . $branch  . "')";
				$result = 	$conn->query($sql);
				
				  //loop the result set
				  echo "<br>";
				while($rs = $result->fetch_assoc()){
					echo $rs['date']." ; ".$rs['time'] ."<br>";
				}

			}


			

			exit();
		}
	}
?>







<form action="<?php echo htmlentities($_SERVER['PHP_SELF']); ?>" method="post">
	<label for='formDoctor'>Select Branch</label><br>
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
			

			$result=$conn->query("SELECT BranchName FROM Branches");
			
			if($result->num_rows > 0){
				$select= "<select name='selectBranch'>" . '<option value="ALL">ALL</option>';
				while($rs = $result->fetch_assoc()){
					$select=$select.'<option value="'.$rs['BranchName'].'">'. $rs['BranchName'].'</option>';
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
