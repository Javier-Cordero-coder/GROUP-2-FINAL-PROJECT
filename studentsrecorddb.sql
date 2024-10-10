-- Create the database
CREATE DATABASE studentsrecorddb;

-- Select the database to use
USE studentsrecorddb;

-- Create the students table without AUTO_INCREMENT
CREATE TABLE `students` (
  `ID` int NOT NULL,
  `NAME` varchar(45) NOT NULL,
  `COURSE / PROGRAM` varchar(45) NOT NULL,
  `YEAR LEVEL` varchar(45) NOT NULL,
  `AGE` varchar(45) NOT NULL,
  `SEX` varchar(45) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

