using System;
using System.Data;
using System.Windows.Forms;
using MySql.Data.MySqlClient;

namespace Webert
{
    class WebertSqlClass
    {
        private string connectionString = "datasource=localhost;port=3306;username=root;password=toor;database=webert_database";
        private MySqlConnection dbConnection;
        public static string attendanceDateShown="1";
        public static string currentName = "-";
        public static string currentAct = "-";
        
        public WebertSqlClass()
        {
            connectDatabase();
            loadUserSettings();

        }

        private void connectDatabase()
        {
            dbConnection = new MySqlConnection(connectionString);
            dbConnection.Open();
        }

        private void loadUserSettings()
        {
            string query = "SELECT `Full Time Salary`, `Half Time Salary`, " +
                "`Over Time Hourly Rate`, `Late Time Salary` FROM webert_database.employee_salaryinfo " +
                "WHERE `ID`=1;";

            MySqlCommand dbCommand = new MySqlCommand(query, dbConnection);
            MySqlDataReader dbReader = dbCommand.ExecuteReader();

            if(dbReader.HasRows)
            {
                dbReader.Read();

                WebertEmployeeClass.FTSalary = int.Parse(dbReader.GetString(0));
                WebertEmployeeClass.HTSalary = int.Parse(dbReader.GetString(1));
                WebertEmployeeClass.OTRate = int.Parse(dbReader.GetString(2));
                WebertEmployeeClass.LateSalary = int.Parse(dbReader.GetString(3));
            }
            else
            {
                MessageBox.Show("No salary info recorded! Please fill it out!",
                    "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }

            dbReader.Close();
        }

        public void closeDatabase()
        {
            dbConnection.Close();
        }

        // DataTable getter functions is used to be the source of data grid view's data.

        public DataTable getAttendanceInfoTable()
        {
            string query = "SELECT `Attendance ID`,`Employee ID`,`Date`,`Time In`,`Lunch Time`,`Time Out`,`Remarks`,`Over Time Hours` from webert_database.employee_attendance WHERE `Date`=@1;";
            
            if(attendanceDateShown=="1")
            {
                query = "SELECT `Attendance ID`,`Employee ID`,`Date`,`Time In`,`Lunch Time`,`Time Out`,`Remarks`,`Over Time Hours` from webert_database.employee_attendance;";

            }

            MySqlCommand dbCommand = new MySqlCommand(query, dbConnection);
            dbCommand.Parameters.AddWithValue("@1", attendanceDateShown);
            MySqlDataAdapter dbAdapter = new MySqlDataAdapter(dbCommand);
            DataTable dbDataTable = new DataTable();

            dbAdapter.Fill(dbDataTable);

            return dbDataTable;
        }

        public DataTable getEmployeeInfoTable()
        {
            string query = "SELECT * from webert_database.employee_info;";

            MySqlCommand dbCommand = new MySqlCommand(query, dbConnection);
            MySqlDataAdapter dbAdapter = new MySqlDataAdapter(dbCommand);
            DataTable dbDataTable = new DataTable();

            dbAdapter.Fill(dbDataTable);

            return dbDataTable;
        }

        public DataTable getWorkStatusInfoTable()
        {
            string query = "SELECT `Employee ID`,`Work Status` FROM webert_database.employee_workstatus";

            MySqlCommand dbCommand = new MySqlCommand(query, dbConnection);
            MySqlDataAdapter dbAdapter = new MySqlDataAdapter(dbCommand);
            DataTable dbDataTable = new DataTable();

            dbAdapter.Fill(dbDataTable);

            return dbDataTable;
        }

        public DataTable getSalaryReportInfoTable()
        {
            string query = "SELECT `Employee ID`,`Number of Full Time Days`,`Number of Half Time Days`,`Number of Over Time Hours`,`Salary` FROM webert_database.salaryreport;";
            MySqlCommand dbCommand = new MySqlCommand(query, dbConnection);
            MySqlDataAdapter dbAdapter = new MySqlDataAdapter(dbCommand);
            DataTable dbDataTable = new DataTable();

            dbAdapter.Fill(dbDataTable);

            return dbDataTable;
        }

        public void addEmployee(params object[] items)
        {
            // Query for adding.
            string query = "INSERT INTO webert_database.employee_info(" +
                "`Employee ID`,`Last Name`, `Given Name`, `Middle Name`, " +
                "`Age`, `Sex`, `Home Address`, `Contact Number`, " +
                "`Marital Status`, `Contact Person`, `Relationship`, " +
                "`Contact Person Number`, `Number of Finger`) " +
                "VALUES(@1,@2,@3,@4,@5,@6,@7,@8,@9,@10,@11,@12,@13)";

            // Query for getting number of current employees.
            // Next employee id will be this + 1.
            string queryNumEmployee = "SELECT `Employee ID` FROM webert_database.employee_info ORDER BY " +
                "`Employee ID` DESC";
            MySqlCommand queryNumEmployeeCommand = new MySqlCommand(queryNumEmployee, dbConnection);
            MySqlDataReader queryEmployeeDataReader = queryNumEmployeeCommand.ExecuteReader();
            int numEmployee = 1;

            if (queryEmployeeDataReader.HasRows)
            {
                queryEmployeeDataReader.Read();
                numEmployee = int.Parse(queryEmployeeDataReader.GetString(0));
                numEmployee++;
            }

            // You need to close MySqlDataReader object to execute another query using
            // other MySql objects.
            queryEmployeeDataReader.Close();

            // Static employee ID
            // This needs to be static since it is created on WebertSqlClass
            WebertEmployeeClass.employeeID = numEmployee;

            // MessageBox.Show(numEmployee.ToString());

            MySqlCommand dbCommand = new MySqlCommand(query, dbConnection);
            dbCommand.Parameters.AddWithValue("@1", numEmployee);
            dbCommand.Parameters.AddWithValue("@2", items[0]);
            dbCommand.Parameters.AddWithValue("@3", items[1]);
            dbCommand.Parameters.AddWithValue("@4", items[2]);
            dbCommand.Parameters.AddWithValue("@5", items[3]);
            dbCommand.Parameters.AddWithValue("@6", items[4]);
            dbCommand.Parameters.AddWithValue("@7", items[5]);
            dbCommand.Parameters.AddWithValue("@8", items[6]);
            dbCommand.Parameters.AddWithValue("@9", items[7]);
            dbCommand.Parameters.AddWithValue("@10", items[8]);
            dbCommand.Parameters.AddWithValue("@11", items[9]);
            dbCommand.Parameters.AddWithValue("@12", items[10]);
            dbCommand.Parameters.AddWithValue("@13", items[11]);

            dbCommand.ExecuteNonQuery();

            addWorkStatus(numEmployee, items[0], items[1], items[2]);
         
        }


        // This function is used along with adding new employee
        // since they will have a work status as well.

        private void addWorkStatus(params object[] items)
        {
            //string query = "INSERT INTO webert_database.employee_workstatus(" +
            //   "`Employee ID`, `Last Name`, `Given Name`, `Middle Name`, " +
            //   "`Work Status`) VALUES(@1,@2,@3,@4,@5)";

            string query = "INSERT INTO webert_database.employee_workstatus(" +
               "`Employee ID`, "+
               "`Work Status`) VALUES(@1,@5)";

            MySqlCommand dbCommand = new MySqlCommand(query, dbConnection);

            //MessageBox.Show(items[0].ToString());
           // MessageBox.Show(items[1].ToString());
           // MessageBox.Show(items[2].ToString());
            //MessageBox.Show(items[3].ToString());

            dbCommand.Parameters.AddWithValue("@1", items[0]);

            dbCommand.Parameters.AddWithValue("@5", "Full Time"); // Full time by default.

            dbCommand.ExecuteNonQuery();
        }

        // Used in adding employee as well, first we need to get
        // finger ids depending on how many fingers is need to registered.
        // Then we set all of that finger ID to be used to 'No'
        // and we will pass those IDs to atmega and finger print scanner.

        public int[] getAvailableFinger(int numberOfFinger)
        {
            String query = "SELECT `Finger ID` FROM webert_database.availablefinger WHERE `Availability`='Yes' " +
                "ORDER BY `Finger ID` LIMIT @1";
            MySqlCommand dbCommand = new MySqlCommand(query, dbConnection);
            dbCommand.Parameters.AddWithValue("@1", numberOfFinger);
            MySqlDataReader dbReader = dbCommand.ExecuteReader();

            int target = numberOfFinger;
            bool isComplete = true;
            int[] returnAvailable = new int[target];

            for (int i = 0; i < target; i++)
            {
                if (dbReader.HasRows)
                {
                    dbReader.Read();
                    returnAvailable[i] = int.Parse(dbReader.GetString(0));
                    //MessageBox.Show("Available: " + returnAvailable[i].ToString(), "Debug");
                }
                else
                {
                    isComplete = false;
                }
            }

            dbReader.Close();

            if(isComplete)
            {
                // Will move the code below to update the database only when the fingerprint
                // is registed to the scanner.

                //for(int i=0; i<target; i++)
                //{
                //    query = "UPDATE webert_database.availablefinger SET `Availability`='No' " +
                //   "WHERE `Finger ID`=@1";

                //    dbCommand = new MySqlCommand(query, dbConnection);
                //    dbCommand.Parameters.AddWithValue("@1", returnAvailable[i]);
                //    dbCommand.ExecuteNonQuery();
                //}

                return returnAvailable;
            }

            int[] notValid = { 0, 0, 0, 0 };

            return notValid;
        }

        public void updateFingerList(int[] fingerList)
        {
            MySqlCommand dbCommand;
            
            for (int i = 0; i < fingerList.Length; i++)
            {
               string query = "UPDATE webert_database.availablefinger SET `Availability`='No' " +
               "WHERE `Finger ID`=@1";

                dbCommand = new MySqlCommand(query, dbConnection);
                dbCommand.Parameters.AddWithValue("@1", fingerList[i]);
                dbCommand.ExecuteNonQuery();
            }
        }

        // Used in adding employee also, when the available finger id is updated and
        // and the employee table is updated, we then update register those availble finger to
        // the employee.

        public void addFingerToEmployee(params object[] items)
        {
            string query = "INSERT INTO webert_database.employee_fingerid(`Employee ID`, " +
         
                "`Finger 1`, " +
                "`Finger 2`, " +
                "`Finger 3`, " +
                "`Finger 4`) " +
                "VALUES(@1,@5,@6,@7,@8)";

            MySqlCommand dbCommand = new MySqlCommand(query, dbConnection);
            dbCommand.Parameters.AddWithValue("@1", items[0]);
       
            dbCommand.Parameters.AddWithValue("@5", items[4]);
            dbCommand.Parameters.AddWithValue("@6", items[5]);
            dbCommand.Parameters.AddWithValue("@7", items[6]);
            dbCommand.Parameters.AddWithValue("@8", items[7]);
            dbCommand.ExecuteNonQuery();
        }

        public void editEmployee(params object[] items)
        {
            string query = "UPDATE webert_database.employee_info SET " +
                "`Last Name`=@1, " +
                "`Given Name`=@2, " +
                "`Middle Name`=@3, " +
                "`Age`=@4, " +
                "`Sex`=@5, " +
                "`Home Address`=@6, " +
                "`Contact Number`=@7, " +
                "`Marital Status`=@8, " +
                "`Contact Person`=@9, " +
                "`Relationship`=@10, " +
                "`Contact Person Number`=@11 " +
                "WHERE `Employee ID`=@12";

            MySqlCommand dbCommand = new MySqlCommand(query, dbConnection);

            dbCommand.Parameters.AddWithValue("@1", items[0]);
            dbCommand.Parameters.AddWithValue("@2", items[1]);
            dbCommand.Parameters.AddWithValue("@3", items[2]);
            dbCommand.Parameters.AddWithValue("@4", items[3]);
            dbCommand.Parameters.AddWithValue("@5", items[4]);
            dbCommand.Parameters.AddWithValue("@6", items[5]);
            dbCommand.Parameters.AddWithValue("@7", items[6]);
            dbCommand.Parameters.AddWithValue("@8", items[7]);
            dbCommand.Parameters.AddWithValue("@9", items[8]);
            dbCommand.Parameters.AddWithValue("@10", items[9]);
            dbCommand.Parameters.AddWithValue("@11", items[10]);
            dbCommand.Parameters.AddWithValue("@12", items[11]);
   

            dbCommand.ExecuteNonQuery();

            //MessageBox.Show(items[12].ToString());
            //MessageBox.Show(items[0].ToString());
            //MessageBox.Show(items[1].ToString());
            //MessageBox.Show(items[2].ToString());

           // editWorkStatus((int)(items[11]),
           //     items[0].ToString(), items[1].ToString(), items[2].ToString());
           // editAttendanceDetails((int)(items[11]),
          //      items[0].ToString(), items[1].ToString(), items[2].ToString());
           // editEmployeeFinger((int)(items[11]),
            //    items[0].ToString(), items[1].ToString(), items[2].ToString());
        }

        private void editWorkStatus(int empID, string lName, string gName, string mName)
        {
            string query = "UPDATE webert_database.employee_workstatus SET " +
                "`Last Name`=@1, " +
                "`Given Name`=@2, " +
                "`Middle Name`=@3 " +
                "WHERE `Employee ID`=@4;";

            //MessageBox.Show(empID.ToString());
            //MessageBox.Show(lName);
            //MessageBox.Show(gName);
            //MessageBox.Show(mName);

            MySqlCommand dbCommand = new MySqlCommand(query, dbConnection);
            dbCommand.Parameters.AddWithValue("@1", lName);
            dbCommand.Parameters.AddWithValue("@2", gName);
            dbCommand.Parameters.AddWithValue("@3", mName);
            dbCommand.Parameters.AddWithValue("@4", empID);

            //MessageBox.Show(dbCommand.ToString());
            dbCommand.ExecuteNonQuery();
        }

        private void editAttendanceDetails(int empID, string lName, string gName, string mName)
        {
            string query = "UPDATE webert_database.employee_attendance SET " +
                "`Last Name`=@1, " +
                "`Given Name`=@2, " +
                "`Middle Name`=@3 " +
                "WHERE `Employee ID`=@4;";

           // MessageBox.Show(empID.ToString());
            //MessageBox.Show(lName);
            //MessageBox.Show(gName);
            //MessageBox.Show(mName);

            MySqlCommand dbCommand = new MySqlCommand(query, dbConnection);
            dbCommand.Parameters.AddWithValue("@1", lName);
            dbCommand.Parameters.AddWithValue("@2", gName);
            dbCommand.Parameters.AddWithValue("@3", mName);
            dbCommand.Parameters.AddWithValue("@4", empID);
            dbCommand.ExecuteNonQuery();
        }

        private void editEmployeeFinger(int empID, string lName, string gName, string mName)
        {
            string query = "UPDATE webert_database.employee_fingerid SET " +
                "`Last Name`=@1, " +
                "`Given Name`=@2, " +
                "`Middle Name`=@3 " +
                "WHERE `Employee ID`=@4;";

            //MessageBox.Show(empID.ToString());
            //MessageBox.Show(lName);
           // MessageBox.Show(gName);
           // MessageBox.Show(mName);

            MySqlCommand dbCommand = new MySqlCommand(query, dbConnection);
            dbCommand.Parameters.AddWithValue("@1", lName);
            dbCommand.Parameters.AddWithValue("@2", gName);
            dbCommand.Parameters.AddWithValue("@3", mName);
            dbCommand.Parameters.AddWithValue("@4", empID);
            dbCommand.ExecuteNonQuery();
        }

        public void deleteEmployee(int employeeID)
        {
            string query = "DELETE FROM webert_database.employee_info WHERE `Employee ID`=@1";
            MySqlCommand dbCommand = new MySqlCommand(query, dbConnection);
            dbCommand.Parameters.AddWithValue("@1", employeeID);
            dbCommand.ExecuteNonQuery();

            deleteWorkStatus(employeeID);
            deleteAttendance(employeeID);
            restoreFingerID(employeeID);
            deleteFingerFromEmployee(employeeID);
        }

        // This function is used along with delete employee 
        // since deleteing an employee will also delete their work status.

        private void deleteWorkStatus(int employeeID)
        {
            string query = "DELETE FROM webert_database.employee_workstatus WHERE `Employee ID`=@1";
            MySqlCommand dbCommand = new MySqlCommand(query, dbConnection);
            dbCommand.Parameters.AddWithValue("@1", employeeID);
            dbCommand.ExecuteNonQuery();
        }

        private void deleteAttendance(int employeeID)
        {
            string query = "DELETE FROM webert_database.employee_attendance WHERE `Employee ID`=@1";
            MySqlCommand dbCommand = new MySqlCommand(query, dbConnection);
            dbCommand.Parameters.AddWithValue("@1", employeeID);
            dbCommand.ExecuteNonQuery();
        }

        private void restoreFingerID(int employeeID)
        {
            string query = "SELECT `Finger 1`, `Finger 2`, `Finger 3`, `Finger 4` FROM " +
                "webert_database.employee_fingerid WHERE `Employee ID`=@1";

            MySqlCommand dbCommand = new MySqlCommand(query, dbConnection);
            dbCommand.Parameters.AddWithValue("@1", employeeID);
            MySqlDataReader dbReader = dbCommand.ExecuteReader();

            if(dbReader.HasRows)
            {
                dbReader.Read();
                int[] id = {int.Parse(dbReader.GetString(0)),
                int.Parse(dbReader.GetString(1)),
                int.Parse(dbReader.GetString(2)),
                int.Parse(dbReader.GetString(3))};
                dbReader.Close();

                for (int i=0; i<id.Length; i++)
                {
                    if(id[i]!=0)
                    {
                        query = "UPDATE webert_database.availablefinger " +
                            "SET `Availability`='Yes' " +
                            "WHERE `Finger ID`=@1";
                        dbCommand = new MySqlCommand(query, dbConnection);
                        dbCommand.Parameters.AddWithValue("@1", id[i]);
                        dbCommand.ExecuteNonQuery();
                    }
                    else
                    {
                        break;
                    }
                }
            }
            else
            {
                dbReader.Close();
            }
        }

        public int[] getFingerToDelete(int employeeID)
        {
            string query = "SELECT `Finger 1`, `Finger 2`, `Finger 3`, `Finger 4` " +
                "FROM webert_database.employee_fingerid WHERE `Employee ID`=@1";

            MySqlCommand dbCommand = new MySqlCommand(query, dbConnection);
            dbCommand.Parameters.AddWithValue("@1", employeeID);
            MySqlDataReader dbReader = dbCommand.ExecuteReader();

            if(dbReader.HasRows)
            {
                int[] valid = new int[4];

                dbReader.Read();

                for(int i=0; i<4; i++)
                {
                    valid[i] = int.Parse(dbReader.GetString(i));
                }

                dbReader.Close();

                return valid;
            }

            dbReader.Close();

            int[] notValid = { 0, 0, 0, 0 };

            return notValid;
        }

        private void deleteFingerFromEmployee(int employeeID)
        {
            string query = "DELETE FROM webert_database.employee_fingerid WHERE `Employee ID`=@1";
            MySqlCommand dbCommand = new MySqlCommand(query, dbConnection);
            dbCommand.Parameters.AddWithValue("@1", employeeID);
            dbCommand.ExecuteNonQuery();
        }

        // This function checks if the finger ID from atmega is registered
        // then returns the employee if it does, else returns 0.

        public int isEmployeeFingerRegistered(int fingerID)
        {
            string query = "SELECT `Employee ID` FROM webert_database.employee_fingerid WHERE +" +
                "`Finger 1`=@1 OR `Finger 2`=@2 OR `Finger 3`=@3 OR `Finger 4`=@4;";
            MySqlCommand dbCommand = new MySqlCommand(query, dbConnection);
            dbCommand.Parameters.Add("@1", fingerID);
            dbCommand.Parameters.Add("@2", fingerID);
            dbCommand.Parameters.Add("@3", fingerID);
            dbCommand.Parameters.Add("@4", fingerID);
            MySqlDataReader dbReader = dbCommand.ExecuteReader();

            // If it returned something, the finger ID exists.
            if (dbReader.HasRows)
            {
                dbReader.Read();
              
                int employeeID = int.Parse(dbReader.GetString(0));

                dbReader.Close();

                return employeeID;
            }

            dbReader.Close();
            return 0;
        }

        bool displayInfo = false;

        public bool getDisplayInfo()
        {
            return this.displayInfo;
        }

        public void recordAttendance(int employeeID)
        {
            displayInfo = false;

            // Get today's date and time.
            DateTime dateTimeNow = DateTime.Now;

            string dateNow = dateTimeNow.ToShortDateString();
            string timeNow = dateTimeNow.ToShortTimeString();

            // Check first the range of timein and timeout max.
            // If it is not between 8 AM - 9 PM, then do not attempt to record anything.

            double hoursSinceMN = (DateTime.Now - DateTime.Today).TotalHours;

            //MessageBox.Show(hoursSinceMN.ToString());

            if(!(hoursSinceMN>=7.5 && hoursSinceMN<=21))
            {
                return;
            }

            // Get the the attendance ID of the employee that
            // has a record for this certain day.

            string query1 = "SELECT `Attendance ID` FROM webert_database.employee_attendance WHERE `Employee ID`=@1 AND `Date`=@2;";
            MySqlCommand dbCommand = new MySqlCommand(query1, dbConnection);
            dbCommand.Parameters.AddWithValue("@1", employeeID);
            dbCommand.Parameters.AddWithValue("@2", dateNow);
            MySqlDataReader dbReader = dbCommand.ExecuteReader();


            // If there is no record, automatic time in for
            // that employee on this day.
            // Not False = True
            if (!dbReader.HasRows)
            {
               
                dbReader.Close();

                DateTime lunchTime = DateTime.Parse(timeNow);
                double hours = double.Parse(lunchTime.ToString("HH"));
                double minutesInHours = (double.Parse(lunchTime.ToString("mm")) * 100.0 / 60.0) / 100.0;

                double totalHoursNow = Math.Round(hours + minutesInHours, 2);


                // Check first if total hours does not exceed 1 PM.
                // If it did, you cannot time in for that day.
                if (!(totalHoursNow > 13))
                {
                    // We then select the highest attendance ID and we will increment it.
                    // for the new record.

                    string query2 = "SELECT `Attendance ID` FROM webert_database.employee_attendance ORDER BY " +
                        "`Attendance ID` DESC;";

                    dbCommand = new MySqlCommand(query2, dbConnection);
                    dbReader = dbCommand.ExecuteReader();
                    int attID = 1;

                    if (dbReader.HasRows)
                    {
                        dbReader.Read();
                        attID = int.Parse(dbReader.GetString(0));
                        attID++;
                        //Console.WriteLine("New Attendance ID: " + attID.ToString());
                    }

                    dbReader.Close();

                    //MessageBox.Show(attID.ToString(),"Attendance ID DEBUG");

                    // Get required employee details.
                    string query3 = "SELECT `Last Name`,`Given Name`, `Middle Name` FROM webert_database.employee_info " +
                        "WHERE `Employee ID`=@1";
                    dbCommand = new MySqlCommand(query3, dbConnection);
                    dbCommand.Parameters.AddWithValue("@1", employeeID);
                    dbReader = dbCommand.ExecuteReader();

                    string lName = "", gName = "", mName = "";

                    if (dbReader.HasRows)
                    {
                        dbReader.Read();

                        lName = dbReader.GetString(0);
                        gName = dbReader.GetString(1);
                        mName = dbReader.GetString(2);
                    }


                    dbReader.Close();

                    string query4 = "INSERT INTO webert_database.employee_attendance(`Attendance ID`, " +
                                    "`Employee ID`, " +
                                
                                    "`Date`, " +
                                    "`Time In`) " +
                                    "VALUES(@1,@2,@6,@7)";

                    dbCommand = new MySqlCommand(query4, dbConnection);
                    dbCommand.Parameters.AddWithValue("@1", attID);
                    dbCommand.Parameters.AddWithValue("@2", employeeID);
         
                    dbCommand.Parameters.AddWithValue("@6", dateTimeNow.ToShortDateString());
                    dbCommand.Parameters.AddWithValue("@7", dateTimeNow.ToShortTimeString());

                    dbCommand.ExecuteNonQuery();

                    //Get required employee details.
                    string minorQuery = "SELECT `Last Name`,`Given Name`, `Middle Name` FROM webert_database.employee_info " +
                        "WHERE `Employee ID`=@1";
                    dbCommand = new MySqlCommand(minorQuery, dbConnection);
                    dbCommand.Parameters.AddWithValue("@1", employeeID);
                    dbReader = dbCommand.ExecuteReader();

                    lName = ""; gName = ""; mName = "";

                    if (dbReader.HasRows)
                    {
                        dbReader.Read();

                        lName = dbReader.GetString(0);
                        gName = dbReader.GetString(1);
                        mName = dbReader.GetString(2);
                    }


                    dbReader.Close();

                    currentName = lName + " " + gName + " " + mName;
                    currentAct = "Time In";
                    displayInfo = true;
                }

            }

            // If it has rows, there is already time in 
            // for that employee id on that certain day.
            // So automatic time out. 

            // UPDATE: automatic lunch or timeout.
            // Check if time is between 12:00 PM - 1:30 PM,
            // if it is, record it as lunch.
            else
            {
                // We read it to get the attendance id.
                dbReader.Read();

                // Get the attendance id that employee that has that time in already for this day.
                int attID = int.Parse(dbReader.GetString(0));

                dbReader.Close();

                DateTime lunchTime = DateTime.Parse(timeNow);
                double hours = double.Parse(lunchTime.ToString("HH"));
                double minutesInHours = (double.Parse(lunchTime.ToString("mm")) * 100.0 / 60.0) / 100.0;

                double totalHoursNow = Math.Round(hours + minutesInHours, 2);

                //MessageBox.Show(totalHoursNow.ToString());

                // If time is between 12 PM and 1 PM, record it as lunch.
                if (totalHoursNow >= 12 && totalHoursNow <= 13)
                {
                    string checkMinute = "SELECT `Time In` FROM webert_database.employee_attendance WHERE `Attendance ID`=@1;";

                    dbCommand = new MySqlCommand(checkMinute, dbConnection);
                    dbCommand.Parameters.AddWithValue("@1", attID);
                    dbReader = dbCommand.ExecuteReader();

                    if (dbReader.HasRows)
                    {
                        dbReader.Read();

                        string timeIn = dbReader.GetString(0);
                        double testWork = (double)DateTime.Parse(timeNow).Subtract(DateTime.Parse(timeIn)).TotalMinutes;


                        if (!(testWork > 10))
                        {
                            dbReader.Close();
                            return;
                        }



                        //MessageBox.Show(testWork.ToString());

                    }

                    dbReader.Close();


                    string lunchquery = "UPDATE webert_database.employee_attendance SET " +
                        "`Lunch Time`=@1 WHERE `Attendance ID`=@2 " +
                        "AND `Lunch Time` IS NULL;";

                    dbCommand = new MySqlCommand(lunchquery, dbConnection);
                    dbCommand.Parameters.AddWithValue("@1", timeNow);
                    dbCommand.Parameters.AddWithValue("@2", attID);
                    dbCommand.ExecuteNonQuery();

                    //Get required employee details.
                    string minorQuery = "SELECT `Last Name`,`Given Name`, `Middle Name` FROM webert_database.employee_info " +
                        "WHERE `Employee ID`=@1";
                    dbCommand = new MySqlCommand(minorQuery, dbConnection);
                    dbCommand.Parameters.AddWithValue("@1", employeeID);
                    dbReader = dbCommand.ExecuteReader();

                    string lName = "", gName = "", mName = "";

                    if (dbReader.HasRows)
                    {
                        dbReader.Read();

                        lName = dbReader.GetString(0);
                        gName = dbReader.GetString(1);
                        mName = dbReader.GetString(2);
                    }


                    dbReader.Close();

                    currentName = lName + " " + gName + " " + mName;
                    currentAct = "Lunch";
                    displayInfo = true;
                    // MessageBox.Show("Lunch");
                }
                else
                {
                    //MessageBox.Show("Not lunch");

                    string checkMinute = "SELECT `Time In` FROM webert_database.employee_attendance WHERE `Attendance ID`=@1;";

                    dbCommand = new MySqlCommand(checkMinute, dbConnection);
                    dbCommand.Parameters.AddWithValue("@1", attID);
                    dbReader = dbCommand.ExecuteReader();

                    if(dbReader.HasRows)
                    {
                        dbReader.Read();

                        string timeIn = dbReader.GetString(0);
                        double testWork = (double)DateTime.Parse(timeNow).Subtract(DateTime.Parse(timeIn)).TotalMinutes;


                        if(!(testWork>10))
                        {
                            dbReader.Close();
                            return;
                        }

                         

                        //MessageBox.Show(testWork.ToString());

                    }

                    dbReader.Close();

                    

                    // Update timeout and include in query to check
                    // if time out is null so that it won't be overrided if there is a previous record.
                    string query5 = "UPDATE webert_database.employee_attendance SET " +
                        "`Time Out`=@1 WHERE `Attendance ID`=@2 AND `Time Out` IS NULL;";

                    dbCommand = new MySqlCommand(query5, dbConnection);
                    dbCommand.Parameters.AddWithValue("@1", timeNow);
                    dbCommand.Parameters.AddWithValue("@2", attID);
                    dbCommand.ExecuteNonQuery();

                    // We then get the difference between the time in and time out to update the remarks.

                    string query6 = "SELECT `Time In`, `Time Out` FROM webert_database.employee_attendance " +
                            "WHERE `Attendance ID`=@1";
                    dbCommand = new MySqlCommand(query6, dbConnection);
                    dbCommand.Parameters.AddWithValue("@1", attID);
                    dbReader = dbCommand.ExecuteReader();

                    if (dbReader.HasRows)
                    {
                        dbReader.Read();

                        string timeIn = dbReader.GetString(0);
                        string timeOut = dbReader.GetString(1);

                        dbReader.Close();

                        double totalWorkHours = (double)DateTime.Parse(timeOut).Subtract(DateTime.Parse(timeIn)).TotalHours;
                        string remarks = "Unknown";

                        //MessageBox.Show(totalWorkHours.ToString(), "Total Work Hours");

                        // Greater than or equal full time and less than over time.
                        // Full Time
                        if ((totalWorkHours >= WebertEmployeeClass.fullTimeWorkHours &&
                            totalWorkHours < WebertEmployeeClass.overTimeWorkhouts) || 
                            (totalWorkHours >= WebertEmployeeClass.fullTimeWorkHours-1 &&
                            totalWorkHours < WebertEmployeeClass.overTimeWorkhouts)
                            
                            )
                        {
                            totalWorkHours = totalWorkHours - 1; // Minus 1 lunch.
                            remarks = "Full Time";
                        }
                        // Late. Greater than or equal late but less than full time.
                        else if(totalWorkHours>=WebertEmployeeClass.lateTimeWorkHours && 
                            totalWorkHours<WebertEmployeeClass.fullTimeWorkHours)
                        {
                            totalWorkHours = totalWorkHours - 1; // Minus 1 lunch.
                            remarks = "Late";
                        }
                        // Greater than or equal half time and less than late time.
                        else if (totalWorkHours >= WebertEmployeeClass.halfTimeWorkHours &&
                            totalWorkHours < WebertEmployeeClass.lateTimeWorkHours)
                        {
                            // No lunch.
                            remarks = "Half Time";
                        }
                        // Over time.
                        else if (totalWorkHours > WebertEmployeeClass.overTimeWorkhouts)
                        {
                            // Check if totalWorkHours exceed max.
                            // If it did, set it only to max.
                            if(totalWorkHours>WebertEmployeeClass.maxOverTimeHours)
                            {
                                totalWorkHours = WebertEmployeeClass.maxOverTimeHours;
                            }

                            totalWorkHours = totalWorkHours - 9; // Minus full time and lunch to get total work hours.


                            remarks = "Over Time";
                        }
                        // else if wala na, unknown pa rin work status.
                        // Example pinaglaruan, nag time in tas nag time out agad.

                        string query7 = "UPDATE webert_database.employee_attendance SET " +
                            "`Remarks`=@1 WHERE `Attendance ID`=@2;";
                        dbCommand = new MySqlCommand(query7, dbConnection);
                        dbCommand.Parameters.AddWithValue("@1", remarks);
                        dbCommand.Parameters.AddWithValue("@2", attID);

                        dbCommand.ExecuteNonQuery();

                        // Then we compute for the overtime hours if over time.

                        if (remarks == "Over Time")
                        {
                            string query8 = "UPDATE webert_database.employee_attendance " +
                                "SET `Over Time Hours`=@1 " +
                                "WHERE `Attendance ID`=@2;";
                            dbCommand = new MySqlCommand(query8, dbConnection);
                            dbCommand.Parameters.AddWithValue("@1", totalWorkHours);
                            dbCommand.Parameters.AddWithValue("@2", attID);

                            dbCommand.ExecuteNonQuery();
                        }

                        //Get required employee details.
                        string minorQuery = "SELECT `Last Name`,`Given Name`, `Middle Name` FROM webert_database.employee_info " +
                            "WHERE `Employee ID`=@1";
                        dbCommand = new MySqlCommand(minorQuery, dbConnection);
                        dbCommand.Parameters.AddWithValue("@1", employeeID);
                        dbReader = dbCommand.ExecuteReader();

                        string lName = "", gName = "", mName = "";

                        if (dbReader.HasRows)
                        {
                            dbReader.Read();

                            lName = dbReader.GetString(0);
                            gName = dbReader.GetString(1);
                            mName = dbReader.GetString(2);
                        }


                        dbReader.Close();

                        currentName = lName + " " + gName + " " + mName;
                        currentAct = "Time Out";
                        displayInfo = true;
                    }
                    else
                    {
                        dbReader.Close();
                    }
                }
            }
        }

        public int getEmpIDFromFingerID(int fingerID)
        {
            string query = "SELECT `Employee ID` FROM webert_database.employee_fingerid " +
                "WHERE `Finger 1`=@1 OR `Finger 2`=@2 OR `Finger 3`=@3 OR `Finger 4`=@4;";

            MySqlCommand dbCommand = new MySqlCommand(query, dbConnection);
            dbCommand.Parameters.AddWithValue("@1", fingerID);
            dbCommand.Parameters.AddWithValue("@2", fingerID);
            dbCommand.Parameters.AddWithValue("@3", fingerID);
            dbCommand.Parameters.AddWithValue("@4", fingerID);

            MySqlDataReader dbReader = dbCommand.ExecuteReader();

            if(dbReader.HasRows)
            {
                dbReader.Read();
                int employeeID= int.Parse(dbReader.GetString(0));
                dbReader.Close();
                return employeeID;
            }

            dbReader.Close();

            return 0;
        }

        public int updateWorkStatus(int employeeID, string workStatus)
        {
            string query = "UPDATE webert_database.employee_workstatus SET " +
                "`Work Status`=@1 WHERE `Employee ID`=@2";
            MySqlCommand dbCommand = new MySqlCommand(query, dbConnection);
            dbCommand.Parameters.AddWithValue("@1", workStatus);
            dbCommand.Parameters.AddWithValue("@2", employeeID);
            return dbCommand.ExecuteNonQuery();
        }

        public int updateRemarks(int attendanceID, string remarks)
        {
            string query = "UPDATE webert_database.employee_attendance SET " +
                "`Remarks`=@1 WHERE `Attendance ID`=@2";
            MySqlCommand dbCommand = new MySqlCommand(query, dbConnection);
            dbCommand.Parameters.AddWithValue("@1", remarks);
            dbCommand.Parameters.AddWithValue("@2", attendanceID);
            return dbCommand.ExecuteNonQuery();
        }

        public int updateRemarks(int attendanceID, string remarks, int newOT)
        {
            string query = "UPDATE webert_database.employee_attendance SET " +
                "`Remarks`=@1, `Over Time Hours`=@2 WHERE `Attendance ID`=@3";
            MySqlCommand dbCommand = new MySqlCommand(query, dbConnection);
            dbCommand.Parameters.AddWithValue("@1", remarks);
            dbCommand.Parameters.AddWithValue("@2", newOT);
            dbCommand.Parameters.AddWithValue("@3", attendanceID);
            return dbCommand.ExecuteNonQuery();
        }

        public void removeTimeIn(int attendanceID)
        {
            string query = "DELETE FROM webert_database.employee_attendance " +
                 "WHERE `Attendance ID`=@1;";
            MySqlCommand dbCommand = new MySqlCommand(query, dbConnection);
            dbCommand.Parameters.AddWithValue("@1", attendanceID);
            dbCommand.ExecuteNonQuery();
        }

        public void removeTimeOut(int attendanceID)
        {
            string query = "UPDATE webert_database.employee_attendance " +
                "SET  `Time Out` = NULL, " +
                "`Over Time Hours`=NULL, " +
                "`Remarks`=NULL " +
                 "WHERE `Attendance ID`=@1;";
            MySqlCommand dbCommand = new MySqlCommand(query, dbConnection);
            dbCommand.Parameters.AddWithValue("@1", attendanceID);
            dbCommand.ExecuteNonQuery();
        }

        // The hardest shit.

        public bool computeSalary(string dateFrom, string dateTo)
        {
            /* The algorithm.
             * -> Kunin lahat ng employee id sa attendance table.
             * -> Mag loop kada employee id, kunin lahat ng info from date range.
             * -> Sa remarks column, bilangin kung ilan and FT,HT at OT. 
             * -> Compute using the formula:
             * -> salary=ftNum*ftSalary+htNum+htSalary+otNum+otSalary;
             * -> Insert sa current salary report table.
             * -> Employee ID, Last Name, Given Name, Middle Name, Number of FT,
             * -> Number of HT, Number of OT and Salary
             */

            // Get number of employee in the attendace by their employee id distinct.
            string query = "SELECT COUNT(DISTINCT `Employee ID`) FROM webert_database.employee_attendance " +
                             "ORDER BY `Employee ID` ASC;";

            MySqlCommand dbCommand = new MySqlCommand(query, dbConnection);
            MySqlDataReader dbReader = dbCommand.ExecuteReader();
            int numEmployee = 0;

            if(dbReader.HasRows)
            {
                dbReader.Read();

                numEmployee = int.Parse(dbReader.GetString(0));
            }

            dbReader.Close();

            if (numEmployee != 0)
            {
                // Get the actual distinct employee ids that we will use for looping.

                query = "SELECT DISTINCT `Employee ID` FROM webert_database.employee_attendance " +
                             "ORDER BY `Employee ID` ASC;";
                dbCommand = new MySqlCommand(query, dbConnection);
                dbReader = dbCommand.ExecuteReader();
                int[] employeeIDs = new int[numEmployee];

                if (dbReader.HasRows)
                {
                    int ctr = 0;

                    while(dbReader.Read())
                    {
                        employeeIDs[ctr] = int.Parse(dbReader.GetString(0));
                        ctr++;
                    }
                }

                dbReader.Close();

                // Now we have the list of distinc employee ids in the attendance,
                // we get their data between two date intervals per employee.

                if(employeeIDs.Length==0)
                {
                    return false;
                }
                else
                {
                    // Delete all records to generate new report.

                    query = "TRUNCATE TABLE webert_database.salaryreport;";
                    dbCommand = new MySqlCommand(query, dbConnection);
                    dbCommand.ExecuteNonQuery();
                }

                for (int i = 0; i < employeeIDs.Length; i++)
                {
                    string queryFTCount = "SELECT COUNT(`Remarks`) " +
                    "FROM webert_database.employee_attendance WHERE `Employee ID`=@1 AND " +
                    "STR_TO_DATE(`Date`, '%m/%d/%Y') " +
                    "BETWEEN STR_TO_DATE(@2, '%m/%d/%Y') AND STR_TO_DATE(@3, '%m/%d/%Y') " +
                    "AND `Remarks`='Full Time' " +
                    "ORDER BY STR_TO_DATE(`Date`, '%m/%d/%Y') DESC;";

                    string queryHTCount = "SELECT COUNT(`Remarks`) " +
                    "FROM webert_database.employee_attendance WHERE `Employee ID`=@1 AND " +
                    "STR_TO_DATE(`Date`, '%m/%d/%Y') " +
                    "BETWEEN STR_TO_DATE(@2, '%m/%d/%Y') AND STR_TO_DATE(@3, '%m/%d/%Y') " +
                    "AND `Remarks`='Half Time' " +
                    "ORDER BY STR_TO_DATE(`Date`, '%m/%d/%Y') DESC;";

                    string queryOTCount = "SELECT COUNT(`Remarks`) " +
                    "FROM webert_database.employee_attendance WHERE `Employee ID`=@1 AND " +
                    "STR_TO_DATE(`Date`, '%m/%d/%Y') " +
                    "BETWEEN STR_TO_DATE(@2, '%m/%d/%Y') AND STR_TO_DATE(@3, '%m/%d/%Y') " +
                    "AND `Remarks`='Over Time' " +
                    "ORDER BY STR_TO_DATE(`Date`, '%m/%d/%Y') DESC;";

                    string querySUMOTHours = "SELECT SUM(`Over Time Hours`) " +
                    "FROM webert_database.employee_attendance WHERE `Employee ID`=@1 AND " +
                    "STR_TO_DATE(`Date`, '%m/%d/%Y') " +
                    "BETWEEN STR_TO_DATE(@2, '%m/%d/%Y') AND STR_TO_DATE(@3, '%m/%d/%Y') " +
                    "AND `Remarks`='Over Time' " +
                    "ORDER BY STR_TO_DATE(`Date`, '%m/%d/%Y') DESC;";

                    string queryLateCount = "SELECT COUNT(`Remarks`) " +
                   "FROM webert_database.employee_attendance WHERE `Employee ID`=@1 AND " +
                   "STR_TO_DATE(`Date`, '%m/%d/%Y') " +
                   "BETWEEN STR_TO_DATE(@2, '%m/%d/%Y') AND STR_TO_DATE(@3, '%m/%d/%Y') " +
                   "AND `Remarks`='Late' " +
                   "ORDER BY STR_TO_DATE(`Date`, '%m/%d/%Y') DESC;";

                    int FTCount = 0;
                    int HTCount = 0;
                    int OTCount = 0;
                    int LateCount = 0;
                    int sumOTHours = 0;

                    //MessageBox.Show(employeeIDs[i].ToString());

                    dbCommand = new MySqlCommand(queryFTCount, dbConnection);
                    dbCommand.Parameters.AddWithValue("@1", employeeIDs[i]);
                    dbCommand.Parameters.AddWithValue("@2", dateFrom);
                    dbCommand.Parameters.AddWithValue("@3", dateTo);
           
                    dbReader = dbCommand.ExecuteReader();

                    if (dbReader.HasRows)
                    {
                        dbReader.Read();
                        FTCount = int.Parse(dbReader.GetString(0));
                    }

                    dbReader.Close();

                    ////////////////////////////////////////////////////////

                    dbCommand = new MySqlCommand(queryHTCount, dbConnection);
                    dbCommand.Parameters.AddWithValue("@1", employeeIDs[i]);
                    dbCommand.Parameters.AddWithValue("@2", dateFrom);
                    dbCommand.Parameters.AddWithValue("@3", dateTo);

                    dbReader = dbCommand.ExecuteReader();

                    if (dbReader.HasRows)
                    {
                        dbReader.Read();
                        HTCount = int.Parse(dbReader.GetString(0));
                    }

                    dbReader.Close();

                    ////////////////////////////////////////////////////////

                    dbCommand = new MySqlCommand(queryLateCount, dbConnection);
                    dbCommand.Parameters.AddWithValue("@1", employeeIDs[i]);
                    dbCommand.Parameters.AddWithValue("@2", dateFrom);
                    dbCommand.Parameters.AddWithValue("@3", dateTo);

                    dbReader = dbCommand.ExecuteReader();

                    if (dbReader.HasRows)
                    {
                        dbReader.Read();
                         LateCount= int.Parse(dbReader.GetString(0));
                    }

                    dbReader.Close();


                    ////////////////////////////////////////////////////////

                    dbCommand = new MySqlCommand(queryOTCount, dbConnection);
                    dbCommand.Parameters.AddWithValue("@1", employeeIDs[i]);
                    dbCommand.Parameters.AddWithValue("@2", dateFrom);
                    dbCommand.Parameters.AddWithValue("@3", dateTo);

                    dbReader = dbCommand.ExecuteReader();

                    if (dbReader.HasRows)
                    {
                        dbReader.Read();
                        OTCount = int.Parse(dbReader.GetString(0));

                        dbReader.Close();

                        // Only compute sum of OT Hours when there is OT in general.

                        if (OTCount != 0)
                        {
                            dbCommand = new MySqlCommand(querySUMOTHours, dbConnection);
                            dbCommand.Parameters.AddWithValue("@1", employeeIDs[i]);
                            dbCommand.Parameters.AddWithValue("@2", dateFrom);
                            dbCommand.Parameters.AddWithValue("@3", dateTo);

                            dbReader = dbCommand.ExecuteReader();

                            if (dbReader.HasRows)
                            {
                                dbReader.Read();
                                sumOTHours = int.Parse(dbReader.GetString(0));
                            }

                            dbReader.Close();
                        }
                    }

                    dbReader.Close();


                    String debug = String.Format("{0}-{1}-{2}-{3}", FTCount.ToString(),
                        HTCount.ToString(), OTCount.ToString(), sumOTHours.ToString());
                    //MessageBox.Show(debug, "DEBUG");

                    int salary = FTCount * WebertEmployeeClass.FTSalary +
                        HTCount * WebertEmployeeClass.HTSalary +
                        OTCount * WebertEmployeeClass.FTSalary +
                        sumOTHours * WebertEmployeeClass.OTRate +
                        LateCount * WebertEmployeeClass.LateSalary;

                    //MessageBox.Show(salary.ToString(), "DEBUG");

                    // We now have the salary, we get relevant info to summarize information
                    // about the employee and the salary.
                    // We need to get the EmpID, LN, GN, MN
                    // Then we add it to a new table with the following info:
                    // EmpID, LN, GN, MN, Number of Full Time, Number of Half Time,
                    // Number of Over Time, Salary

                    query = "SELECT `Last Name`, `Given Name`, `Middle Name` " +
                            "FROM webert_database.employee_info " +
                            "WHERE `Employee ID`=@1";

                    dbCommand = new MySqlCommand(query, dbConnection);
                    dbCommand.Parameters.Add("@1", employeeIDs[i]);
                    dbReader = dbCommand.ExecuteReader();

                    string lName="", gName="", mName="";

                    if(dbReader.HasRows)
                    {
                        dbReader.Read();

                        lName = dbReader.GetString(0);
                        gName = dbReader.GetString(1);
                        mName = dbReader.GetString(2);
                    }

                    dbReader.Close();

                    query = "INSERT INTO webert_database.salaryreport(`Employee ID`, " +
                        "`Last Name`, `Given Name`, `Middle Name`, `Number of Full Time Days`, " +
                        "`Number of Half Time Days`, `Number of Over Time Hours`, `Salary`) " +
                        "VALUES(@1,@2,@3,@4,@5,@6,@7,@8);";
                    //MessageBox.Show(query);
                    dbCommand = new MySqlCommand(query, dbConnection);
                    dbCommand.Parameters.AddWithValue("@1", employeeIDs[i]);
                    dbCommand.Parameters.AddWithValue("@2", lName);
                    dbCommand.Parameters.AddWithValue("@3", gName);
                    dbCommand.Parameters.AddWithValue("@4", mName);
                    dbCommand.Parameters.AddWithValue("@5", FTCount);
                    dbCommand.Parameters.AddWithValue("@6", HTCount);
                    dbCommand.Parameters.AddWithValue("@7", OTCount);
                    dbCommand.Parameters.AddWithValue("@8", salary);

                    dbCommand.ExecuteNonQuery();
                }

                return true;
            }

            return false;
        }

        public string getAdminName()
        {
            string query = "SELECT `Username` FROM webert_database.admininfo WHERE `ID`=1";

            MySqlCommand dbCommand = new MySqlCommand(query, dbConnection);
            MySqlDataReader dbReader = dbCommand.ExecuteReader();

            if(dbReader.HasRows)
            {
                dbReader.Read();

                string adminname = dbReader.GetString(0);

                dbReader.Close();

                return adminname;
            }

            return "";
        }

        public string[] getSalaryInfo()
        {
            string query = "SELECT `Full Time Salary`, `Half Time Salary`, " +
                "`Over Time Hourly Rate`, `Late Time Salary` FROM webert_database.employee_salaryinfo " +
                "WHERE `ID`=1;";

            MySqlCommand dbCommand = new MySqlCommand(query, dbConnection);
            MySqlDataReader dbReader = dbCommand.ExecuteReader();

            if(dbReader.HasRows)
            {
                string[] salaryList = new string[4];

                dbReader.Read();

                for(int i=0; i<salaryList.Length; i++)
                {
                    salaryList[i] = dbReader.GetString(i);
                }

                dbReader.Close();

                return salaryList;
            }

            dbReader.Close();

            string[] empty = new string[4];
            return empty;
        }

        public void setSalaryIfo(int[] salaryList)
        {
            string query = "UPDATE webert_database.employee_salaryinfo SET " +
                "`Full Time Salary`=@1, " +
                "`Half Time Salary`=@2, " +
                "`Over Time Hourly Rate`=@3, " +
                "`Late Time Salary`=@4 " +
                " WHERE `ID`=1;";

            MySqlCommand dbCommand = new MySqlCommand(query, dbConnection);

            dbCommand.Parameters.AddWithValue("@1", salaryList[0]);
            dbCommand.Parameters.AddWithValue("@2", salaryList[1]);
            dbCommand.Parameters.AddWithValue("@3", salaryList[2]);
            dbCommand.Parameters.AddWithValue("@4", salaryList[3]);

            dbCommand.ExecuteNonQuery();
        }

        public bool isPasswordCorrect(string password)
        {
            string query = "SELECT `Password` FROM webert_database.admininfo " +
                "WHERE `Password`=@1 AND `ID`=1";
            MySqlCommand dbCommand = new MySqlCommand(query, dbConnection);
            dbCommand.Parameters.AddWithValue("@1", password);
            //MessageBox.Show(password);

            MySqlDataReader dbReader = dbCommand.ExecuteReader();

            if(dbReader.HasRows)
            {
                dbReader.Read();

                if(dbReader.GetString(0).Equals(password))
                {
                    dbReader.Close();

                    return true;
                }
                else
                {
                    dbReader.Close();

                    return false;
                }
            }

            dbReader.Close();

            return false;
        }

        public void changeAdminInfo(string username)
        {
            string query = "UPDATE webert_database.admininfo " +
                "SET `Username`=@1 WHERE `ID`=1";

            MySqlCommand dbCommand = new MySqlCommand(query, dbConnection);
            dbCommand.Parameters.AddWithValue("@1", username);

            dbCommand.ExecuteNonQuery();
        }

        public void changeAdminInfo(string username, string password)
        {
            string query = "UPDATE webert_database.admininfo " +
                "SET `Username`=@1, `Password`=@2 WHERE `ID`=1";

            MySqlCommand dbCommand = new MySqlCommand(query, dbConnection);
            dbCommand.Parameters.AddWithValue("@1", username);
            dbCommand.Parameters.AddWithValue("@2", password);

            dbCommand.ExecuteNonQuery();
        }

        public void closeSqlConnection()
        {
            dbConnection.Close();
        }

        public bool isUserExist(string username, string password)
        {
            string query = "SELECT `Username`,`Password` FROM webert_database.admininfo " +
                "WHERE `Username`=@1 AND `Password`=@2;";

            MySqlCommand dbCommand = new MySqlCommand(query, dbConnection);
            dbCommand.Parameters.AddWithValue("@1", username);
            dbCommand.Parameters.AddWithValue("@2", password);
            MySqlDataReader dbReader = dbCommand.ExecuteReader();


            if(dbReader.HasRows)
            {
                dbReader.Read();

                bool isUserExists = dbReader.GetString(0).Equals(username) &&
                    dbReader.GetString(1).Equals(password);

                dbReader.Close();

                return isUserExists;
            }

            dbReader.Close();
           
            return false;
        }

        public void resetdatabase(string sqlQueries)
        {
            MySqlCommand dbCommand = new MySqlCommand(sqlQueries, dbConnection);
            dbCommand.ExecuteNonQuery();
        }

        public void addEmployeeImage(string imageName, int employeeID)
        {
            string query = "UPDATE webert_database.employee_info SET `Image Name`=@1 " +
                "WHERE `Employee ID`=@2";

            MySqlCommand dbCommand = new MySqlCommand(query, dbConnection);
            dbCommand.Parameters.AddWithValue("@1", imageName);
            dbCommand.Parameters.AddWithValue("@2", employeeID);

            dbCommand.ExecuteNonQuery();
        }

        public string getEmployeeImageName(int employeeID)
        {
            string query = "SELECT `Image Name` FROM webert_database.employee_info " +
                "WHERE `Employee ID`=@1";

            MySqlCommand dbCommand = new MySqlCommand(query, dbConnection);
            dbCommand.Parameters.AddWithValue("@1", employeeID);
            MySqlDataReader dbReader = dbCommand.ExecuteReader();

            if(dbReader.HasRows)
            {
                dbReader.Read();

                string imageName= dbReader.GetString(0);

                // Debug

                //MessageBox.Show(imageName, "Image Name");

                dbReader.Close();

                return imageName;
            }

            dbReader.Close();

            return "";
        }
    }
}
