<html>
    <head>
        <title>Home Page</title>
    </head>
    <body>
      <?php
        session_start();
        
        if(!isset($_SESSION['Role']) or  $_SESSION['Role']!=1){
			echo $_SESSION['Role'];
			echo $_SESSION['Role'];
			die("unauthorized access");
		}

        if (!isset($_SESSION['username'])) {
          $msg = "Please <a href = 'http://localhost/Hospital/login_Hospital.php'>log in</a> to view this page";
          echo $msg;
        }else{
      ?>
        Welcome, <? echo $_SESSION['username'] ?>.

        <br />

        Click 	<a href = "http://localhost/Hospital/logout_Hospital.php">here</a> to log out. <br>
				<a href = "http://localhost/Hospital/removeDoctor.php">remove</a> to remove a Doctor out. <br>
				<a href = "http://localhost/Hospital/addDoctor.php">addDoc</a> to add a new doc. <br>
				<a href = "http://localhost/Hospital/editDoc.php">edit</a> to edit a doc. <br>
				<a href = "http://localhost/Hospital/reportPast.php">report past</a> . <br>
				<a href = "http://localhost/Hospital/reportFuture.php">report future</a> .<br>
				<a href = "http://localhost/Hospital/addBranch.php">addBranch</a> to add a new Branch. <br>
				<a href = "http://localhost/Hospital/removeBranch.php">removeBranch</a> to remove Branch. <br>
				<a href = "http://localhost/Hospital/editBranch.php">editBranch</a> to edit Branch. <br>

      <?
        }
      ?>
    </body>
</html>
