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
				
				
				
                // Update the record
                $sql = "DELETE FROM appointments WHERE ID = " . $_POST['ID'];

                if ($conn->query($sql) === TRUE) {
                    echo "Done! <br />";
                    echo "<a href = 'homepage_Hospital_pt.php'>Go to homepage</a>";
                } else {
                    echo "Error deleting record: " . $conn->error;
                }
            }
            $conn->close();
        ?>

    </body>
</html>
