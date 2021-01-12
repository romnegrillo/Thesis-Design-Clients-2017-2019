INSERT INTO summerouting.judgeonerecord(`ID`,`Candidate`) 
VALUES 
(1,"SAMANTHA TANQUECO"),
(2,"BRIDALYN BEJERAS"),
(3,"CHRISTINE LOISSE ALBOS"),
(4,"DWIGHT TAGAPULOT"),
(5,"JOHN MEDINA"),
(6,"CHRYSTOPHER ONG"),
(7,"EARL ZUNEGA"),
(8,"CARL FRANCIS REYES"),
(9,"JUMARIE MOCON");

UPDATE summerouting.judgeonerecord SET `Popularity Tickets`=0 ,
`Event Tickets`=0,
`Theme Wear`=0,
`Swim Wear`=0,
`Confidence`=0,
`Audience Impact`=0,
`Total`=0
WHERE `ID`<=9;

INSERT INTO summerouting.judgetworecord SELECT * FROM summerouting.judgeonerecord;

INSERT INTO summerouting.judgethreerecord SELECT * FROM summerouting.judgeonerecord;

INSERT INTO summerouting.masterrecord SELECT * FROM summerouting.judgeonerecord;

SELECT * FROM summerouting.judgethreerecord;


