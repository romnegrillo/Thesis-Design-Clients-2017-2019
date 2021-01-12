CREATE DATABASE IF NOT EXISTS thesisrecorder;

CREATE TABLE IF NOT EXISTS thesisrecorder.users(`Username` VARCHAR(30),
`Password` VARCHAR(30), `Type` VARCHAR(10), UNIQUE(`Username`));

CREATE TABLE IF NOT EXISTS thesisrecorder.thesisrecord(`ID` INT, `Title` VARCHAR(100), 
`Program` VARCHAR(10), `Category` VARCHAR(30), `Date Added` VARCHAR(10), `File Name` VARCHAR(50), UNIQUE(`ID`));

CREATE TABLE IF NOT EXISTS thesisrecorder.thesispending(`ID` INT, `Title` VARCHAR(100), 
`Program` VARCHAR(10), `Category` VARCHAR(30), `Date Added` VARCHAR(10), `File Name` VARCHAR(50), UNIQUE(`ID`));

INSERT INTO thesisrecorder.users(`Username`, `Password`, `Type`) VALUES("admin", 1234, "Admin"); 

INSERT INTO thesisrecorder.thesisrecord(`ID`,`Title`, `Program`,`Category`, `Date Added`, `File Name`)
VALUES(1,"Pig Weight Estimation Using Image Processing Techniques", "CpE", "Image Processing","06/03/2018", "MyFile");

SELECT * FROM thesisrecorder.thesisrecord;
