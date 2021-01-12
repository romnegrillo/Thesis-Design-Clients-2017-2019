CREATE DATABASE IF NOT EXISTS flower;

CREATE TABLE IF NOT EXISTS flower.users(`Username` VARCHAR(30), `Password` VARCHAR(30), UNIQUE(`Username`));
INSERT INTO flower.users(`Username`, `Password`) VALUES ("admin", "admin");

CREATE TABLE IF NOT EXISTS flower.flowerpath(`Flower ID` INT, `Flower Name` VARCHAR(30), 
`Flower Image Path`VARCHAR(240), `Mask Image Path` VARCHAR(240), UNIQUE(`Flower ID`));

SELECT * FROM flower.users;