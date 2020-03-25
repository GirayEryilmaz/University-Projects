<html>
    <head>
        <title>CMPE Students</title>
    </head>
    <body>

        <?php
            $servername = "localhost";
            $username = "root";
            $password = "";
            $dbname = "CMPE";

            // Create connection
            $conn = new mysqli($servername, $username, $password, $dbname);

            // Check connection
            if ($conn->connect_error) {

                die("Connection failed: " . $conn->connect_error);
            }else{
				
            ?>
			
			

            <?php
            
           
            
            }
            $conn->close();
        ?>

    </body>
</html>
