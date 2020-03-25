-- phpMyAdmin SQL Dump
-- version 4.6.5.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: May 15, 2017 at 07:19 ÖS
-- Server version: 10.1.21-MariaDB
-- PHP Version: 5.6.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `Hospital`
--

DELIMITER $$
--
-- Procedures
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `future` (IN `BranchName` TEXT)  READS SQL DATA
if BranchName = "ALL" then
SELECT * FROM appointments WHERE appointments.date >= (SELECT CURDATE()) AND EXISTS (SELECT * FROM Doctors WHERE appointments.DoctorID = Doctors.ID);
else
SELECT * FROM appointments WHERE appointments.date >= (SELECT CURDATE()) AND EXISTS (SELECT * FROM Doctors WHERE appointments.DoctorID = Doctors.ID AND Doctors.Branch = BranchName);
end if$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `past` (IN `BranchName` TEXT)  READS SQL DATA
if BranchName = "ALL" then
SELECT * FROM appointments WHERE appointments.date < (SELECT CURDATE()) AND EXISTS (SELECT * FROM Doctors WHERE appointments.DoctorID = Doctors.ID);
else
SELECT * FROM appointments WHERE appointments.date < (SELECT CURDATE()) AND EXISTS (SELECT * FROM Doctors WHERE appointments.DoctorID = Doctors.ID AND Doctors.Branch = BranchName);
end if$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `appointments`
--

CREATE TABLE `appointments` (
  `ID` int(11) NOT NULL,
  `date` date NOT NULL,
  `time` time NOT NULL,
  `DoctorID` int(11) NOT NULL,
  `PatientID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `appointments`
--

INSERT INTO `appointments` (`ID`, `date`, `time`, `DoctorID`, `PatientID`) VALUES
(3, '2017-05-02', '14:15:00', 9, 3),
(4, '2017-02-15', '14:45:00', 9, 3),
(7, '2017-05-16', '13:00:00', 9, 2),
(8, '2017-05-24', '02:05:00', 10, 3),
(9, '2017-05-29', '02:00:00', 9, 3),
(10, '2017-05-23', '01:55:00', 10, 5),
(11, '2017-05-31', '15:00:00', 12, 3),
(12, '2017-05-31', '17:00:00', 12, 2);

-- --------------------------------------------------------

--
-- Table structure for table `Branches`
--

CREATE TABLE `Branches` (
  `ID` int(11) NOT NULL,
  `BranchName` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Branches`
--

INSERT INTO `Branches` (`ID`, `BranchName`) VALUES
(2, 'kbb'),
(5, 'Dahiliye'),
(6, 'ayak');

--
-- Triggers `Branches`
--
DELIMITER $$
CREATE TRIGGER `delDocs` AFTER DELETE ON `Branches` FOR EACH ROW DELETE FROM Doctors WHERE Doctors.Branch = old.BranchName
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `Doctors`
--

CREATE TABLE `Doctors` (
  `ID` int(11) NOT NULL,
  `Name` text NOT NULL,
  `Surname` text NOT NULL,
  `Branch` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Doctors`
--

INSERT INTO `Doctors` (`ID`, `Name`, `Surname`, `Branch`) VALUES
(9, 'ali', 'laz', 'kbb'),
(10, 'hakan', 'altan', 'Dahiliye'),
(12, 'SEFA', 'veli', 'ayak');

--
-- Triggers `Doctors`
--
DELIMITER $$
CREATE TRIGGER `docDeleted` AFTER DELETE ON `Doctors` FOR EACH ROW DELETE FROM appointments WHERE appointments.DoctorID = old.ID
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `ID` int(11) NOT NULL,
  `Username` text NOT NULL,
  `Password` text NOT NULL,
  `Role` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Holds admins (1) and patients (2) ';

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`ID`, `Username`, `Password`, `Role`) VALUES
(1, 'admin', 'admin', 1),
(2, 'user2', 'a', 2),
(3, 'user3', 'a', 2),
(4, 'ceyhun issiz', 'ssd', 2),
(5, 'abdullah kaz', 'a', 2);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `appointments`
--
ALTER TABLE `appointments`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `Branches`
--
ALTER TABLE `Branches`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `Doctors`
--
ALTER TABLE `Doctors`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `ID` (`ID`),
  ADD KEY `ID_2` (`ID`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `ID` (`ID`),
  ADD KEY `ID_2` (`ID`),
  ADD KEY `ID_3` (`ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `appointments`
--
ALTER TABLE `appointments`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;
--
-- AUTO_INCREMENT for table `Branches`
--
ALTER TABLE `Branches`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
--
-- AUTO_INCREMENT for table `Doctors`
--
ALTER TABLE `Doctors`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;
--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
