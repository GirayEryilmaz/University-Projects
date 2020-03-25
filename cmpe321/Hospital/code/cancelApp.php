<html>
    <head>
        <title>Hospital</title>
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
				
				
                // Fetch the record
                $sql = "SELECT * FROM appointments WHERE ID = " . $_GET['id'];
                $result = $conn->query($sql);
                
                session_start();
                
              

                // If the record actually exists
                if ($result->num_rows > 0) {
                    //echo $result->num_rows;
                    ?>
                    <form action="cancelApp_result.php" method="post">
                    <?php

                    // Get the data
                    $row = $result->fetch_assoc();
                    
                    if($row["PatientID"] != $_SESSION['userID']){
						die("unauthorised!");
					}
                    
                    $sql2 = "SELECT Name, Surname FROM Doctors WHERE ID =  " . $row["DoctorID"];
					$temp = $conn->query($sql2);
					$doc = $temp->fetch_assoc();
                    
                    ?>
                        Are you sure you want to cancel the appointment? <br />
                        <p>Doctor: <input type="text" name="doctor" value = "<?php echo $doc["Name"].  " ". $doc["Surname"] ?>" readonly /></p>
                        <p>Date: <input type="text" name="Date" value = "<?php echo $row["date"] ?>" readonly /></p>
                        <p>Time: <input type="text" name="Time" value = "<?php echo $row["time"] ?>" readonly /></p>
                        <p><input type="hidden" name="ID" value = "<?php echo $row["ID"] ?>" /></p>
                        <p><input type="submit" value = "cancelApp" /></p>
                    </form>
                    <?php
                } else {
                    echo "Record does not exist";
                }
            }
            $conn->close();
        ?>

    </body>
</html>
