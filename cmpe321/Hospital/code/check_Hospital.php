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
		$id = $_POST["id"];
		$pass = $_POST["pass"];
		
		//$sql = "SELECT Username,Role,ID FROM users WHERE Username = '" . $id . "' AND Password = '" . $pass . "' " ;
		
		//$result = $conn->query($sql);
		
		$stmt = $conn->prepare("SELECT Username,Role,ID FROM users WHERE Username = ? AND Password = ?");
		$stmt->bind_param('ss', $id,$pass);

		$stmt->execute();

		$result = $stmt->get_result();
		
		if ($result->num_rows > 0) {
			session_start();
			$_SESSION['username'] = $id;
			
			$row = $result->fetch_assoc();
			if($row['Role'] == 1){
				$_SESSION['Role'] = $row['Role'];
				header("Location:http://localhost/Hospital/homepage_Hospital_Admin.php");
				die();
			
			}else if($row['Role'] == 2){
				$_SESSION['userID'] = $row['ID'];

				header("Location:http://localhost/Hospital/homepage_Hospital_pt.php");
				die();
				
			}
			
				
			
			
			
		}else{
			$conn->close();
			
			?>
			
			Wrong username or password. <br> Click <a href = "http://localhost/Hospital/logout_Hospital.php">here</a> to go back to login page.
			
			<?
			
			die("Wrong username or password");
			
			
		
		}
	}


?>
