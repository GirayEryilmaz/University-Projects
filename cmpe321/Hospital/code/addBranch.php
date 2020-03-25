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
		
		$branch = $_POST['branch'];
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
				
				
				$sql = "SELECT ID FROM Branches WHERE BranchName = '". $branch ."'";
				

				if ($conn->query($sql) === TRUE) {
					die("branch already exists");
					
				}else{
					
				
				
					$sql = "INSERT INTO Branches (BranchName) VALUES('" . $branch  . "')";
					

					if ($conn->query($sql) === TRUE) {
						echo "Branch added <br />";
						//$msg = "Please <a href = 'http://localhost/Hospital/login_Hospital.php'>log in</a> to make an appointment <br />";
						//echo $msg;
						
					} else {
						echo "Error while registering to the system: " . $conn->error;
					}
					
				}

			}


			

			exit();
		}
	}
?>







<form action="<?php echo htmlentities($_SERVER['PHP_SELF']); ?>" method="post">
	<p>new Branch: <input type="text" name="branch" /></p>	 
	<input type="submit" name="formSubmit" value="Submit" />
</form>

</body>
</html>
