DROP DATABASE IF EXISTS webert_database;
CREATE DATABASE IF NOT EXISTS webert_database;
USE webert_database;

CREATE TABLE webert_database.employee_info(
`Employee ID` INT, 
`Last Name` VARCHAR(30), 
`Given Name` VARCHAR(30), 
`Middle Name` VARCHAR(30),
`Age` SMALLINT, 
`Sex` VARCHAR(6), 
`Home Address` VARCHAR(100), 
`Contact Number` VARCHAR(30),
`Marital Status` VARCHAR(30), 
`Contact Person` VARCHAR(50),
 `Relationship` VARCHAR(30),  
`Contact Person Number` VARCHAR(30),
 `Number of Finger` SMALLINT,
 UNIQUE(`Employee ID`));
 
 CREATE TABLE webert_database.employee_fingerid(
 `Employee ID` INT, 
`Last Name` VARCHAR(30), 
`Given Name` VARCHAR(30), 
`Middle Name` VARCHAR(30),
`Finger 1` SMALLINT,
`Finger 2` SMALLINT,
`Finger 3` SMALLINT,
`Finger 4` SMALLINT,
UNIQUE(`Employee ID`));

CREATE TABLE webert_database.employee_attendance(
`Attendance ID` INT,
`Employee ID` INT, 
`Last Name` VARCHAR(30), 
`Given Name` VARCHAR(30), 
`Middle Name` VARCHAR(30),
`Date` VARCHAR(10),
`Time In` VARCHAR(8),
`Time Out` VARCHAR(8),
`Remarks` VARCHAR(30),
`Over Time Hours` INT,
UNIQUE(`Attendance ID`));

CREATE TABLE webert_database.employee_workstatus(
 `Employee ID` INT, 
`Last Name` VARCHAR(30), 
`Given Name` VARCHAR(30), 
`Middle Name` VARCHAR(30),
`Work Status` VARCHAR(30),
UNIQUE(`Employee ID`));

CREATE TABLE webert_database.availablefinger(`Finger ID` INT, 
`Availability` VARCHAR(3),
UNIQUE(`Finger ID`));

CREATE TABLE webert_database.employee_salaryinfo(
`ID` INT, `Full Time Salary` INT, 
`Half Time Salary` INT,
`Over Time Hourly Rate` INT,
UNIQUE(`ID`)); 

CREATE TABLE webert_database.salaryreport(
`Employee ID` INT,
`Last Name` VARCHAR(30),
`Given Name` VARCHAR(30),
`Middle Name` VARCHAR(30),
`Number of Full Time Days` INT,
`Number of Half Time Days` INT,
`Number of Over Time Days` INT,
`Salary` INT,
UNIQUE(`Employee ID`));

CREATE TABLE webert_database.admininfo(
`ID` INT,
`Username` VARCHAR(30),
`Password` VARCHAR(30));

INSERT INTO webert_database.admininfo(`ID`,
`Username`,`Password`) VALUES(1,'admin','admin');

INSERT INTO webert_database.employee_salaryinfo(
`ID`,`Full Time Salary`, `Half Time Salary`, `Over Time Hourly Rate`)
VALUES(1,350,200,100);

DELIMITER $$
	CREATE PROCEDURE webert_database.PopulateFingerID()
		BEGIN
			DECLARE CTR INT;
            SET CTR=1;
            
            WHILE CTR<=127 DO
				INSERT INTO webert_database.availablefinger(`Finger ID`, `Availability`) VALUES(CTR,'Yes');
                SET CTR=CTR+1;
            END WHILE;
            
		END $$
DELIMITER ;

CALL webert_database.PopulateFingerID;

/*

FTCount

SELECT COUNT(*) FROM webert_database.employee_attendance WHERE `Employee ID`=3 AND
STR_TO_DATE(`Date`, "%m/%d/%Y") 
BETWEEN STR_TO_DATE('08/01/2018', "%m/%d/%Y") AND STR_TO_DATE('08/08/2018', "%m/%d/%Y")
AND `Remarks`='Full Time' ORDER BY STR_TO_DATE(`Date`, "%m/%d/%Y") ASC;

HTCount

SELECT COUNT(*) FROM webert_database.employee_attendance WHERE `Employee ID`=3 AND
STR_TO_DATE(`Date`, "%m/%d/%Y") 
BETWEEN STR_TO_DATE('08/01/2018', "%m/%d/%Y") AND STR_TO_DATE('08/08/2018', "%m/%d/%Y")
AND `Remarks`='Half Time' ORDER BY STR_TO_DATE(`Date`, "%m/%d/%Y") ASC;

OTCount
SELECT COUNT(*) FROM webert_database.employee_attendance WHERE `Employee ID`=3 AND
STR_TO_DATE(`Date`, "%m/%d/%Y") 
BETWEEN STR_TO_DATE('08/01/2018', "%m/%d/%Y") AND STR_TO_DATE('08/08/2018', "%m/%d/%Y")
AND `Remarks`='Over Time' ORDER BY STR_TO_DATE(`Date`, "%m/%d/%Y") ASC;

sumOT
SELECT SUM(`Over Time Hours`) FROM webert_database.employee_attendance WHERE `Employee ID`=3 AND
STR_TO_DATE(`Date`, "%m/%d/%Y") 
BETWEEN STR_TO_DATE('08/01/2018', "%m/%d/%Y") AND STR_TO_DATE('08/08/2018', "%m/%d/%Y")
AND `Remarks`='Half Time' ORDER BY STR_TO_DATE(`Date`, "%m/%d/%Y") ASC;

salary=FTCount*FTSalary+HTCount+HTSalary+OTCount*FTSalary+sumOT*OThourlyRate;

/*