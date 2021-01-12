DROP DATABASE IF EXISTS summerouting;

CREATE DATABASE IF NOT EXISTS summerouting;

CREATE TABLE IF NOT EXISTS summerouting.judgeonerecord(`ID` TINYINT, `Candidate` VARCHAR(30), `Popularity Tickets` TINYINT,
`Event Tickets` TINYINT, `Theme Wear` TINYINT, `Swim Wear` TINYINT, `Confidence` TINYINT,
`Audience Impact` TINYINT, `Total` TINYINT, UNIQUE (`ID`));

CREATE TABLE IF NOT EXISTS summerouting.judgetworecord(`ID` TINYINT, `Candidate` VARCHAR(30), `Popularity Tickets` TINYINT,
`Event Tickets` TINYINT, `Theme Wear` TINYINT, `Swim Wear` TINYINT, `Confidence` TINYINT,
`Audience Impact` TINYINT, `Total` TINYINT, UNIQUE (`ID`));

CREATE TABLE IF NOT EXISTS summerouting.judgethreerecord(`ID` TINYINT, `Candidate` VARCHAR(30), `Popularity Tickets` TINYINT,
`Event Tickets` TINYINT, `Theme Wear` TINYINT, `Swim Wear` TINYINT, `Confidence` TINYINT,
`Audience Impact` TINYINT, `Total` TINYINT, UNIQUE (`ID`));

CREATE TABLE IF NOT EXISTS summerouting.masterrecord(`ID` TINYINT, `Candidate` VARCHAR(30), `Popularity Tickets` TINYINT,
`Event Tickets` TINYINT, `Theme Wear` TINYINT, `Swim Wear` TINYINT, `Confidence` TINYINT,
`Audience Impact` TINYINT, `Total` TINYINT, UNIQUE (`ID`));

