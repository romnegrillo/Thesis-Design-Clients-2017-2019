DROP DATABASE IF EXISTS filerecorder;

CREATE DATABASE filerecorder;

CREATE TABLE filerecorder.records(`File ID` INT, `File Name` VARCHAR(240), 
`Uploader` VARCHAR(100), `Date Uploaded` VARCHAR(10), UNIQUE(`File ID`));

CREATE TABLE filerecorder.users(`Faculty ID` INT, `Username` VARCHAR(240), `Password` VARCHAR(30),
`First Name` VARCHAR(30), `Last Name` VARCHAR(30), `Account Type` VARCHAR(5), UNIQUE(`Faculty ID`));

SELECT * FROM filerecorder.records;
SELECT * FROM filerecorder.users;
