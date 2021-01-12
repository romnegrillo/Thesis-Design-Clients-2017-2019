USE webert_database;

TRUNCATE webert_database.employee_info;
TRUNCATE webert_database.employee_fingerid;
TRUNCATE webert_database.employee_attendance;
TRUNCATE webert_database.employee_workstatus;
TRUNCATE webert_database.availablefinger;
TRUNCATE webert_database.employee_salaryinfo;
TRUNCATE webert_database.salaryreport;
TRUNCATE webert_database.admininfo;

INSERT INTO webert_database.admininfo(`ID`,
`Username`,`Password`) VALUES(1,'admin','admin');

INSERT INTO webert_database.employee_salaryinfo(
`ID`,`Full Time Salary`, `Half Time Salary`, `Over Time Hourly Rate`,`Late Time Salary`)
VALUES(1,350,200,100,305);

CALL webert_database.PopulateFingerID;

