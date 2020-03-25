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
				
				session_start();
                ?>

                <!--<a href = "create_student.php">Create a new record</a><br /> -->

                <?php

                // List records
                $sql = "SELECT * FROM appointments WHERE PatientID = " . $_SESSION['userID'];	
            
                $result = $conn->query($sql);

                if ($result->num_rows > 0) {
                    echo $result->num_rows;
                    
                    
                    
                    ?>
                    <table border = 1>
                        <tr>
                            <th>Operations</th>
                            <th>Doctor</th>
                            <th>Date</th>
                            <th>Time</th>                         
                    <?php

                    // output data of each row
                    while($row = $result->fetch_assoc()) {
						$sql2 = "SELECT Name, Surname FROM Doctors WHERE ID =  " . $row["DoctorID"];
						$temp = $conn->query($sql2);
						$doc = $temp->fetch_assoc();
						//$docName = $doc[Name] . 
                        ?>
                        <tr>
                            <td>
								<a href = "cancelApp.php?id=<?php echo $row["ID"]; ?>"><img src = "img/delete.png" alt = "Cancel" /></a>
                                <a href = "editApp.php?id=<?php echo $row["ID"]; ?>"><img src = "img/edit.png" alt = "Edit" /></a>
                            </td>
                            <td><?php echo $doc["Name"] . " " . $doc["Surname"]; ?></td>
                            <td><?php echo $row["date"]; ?></td>
                            <td><?php echo $row["time"]; ?></td>                           
                        </tr>
                        <?php
                    }

                    ?>
                    </table>
                    <?php
                } else {
                    echo "The table is empty";
                }
            }
            $conn->close();
        ?>

    </body>
</html>
