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
		
		$ID = $_POST['ID'];
		//echo $branch . " ==>  ";
		$errorMessage = "";
		
		if(empty($ID)) 
		{
			$errorMessage = "<li>You forgot to select a ID!</li>";
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
				
				
				// delete the record
                $sql = "DELETE FROM Doctors WHERE ID = " . $_POST['ID'];

                if ($conn->query($sql) === TRUE) {
                    echo "Done! <br />";
                    //echo "<a href = 'homepage_Hospital_pt.php'>Go to homepage</a>";
                } else {
                    echo "Error deleting record: " . $conn->error;
                }

			}


			

			exit();
		}
	}
?>







<form action="<?php echo htmlentities($_SERVER['PHP_SELF']); ?>" method="post">
	<p>Doctors ID : <input type="number" name="ID"/></p> 
	<input type="submit" name="formSubmit" value="Submit" />
</form>

</body>
</html>
