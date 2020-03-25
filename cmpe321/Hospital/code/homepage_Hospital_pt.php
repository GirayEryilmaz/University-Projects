<html>
    <head>
        <title>Home Page</title>
    </head>
    <body>
      <?php
        session_start();

        if (!isset($_SESSION['username'])) {
          $msg = "Please <a href = 'http://localhost/Hospital/login_Hospital.php'>log in</a> to view this page";
          echo $msg;
        }else{
      ?>
        Welcome, fellow patient <? echo $_SESSION['username'] ?>. <br />

        

        Click <a href = "http://localhost/Hospital/logout_Hospital.php">here</a> to log out. <br>
        <a href = "http://localhost/Hospital/select_Branch.php">New Appointment</a>. <br>
		<a href = "http://localhost/Hospital/showApps.php">Show appointments</a>. <br>
        <!--<a href = "http://localhost/Hospital/logout_Hospital.php">Edit Appointment</a>.<br> -->


      <?
        }
      ?>
    </body>
</html>
