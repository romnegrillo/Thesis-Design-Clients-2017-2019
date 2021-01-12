using System;
using System.Windows.Forms;
using System.IO.Ports;
using System.IO;
using Microsoft.Office.Interop.Excel;
using System.Drawing;

namespace Webert
{
    public partial class AdminForm : Form
    {
        private WebertSqlClass mySqlClass;
        private WebertEmployeeClass myWebertEmployeeClass;
        private SerialPort atmegaPort = new SerialPort();
        private bool portLoaded = false;
        private string portName;

        public AdminForm(string portName)
        {
            InitializeComponent();
            this.portName = portName;

            loadFormInfo();

            try
            {
                mySqlClass = new WebertSqlClass();
                refreshTables();
                loadAdminInfo();
            }
            catch (Exception exp)
            {
                MessageBox.Show("Cannot connect to database.", "Error",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
            }

            try
            {
                loadPort();
                this.portLoaded = true;
            }
            catch (Exception exp)
            {
                //MessageBox.Show(exp.ToString());
                MessageBox.Show("No device connected.", "Error",
                  MessageBoxButtons.OK, MessageBoxIcon.Error);
            }


            // For Debugging

            // Checking if finger is registered.
            // This will return the employee ID of the owner of the finger ID.
            //MessageBox.Show(checkFingerRegistered(5).ToString(), "Finger Check");

            // Checking to see available finger ids when adding employees.
            //int[] availableFinger=mySqlClass.getAvailableFinger(3);

            //foreach(int item in availableFinger)
            //{
            //    MessageBox.Show(item.ToString(), "Available Finger");
            //}


            // Checking to get registered finger for one employee to delete.
            //int[] toDelete=mySqlClass.getFingerToDelete(1);
            //MessageBox.Show(toDelete[1].ToString());

        }

        private void AdminForm_Shown(object sender, EventArgs e)
        {
            if (!this.portLoaded)
            {
                mySqlClass.closeDatabase();
                System.Windows.Forms.Application.Exit();
            }
        }

        private void loadFormInfo()
        {
            string[] genderList = { "Male", "Female" };
            int[] numFingerList = { 1, 2, 3, 4 };
            string[] workStatusList = { "Full Time", "Part Time", "Leave of Absence" };
            string[] remarksList = { "Full Time", "Half Time", "Over Time" };

            foreach (string item in genderList)
            {
                // Combobox for gender.
                comboBox1.Items.Add(item);
                comboBox3.Items.Add(item);
            }

            foreach (int item in numFingerList)
            {
                // Combobox for number of fingerprint to register.
                comboBox2.Items.Add(item);
            }

            foreach (string item in workStatusList)
            {
                //workStatusCB.Items.Add(item);
            }

            foreach (string item in remarksList)
            {
                remarksCB.Items.Add(item);
            }

            comboBox1.SelectedIndex = 0;
            comboBox3.SelectedIndex = 0;
            comboBox2.SelectedIndex = 0;
           // workStatusCB.SelectedIndex = 0;
            remarksCB.SelectedIndex = 0;

            comboBox1.DropDownStyle = ComboBoxStyle.DropDownList;
            comboBox2.DropDownStyle = ComboBoxStyle.DropDownList;
            comboBox3.DropDownStyle = ComboBoxStyle.DropDownList;

            employee_attendanceDGV1.ReadOnly = true;  // Attendance Tab
            employee_infoDGV1.ReadOnly = true;        // Add Employee Tab
            employee_infoDGV2.ReadOnly = true;        // Edit Employee Tab
            employee_infoDGV3.ReadOnly = true;        // Delete Employee Tab
            employee_attendanceDGV2.ReadOnly = true;  // Edit Remarks Tab
            //employee_workstatus_DGV.ReadOnly = true;  // Edit Work Status Stab
            employee_SalaryReport_DGV.ReadOnly = true; // Salary Report Tab

            // Full row selection mode.
            employee_attendanceDGV1.SelectionMode = DataGridViewSelectionMode.FullRowSelect;
            employee_infoDGV1.SelectionMode = DataGridViewSelectionMode.FullRowSelect;
            employee_infoDGV2.SelectionMode = DataGridViewSelectionMode.FullRowSelect;
            employee_infoDGV3.SelectionMode = DataGridViewSelectionMode.FullRowSelect;
            employee_attendanceDGV2.SelectionMode = DataGridViewSelectionMode.FullRowSelect;
            //employee_workstatus_DGV.SelectionMode = DataGridViewSelectionMode.FullRowSelect;
            employee_SalaryReport_DGV.SelectionMode = DataGridViewSelectionMode.FullRowSelect;

            // Used to remove one blank row at the end of the datagrid view.
            employee_attendanceDGV1.AllowUserToAddRows = false;
            employee_infoDGV1.AllowUserToAddRows = false;
            employee_infoDGV2.AllowUserToAddRows = false;
            employee_infoDGV3.AllowUserToAddRows = false;
            employee_attendanceDGV2.AllowUserToAddRows = false;
            //employee_workstatus_DGV.AllowUserToAddRows = false;
            employee_SalaryReport_DGV.AllowUserToAddRows = false; 

            // Clear selection.
            employee_attendanceDGV1.ClearSelection();
            employee_infoDGV1.ClearSelection();
            employee_infoDGV2.ClearSelection();
            employee_infoDGV3.ClearSelection();
            employee_attendanceDGV2.ClearSelection();
            //employee_workstatus_DGV.ClearSelection();
            employee_SalaryReport_DGV.ClearSelection();

            currPassTB.Enabled = false;
            newPassTB.Enabled = false;
            confirmPassTB.Enabled = false;


            OTHoursEdit.Enabled = false;

            loadImages();   

        }

        private void loadImages()
        {
            string startupPath = Path.Combine(Directory.GetParent(System.IO.Directory.GetCurrentDirectory()).Parent.Parent.Parent.FullName, "Webert\\EmployeeImages\\employee_logo.png");
            WebertEmployeeClass.pictureName = startupPath;

            attendancePBox.ImageLocation = startupPath;
            addPBox.ImageLocation = startupPath;
            editPBox.ImageLocation = startupPath;

            attendancePBox.SizeMode = PictureBoxSizeMode.StretchImage;
            addPBox.SizeMode = PictureBoxSizeMode.StretchImage;
            editPBox.SizeMode = PictureBoxSizeMode.StretchImage;

            startupPath = "";
        }

        private void loadAdminInfo()
        {
            uNameTB.Text = mySqlClass.getAdminName();

            string[] salaryList= mySqlClass.getSalaryInfo();

            FTSTB.Text = salaryList[0];
            HTSTB.Text = salaryList[1];
            OTTB.Text = salaryList[2];
            LateSalaryTB.Text = salaryList[3];

            // To update, check it empty.

            WebertEmployeeClass.FTSalary = int.Parse(salaryList[0]);
            WebertEmployeeClass.HTSalary = int.Parse(salaryList[1]);
            WebertEmployeeClass.OTRate = int.Parse(salaryList[2]);
            WebertEmployeeClass.LateSalary = int.Parse(salaryList[3]);
        }

        private void formClosing(object sender, FormClosingEventArgs e)
        {
            atmegaPort.Close();
            System.Windows.Forms.Application.Exit();
            
        }

        private void refreshTables()
        {
            try
            {

                if (InvokeRequired)
                {
                    // after we've done all the processing, 
                    this.Invoke(new MethodInvoker(delegate {
                        // load the control with the appropriate data
                        employee_attendanceDGV1.DataSource = mySqlClass.getAttendanceInfoTable();
                        employee_infoDGV1.DataSource = mySqlClass.getEmployeeInfoTable();
                        employee_infoDGV2.DataSource = mySqlClass.getEmployeeInfoTable();
                        employee_infoDGV3.DataSource = mySqlClass.getEmployeeInfoTable();
                        employee_attendanceDGV2.DataSource = mySqlClass.getAttendanceInfoTable();
                        //employee_workstatus_DGV.DataSource = mySqlClass.getWorkStatusInfoTable();
                        employee_SalaryReport_DGV.DataSource = mySqlClass.getSalaryReportInfoTable();
                    }));
                    return;
                }
                else
                {
                    employee_attendanceDGV1.DataSource = mySqlClass.getAttendanceInfoTable();
                    employee_infoDGV1.DataSource = mySqlClass.getEmployeeInfoTable();
                    employee_infoDGV2.DataSource = mySqlClass.getEmployeeInfoTable();
                    employee_infoDGV3.DataSource = mySqlClass.getEmployeeInfoTable();
                    employee_attendanceDGV2.DataSource = mySqlClass.getAttendanceInfoTable();
                    //employee_workstatus_DGV.DataSource = mySqlClass.getWorkStatusInfoTable();
                    employee_SalaryReport_DGV.DataSource = mySqlClass.getSalaryReportInfoTable();
                }
            }
            catch (Exception exp)
            {
                //MessageBox.Show(exp.ToString());
                MessageBox.Show("Cannot connect to database.", "Error",
                     MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void clearAddEmployeeTextBox()
        {
            textBox1.Text = "";
            textBox2.Text = "";
            textBox3.Text = "";
            textBox4.Text = "";
            textBox6.Text = "";
            textBox7.Text = "";
            textBox8.Text = "";
            textBox9.Text = "";
            textBox10.Text = "";
            textBox11.Text = "";
            loadImages();
        }

        private void clearEditEmployeeTextBox()
        {
            textBox24.Text = "";
            textBox23.Text = "";
            textBox22.Text = "";
            textBox21.Text = "";
            textBox19.Text = "";
            textBox18.Text = "";
            textBox17.Text = "";
            textBox16.Text = "";
            textBox15.Text = "";
            textBox14.Text = "";
            loadImages();
        }

        private void loadPort()
        {
            atmegaPort.PortName = this.portName;
            atmegaPort.BaudRate = 9600;
            atmegaPort.DtrEnable = true;
            atmegaPort.Open();

            //atmegaPort = new SerialPort(this.portName, 9600);
            //atmegaPort.Open();
            //atmegaPort.DataReceived += new SerialDataReceivedEventHandler(DataReceivedHandler);

            atmegaPort.DataReceived += new SerialDataReceivedEventHandler(DataReceivedHandler);
        }

        private void DataReceivedHandler(
                    object sender,
                    SerialDataReceivedEventArgs e)
        {
            SerialPort sp = (SerialPort)sender;
            string inData = sp.ReadLine();
            //MessageBox.Show(inData, "Device Message");
            if (!(inData.Contains("INCOMINGFINGER")))
            {
                //MessageBox.Show(inData, "Device Message");

                if (
                    inData.StartsWith("ENROLLMODE")
                    ||
                    inData.StartsWith("DELETEMODE")
                    ||
                    inData.StartsWith("Waiting for finger")
                    ||
                    inData.StartsWith("Image taken")
                    ||
                    inData.StartsWith("Remove finger")
                    ||
                    inData.StartsWith("Place same finger again")
                    ||
                    inData.StartsWith("Fingerprints did not match")
                    ||
                    inData.StartsWith("Stored!")
                    ||
                    inData.StartsWith("Prints matched!")
                    ||
                    inData.StartsWith("ENROLL MODE DONE")
                    ||
                    inData.StartsWith("DELETE MODE DONE")
                    ||
                    inData.StartsWith("All finger prints deleted!")
                    ||
                    inData.StartsWith("Finger print not recognized.")
                    )
                {
                    MessageBox.Show(inData, "Device Message");

                }
                else
                {
                    MessageBox.Show(inData, "Device Message");
                    //MessageBox.Show("Press device button", "Device Message");
                }

                sp.DiscardInBuffer();


            }

            // Check if the atmega receives the enroll mode done signal.
            // This will only execute on add employee button
            // where there is a valid number of finger prints available.
            if (inData == "ENROLL MODE DONE\r")
            {
                //MessageBox.Show("ENROLLMODEDONE", "DEBUG");

                // The myWebertEmployeeClass is already instantiated when the add button
                // is clicked.
                // We just simply need to call mySqlClass to register it after
                // the finger print is registered.

                mySqlClass.addEmployee(myWebertEmployeeClass.getLN(),
                          myWebertEmployeeClass.getGN(),
                          myWebertEmployeeClass.getMN(),
                          myWebertEmployeeClass.getAge(),
                          myWebertEmployeeClass.getSex(),
                          myWebertEmployeeClass.getHA(),
                          myWebertEmployeeClass.getCN(),
                          myWebertEmployeeClass.getMarital(),
                          myWebertEmployeeClass.getContactPerson(),
                          myWebertEmployeeClass.getCPRelationship(),
                          myWebertEmployeeClass.getCPNumber(),
                          myWebertEmployeeClass.getNumFinger());

                mySqlClass.addFingerToEmployee(WebertEmployeeClass.employeeID,
                    myWebertEmployeeClass.getLN(),
                    myWebertEmployeeClass.getGN(),
                    myWebertEmployeeClass.getMN(),
                    myWebertEmployeeClass.getFinger1(),
                    myWebertEmployeeClass.getFinger2(),
                    myWebertEmployeeClass.getFinger3(),
                    myWebertEmployeeClass.getFinger4());

                int[] fingerList = {myWebertEmployeeClass.getFinger1(),
                myWebertEmployeeClass.getFinger2(),
                myWebertEmployeeClass.getFinger3(),
                myWebertEmployeeClass.getFinger4()};

                mySqlClass.updateFingerList(fingerList);

                // This is set when browse button is clicked.
                // WebertEmployeeClass.pictureName = fileDialog.FileName;

                mySqlClass.addEmployeeImage(WebertEmployeeClass.pictureName,
                    WebertEmployeeClass.employeeID);

                refreshTables();
            }

           

            if ((inData.Contains("INCOMINGFINGER")) || inData.Contains(":"))
            {
                //MessageBox.Show("DEBUG");
                if (InvokeRequired)
                {
                    // after we've done all the processing, 
                    this.Invoke(new MethodInvoker(delegate
                    {
                       // MessageBox.Show("DEBUG");
                        if (tab.SelectedTab == tab.TabPages["attendanceTab"])
                        {
                            int terminator = inData.IndexOf(':');
                            int fingerID = int.Parse(inData.Substring(terminator + 1));
                            //MessageBox.Show("DEBUG");
                            //MessageBox.Show(fingerID.ToString(), "DEBUG");

                            int employeeID = mySqlClass.getEmpIDFromFingerID(fingerID);
                            //MessageBox.Show(employeeID.ToString());
                            if (employeeID != 0)
                            {
                                //MessageBox.Show("DEBUG");
                                mySqlClass.recordAttendance(employeeID);

                                if (mySqlClass.getDisplayInfo())
                                {
                                    nameLabel.Text = WebertSqlClass.currentName;
                                    actLabel.Text = WebertSqlClass.currentAct;
                                    attendancePBox.ImageLocation = mySqlClass.getEmployeeImageName(employeeID);
                                }

                                 
                            }
                            //else
                            //{
                            //    MessageBox.Show("Fingerprint id full. Reduce the number of fingerprints.",
                            //       "Error",
                            //        MessageBoxButtons.OK,
                            //        MessageBoxIcon.Error);
                            //}

                             
                            refreshTables();
                        }

                    }));
                    return;
                }
                else
                {
                    if (tab.SelectedTab == tab.TabPages["attendanceTab"])
                    {
                        int terminator = inData.IndexOf(':');
                        int fingerID = int.Parse(inData.Substring(terminator + 1));

                        //MessageBox.Show(fingerID.ToString(), "DEBUG");

                        int employeeID = mySqlClass.getEmpIDFromFingerID(fingerID);

                        if (employeeID != 0)
                        {
                            mySqlClass.recordAttendance(employeeID);
                        }

                        refreshTables();
                    }
                }
            }

            else if(inData.StartsWith("DELETE MODE DONE"))
            {
                mySqlClass.deleteEmployee(WebertEmployeeClass.employeeID);
                MessageBox.Show("Employee successfully deleted!", "Succes",
                    MessageBoxButtons.OK, MessageBoxIcon.Information);

                refreshTables();
            }

            else if(inData.StartsWith("All finger prints deleted!"))
            {
                refreshTables();
            }
        }

        private void addEmployeeButton_Click(object sender, System.EventArgs e)
        {
            try
            {
                // Switch focus to first textbox.
                this.ActiveControl = textBox1;

                // Create employee model.

                if (!string.IsNullOrWhiteSpace(textBox1.Text) &&
                    !string.IsNullOrWhiteSpace(textBox2.Text) &&
                    !string.IsNullOrWhiteSpace(textBox3.Text) &&
                    !string.IsNullOrWhiteSpace(textBox4.Text) &&
                    !string.IsNullOrWhiteSpace(textBox6.Text) &&
                    !string.IsNullOrWhiteSpace(textBox7.Text) &&
                    !string.IsNullOrWhiteSpace(textBox8.Text) &&
                    !string.IsNullOrWhiteSpace(textBox9.Text) &&
                    !string.IsNullOrWhiteSpace(textBox10.Text) &&
                    !string.IsNullOrWhiteSpace(textBox11.Text)
                    )

                {
                    //4 should be a number
                    int num1;

                    if (!(int.TryParse(textBox4.Text, out num1)))
                    {
                        MessageBox.Show("Age should be a number.", "Error",
                           MessageBoxButtons.OK, MessageBoxIcon.Information);
                        return;
                    }


                    myWebertEmployeeClass = new WebertEmployeeClass(
                        textBox1.Text,
                        textBox2.Text,
                        textBox3.Text,
                        textBox4.Text,
                        comboBox1.SelectedItem.ToString(),
                        textBox6.Text,
                        textBox7.Text,
                        textBox8.Text,
                        textBox9.Text,
                        textBox10.Text,
                        textBox11.Text,
                        comboBox2.SelectedItem.ToString());
                }
                else
                {
                    MessageBox.Show("All fields are required!", "Error",
                        MessageBoxButtons.OK, MessageBoxIcon.Information);

                    return;
                }


                /*
                     0 - LN
                     1 - GN
                     2 - MN
                     3 - Age
                     4 - Sex
                     5 - HA
                     6 - CN
                     7 - MS
                     8 - CP
                     9 - R
                     10 - CPN
                     11 - Salary
                     12 - NumFingerprint
                */

                // Check if number of finger required is available.

                int[] availableFinger = mySqlClass.getAvailableFinger(myWebertEmployeeClass.getNumFinger());


                // If available, register the employee and register the fingers available
                // to the employee.

                if (availableFinger[0] != 0)
                {
                    for (int i = 0; i < availableFinger.Length; i++)
                    {
                        // MessageBox.Show(availableFinger[i].ToString(), "Debug");

                        if (i == 0)
                        {
                            myWebertEmployeeClass.setFinger1(availableFinger[i]);
                        }
                        else if (i == 1)
                        {
                            myWebertEmployeeClass.setFinger2(availableFinger[i]);
                        }
                        else if (i == 2)
                        {
                            myWebertEmployeeClass.setFinger3(availableFinger[i]);
                        }
                        else if (i == 3)
                        {
                            myWebertEmployeeClass.setFinger4(availableFinger[i]);
                        }
                    }

                    string toSend = "ENROLLMODE";
                    toSend += ",";
                    toSend += myWebertEmployeeClass.getFinger1().ToString();
                    toSend += ",";
                    toSend += myWebertEmployeeClass.getFinger2().ToString();
                    toSend += ",";
                    toSend += myWebertEmployeeClass.getFinger3().ToString();
                    toSend += ",";
                    toSend += myWebertEmployeeClass.getFinger4().ToString();

                    atmegaPort.Write(toSend);

                    // Do this only after the finger print is registered in the scanner.
                    // Moved this to serial event when all the finger is registered.

                    /*
       
                    mySqlClass.addEmployee(myWebertEmployeeClass.getLN(),
                        myWebertEmployeeClass.getGN(),
                        myWebertEmployeeClass.getMN(),
                        myWebertEmployeeClass.getAge(),
                        myWebertEmployeeClass.getSex(),
                        myWebertEmployeeClass.getHA(),
                        myWebertEmployeeClass.getCN(),
                        myWebertEmployeeClass.getMarital(),
                        myWebertEmployeeClass.getContactPerson(),
                        myWebertEmployeeClass.getCPRelationship(),
                        myWebertEmployeeClass.getCPNumber(),
                        myWebertEmployeeClass.getSalary(),
                        myWebertEmployeeClass.getNumFinger());

                    mySqlClass.addFingerToEmployee(WebertEmployeeClass.employeeID,
                        myWebertEmployeeClass.getLN(),
                        myWebertEmployeeClass.getGN(),
                        myWebertEmployeeClass.getMN(),
                        myWebertEmployeeClass.getFinger1(),
                        myWebertEmployeeClass.getFinger2(),
                        myWebertEmployeeClass.getFinger3(),
                        myWebertEmployeeClass.getFinger4());

                     */
                }


          

                refreshTables();

            }
            catch (Exception exp)
            {
                //MessageBox.Show(exp.ToString());

                MessageBox.Show("Cannot connect to database.", "Error",
                   MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void updateEmployeeButton_Click(object sender, EventArgs e)
        {
            try
            {
                if (employee_infoDGV2.SelectedRows.Count > 0)
                {
                    // Switch focus to first textbox.
                    this.ActiveControl = textBox24;

                    if (!string.IsNullOrWhiteSpace(textBox24.Text) &&
                        !string.IsNullOrWhiteSpace(textBox23.Text) &&
                        !string.IsNullOrWhiteSpace(textBox22.Text) &&
                        !string.IsNullOrWhiteSpace(textBox21.Text) &&
                        !string.IsNullOrWhiteSpace(textBox19.Text) &&
                        !string.IsNullOrWhiteSpace(textBox18.Text) &&
                        !string.IsNullOrWhiteSpace(textBox17.Text) &&
                        !string.IsNullOrWhiteSpace(textBox16.Text) &&
                        !string.IsNullOrWhiteSpace(textBox15.Text) &&
                        !string.IsNullOrWhiteSpace(textBox14.Text)
                        )
                    {

                        //21;
                        int num1;

                        if (!(int.TryParse(textBox21.Text, out num1)))
                        {
                            MessageBox.Show("Age should be a number.", "Error",
                           MessageBoxButtons.OK, MessageBoxIcon.Information);
                            return;
                        }

                        myWebertEmployeeClass = new WebertEmployeeClass(
                        textBox24.Text,
                        textBox23.Text,
                        textBox22.Text,
                        textBox21.Text,
                        comboBox3.SelectedItem.ToString(),
                        textBox19.Text,
                        textBox18.Text,
                        textBox17.Text,
                        textBox16.Text,
                        textBox15.Text,
                        textBox14.Text);
                    }
                    else
                    {
                        MessageBox.Show("All fields are required!", "Error",
                           MessageBoxButtons.OK, MessageBoxIcon.Information);

                        return;
                    }



                    // MessageBox.Show(employee_infoDGV2.SelectedRows[0].Cells[0].Value.ToString());

                    mySqlClass.editEmployee(myWebertEmployeeClass.getLN(),
                        myWebertEmployeeClass.getGN(),
                        myWebertEmployeeClass.getMN(),
                        myWebertEmployeeClass.getAge(),
                        myWebertEmployeeClass.getSex(),
                        myWebertEmployeeClass.getHA(),
                        myWebertEmployeeClass.getCN(),
                        myWebertEmployeeClass.getMarital(),
                        myWebertEmployeeClass.getContactPerson(),
                        myWebertEmployeeClass.getCPRelationship(),
                        myWebertEmployeeClass.getCPNumber(),
                        int.Parse(employee_infoDGV2.SelectedRows[0].Cells[0].Value.ToString()));
                    // Last item is selected ID to be passed in the WebertSqlClass as a uniqe key to
                    // edit the database.

                    // This is set when browse button in edit is clicked.
                    // WebertEmployeeClass.pictureName = fileDialog.FileName;

                    WebertEmployeeClass.employeeID = int.Parse(employee_infoDGV2.SelectedRows[0].Cells[0].Value.ToString());
                    mySqlClass.addEmployeeImage(WebertEmployeeClass.pictureName,
                        WebertEmployeeClass.employeeID);

                    MessageBox.Show("Employee record updated!", "Success",
                        MessageBoxButtons.OK, MessageBoxIcon.Information);

                    refreshTables();
                }
                else
                {
                    MessageBox.Show("Select a row to edit!", "Error",
                        MessageBoxButtons.OK, MessageBoxIcon.Error);
                }

            }
            catch (Exception exp)
            {
                MessageBox.Show(exp.ToString());
                MessageBox.Show("Select a row to edit!", "Error",
                       MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void deleteEmployeeButton_Click(object sender, EventArgs e)
        {
            if (employee_infoDGV3.SelectedRows.Count > 0)
            {
                try
                {
                    foreach (DataGridViewRow row in employee_infoDGV3.SelectedRows)
                    {

                        if (MessageBox.Show("Are you sure you want to delete this employee?",
                            "Confirm",
                            MessageBoxButtons.YesNo,
                            MessageBoxIcon.Question) == DialogResult.Yes)
                        {
                            
                            int employeeID = int.Parse(row.Cells[0].Value.ToString());
                            // MessageBox.Show(employeeID.ToString());
                            WebertEmployeeClass.employeeID = employeeID;
                            int[] toDelete = mySqlClass.getFingerToDelete(employeeID);

                            string toSend = "DELETEMODE";
                            toSend += ",";
                            toSend += toDelete[0].ToString();
                            toSend += ",";
                            toSend += toDelete[1].ToString();
                            toSend += ",";
                            toSend += toDelete[2].ToString();
                            toSend += ",";
                            toSend += toDelete[3].ToString();

                            atmegaPort.Write(toSend);

                            loadImages();

                            // Move to serial event.
                            // We will delete the database only if the finger
                            // print is also deleted from the device.
                            // mySqlClass.deleteEmployee(employeeID);
                        }
                    }
                }
                catch (Exception exp)
                {
                    //MessageBox.Show(exp.ToString());

                    MessageBox.Show("Cannot connect to database.", "Error",
                   MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }
            else
            {
                MessageBox.Show("Select a row to delete!", "Error",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void employee_infoDGV2_CellClick(object sender, DataGridViewCellEventArgs e)
        {
            // MessageBox.Show(employee_infoDGV2.SelectedRows[0].Cells[0].Value.ToString());

            textBox24.Text = employee_infoDGV2.SelectedRows[0].Cells[1].Value.ToString();
            textBox23.Text = employee_infoDGV2.SelectedRows[0].Cells[2].Value.ToString();
            textBox22.Text = employee_infoDGV2.SelectedRows[0].Cells[3].Value.ToString();
            textBox21.Text = employee_infoDGV2.SelectedRows[0].Cells[4].Value.ToString();
            comboBox3.Text = employee_infoDGV2.SelectedRows[0].Cells[5].Value.ToString();
            textBox19.Text = employee_infoDGV2.SelectedRows[0].Cells[6].Value.ToString();
            textBox18.Text = employee_infoDGV2.SelectedRows[0].Cells[7].Value.ToString();
            textBox17.Text = employee_infoDGV2.SelectedRows[0].Cells[8].Value.ToString();
            textBox16.Text = employee_infoDGV2.SelectedRows[0].Cells[9].Value.ToString();
            textBox15.Text = employee_infoDGV2.SelectedRows[0].Cells[10].Value.ToString();
            textBox14.Text = employee_infoDGV2.SelectedRows[0].Cells[11].Value.ToString();

            int employeeID = int.Parse(employee_infoDGV2.SelectedRows[0].Cells[0].Value.ToString());
            editPBox.ImageLocation=mySqlClass.getEmployeeImageName(employeeID);

        }

        private void addEmployeeClearButton_Click(object sender, EventArgs e)
        {
            clearAddEmployeeTextBox();
        }

        private void editEmployeeClearButton_Click(object sender, EventArgs e)
        {
            clearEditEmployeeTextBox();
            employee_infoDGV2.ClearSelection();
        }

        // This function will be called whenever the fingerprintscanner receives
        // a finger id then it will check if it is in the database.
        // It will return the employee id associated with that finger id.

        private int checkFingerRegistered(int fingerID)
        {
            if (!(fingerID >= 1 && fingerID <= 127))
            {
                return 0;
            }

            int employeeID = mySqlClass.isEmployeeFingerRegistered(fingerID);

            if (employeeID != 0)
            {
                return employeeID;
            }

            return 0;
        }

        //private void updateWorkStatusButton_Click(object sender, EventArgs e)
        //{
        //    if (employee_workstatus_DGV.SelectedRows.Count > 0)
        //    {
        //        try
        //        {
        //            if (!(MessageBox.Show("Are you sure you want to update work status for this employee?",
        //                 "Update Work Status",
        //                 MessageBoxButtons.YesNo,
        //                 MessageBoxIcon.Information) == DialogResult.Yes))
        //            {
        //                return;
        //            }

        //            foreach (DataGridViewRow row in employee_workstatus_DGV.SelectedRows)
        //            {
        //                int employeeID = int.Parse(row.Cells[0].Value.ToString());
        //                //MessageBox.Show(employeeID.ToString());

        //                // Change work status, unique employee id.
        //                if(mySqlClass.updateWorkStatus(employeeID, workStatusCB.SelectedItem.ToString())>0)
        //                {
        //                    MessageBox.Show("Work Status Updated", "Success",
        //                        MessageBoxButtons.OK, MessageBoxIcon.Information);
        //                }

        //                refreshTables();
        //            }
        //        }
        //        catch (Exception exp)
        //        {
        //            // MessageBox.Show(exp.ToString());

        //            MessageBox.Show("Cannot connect to database.", "Error",
        //           MessageBoxButtons.OK, MessageBoxIcon.Error);
        //        }
        //    }
        //    else
        //    {
        //        MessageBox.Show("Select a row to update!", "Error",
        //            MessageBoxButtons.OK, MessageBoxIcon.Error);
        //    }
        //}

        private void updateRemarksButton_Click(object sender, EventArgs e)
        {
            if (employee_attendanceDGV2.SelectedRows.Count > 0)
            {
                try
                {
                   if (!(MessageBox.Show("Are you sure you want to update remarks for this employee?",
                        "Update Remarks",
                        MessageBoxButtons.YesNo,
                        MessageBoxIcon.Information)==DialogResult.Yes))
                    {
                        return;
                    }

                    if (remarksCB.SelectedItem.ToString().Equals("Over Time"))
                    {
                        foreach (DataGridViewRow row in employee_attendanceDGV2.SelectedRows)
                        {
                            int attendanceID = int.Parse(row.Cells[0].Value.ToString());
                            //MessageBox.Show(attendanceID.ToString());

                            // Change remarks, unique attendance ID.
                            int otHours;

                            bool isNum = int.TryParse(OTHoursEdit.Text, out otHours);

                            if(!(isNum && otHours > 0))
                            {
                                MessageBox.Show("Over time rate must be a number greater than 0",
                                    "Error",
                                    MessageBoxButtons.OK,
                                    MessageBoxIcon.Error);

                                return;
                            }

                            if (mySqlClass.updateRemarks(attendanceID, remarksCB.SelectedItem.ToString(), otHours) > 0)
                            {
                                MessageBox.Show("Remarks Updated", "Success",
                                   MessageBoxButtons.OK, MessageBoxIcon.Information);
                            }

                            refreshTables();
                        }
                    }
                    else
                    {
                        foreach (DataGridViewRow row in employee_attendanceDGV2.SelectedRows)
                        {
                            int attendanceID = int.Parse(row.Cells[0].Value.ToString());
                            //MessageBox.Show(attendanceID.ToString());

                            // Change remarks, unique attendance ID.

                            if (mySqlClass.updateRemarks(attendanceID, remarksCB.SelectedItem.ToString()) > 0)
                            {
                                MessageBox.Show("Remarks Updated", "Success",
                                   MessageBoxButtons.OK, MessageBoxIcon.Information);
                            }

                            refreshTables();
                        }
                    }
                }
                catch (Exception exp)
                {
                    MessageBox.Show(exp.ToString());

                    MessageBox.Show("Cannot connect to database.", "Error",
                   MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }
            else
            {
                MessageBox.Show("Select a row to update!", "Error",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void generateSalaryReportButton_Click(object sender, EventArgs e)
        {
            //MessageBox.Show(dateFrom.Value.ToShortDateString());
            //MessageBox.Show(dateTo.Value.ToShortDateString());

            if(mySqlClass.computeSalary(dateFrom.Value.ToShortDateString(),
                dateTo.Value.ToShortDateString()))
            {
                MessageBox.Show("Salary Report Generated", "Success",
                    MessageBoxButtons.OK, MessageBoxIcon.Information);

                refreshTables();
            }
            else
            {
                MessageBox.Show("Range Selected is invalid or no record found.", "No record",
                   MessageBoxButtons.OK, MessageBoxIcon.Information);

                refreshTables();
            }
        }

        private void removeTimeInButton_Click(object sender, EventArgs e)
        {
            
            if (employee_attendanceDGV2.SelectedRows.Count > 0)
            {
                try
                {
                    if (!(MessageBox.Show("Are you sure you want to remove time in for this employee?",
                             "Remove Time In",
                             MessageBoxButtons.YesNo,
                             MessageBoxIcon.Information) == DialogResult.Yes))
                    {
                        return;
                    }

                    foreach (DataGridViewRow row in employee_attendanceDGV2.SelectedRows)
                    {
                        int attendanceID = int.Parse(row.Cells[0].Value.ToString());
                        //MessageBox.Show(attendanceID.ToString());
                        mySqlClass.removeTimeIn(attendanceID);
                    }

                    MessageBox.Show("Time In Removed", "Success",
                   MessageBoxButtons.OK, MessageBoxIcon.Information);

                    refreshTables();
                }
                catch(Exception exp)
                {
                    //MessageBox.Show(exp.ToString());

                    MessageBox.Show("Cannot connect to database.", "Error",
                   MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }
            else
            {
                MessageBox.Show("Select a row to update!", "Error",
                   MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void removeTimeOutButton_Click(object sEender, EventArgs e)
        {
            if(employee_attendanceDGV2.SelectedRows.Count>0)
            {
                try
                {
                    if (!(MessageBox.Show("Are you sure you want to remove time out for this employee?",
                         "Remove Time Out",
                         MessageBoxButtons.YesNo,
                         MessageBoxIcon.Information) == DialogResult.Yes))
                    {
                        return;
                    }

                    foreach (DataGridViewRow row in employee_attendanceDGV2.SelectedRows)
                    {
                        int attendanceID = int.Parse(row.Cells[0].Value.ToString());
                        
                        mySqlClass.removeTimeOut(attendanceID);
                    }

                    MessageBox.Show("Time Out Removed", "Success",
                MessageBoxButtons.OK, MessageBoxIcon.Information);

                    refreshTables();
                }
                catch(Exception exp)
                {
                    //MessageBox.Show(exp.ToString());
                    MessageBox.Show("Cannot connect to database.", "Error",
                   MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }
            else
            {
                MessageBox.Show("Select a row to update!", "Error",
                   MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        // Version 1 save excel.
        // More simple and does not depend on library.
        // But it cannot copy formats.
        //private void ToCsV(DataGridView dGV, string filename)
        //{
        //    string stOutput = "";
        //    // Export titles:
        //    string sHeaders = "";

        //    for (int j = 0; j < dGV.Columns.Count; j++)
        //        sHeaders = sHeaders.ToString() + Convert.ToString(dGV.Columns[j].HeaderText) + "\t";

        //    stOutput += sHeaders + "\r\n";
        //    // Export data.
        //    for (int i = 0; i < dGV.RowCount - 1; i++)
        //    {
        //        string stLine = "";
        //        for (int j = 0; j < dGV.Rows[i].Cells.Count; j++)
        //            stLine = stLine.ToString() + Convert.ToString(dGV.Rows[i].Cells[j].Value) + "\t";
        //        stOutput += stLine + "\r\n";
        //    }

        //    Encoding utf16 = Encoding.GetEncoding(1254);
        //    byte[] output = utf16.GetBytes(stOutput);
        //    FileStream fs = new FileStream(filename, FileMode.Create);
        //    BinaryWriter bw = new BinaryWriter(fs);
        //    bw.Write(output, 0, output.Length); //write the encoded file
        //    bw.Flush();
        //    bw.Close();
        //    fs.Close();
        //}

        public void SaveToExcelFile(System.Data.DataTable dt, string filename)
        {
            Microsoft.Office.Interop.Excel.Application app =
                new Microsoft.Office.Interop.Excel.Application();
            try
            {
                Workbook wb = app.Workbooks.Add(1);
                Worksheet ws = (Worksheet)wb.Worksheets[1];
             

                // export column headers
                for (int colNdx = 0; colNdx < dt.Columns.Count; colNdx++)
                {
                    ws.Cells[1, colNdx + 1] = dt.Columns[colNdx].ColumnName;
                }

                // export data
                for (int rowNdx = 0; rowNdx < dt.Rows.Count; rowNdx++)
                {
                    for (int colNdx = 0; colNdx < dt.Columns.Count; colNdx++)
                    {
                        ws.Cells[rowNdx + 2, colNdx + 1] = GetString(dt.Rows[rowNdx][colNdx]);
                    }
                }

                Microsoft.Office.Interop.Excel.Range usedrange = ws.UsedRange;
                usedrange.Columns.AutoFit();
                usedrange.HorizontalAlignment =
                                Microsoft.Office.Interop.Excel.XlHAlign.xlHAlignCenter;
                wb.SaveAs(filename, Type.Missing, Type.Missing, Type.Missing,
                    Type.Missing, Type.Missing, XlSaveAsAccessMode.xlNoChange,
                    Type.Missing, Type.Missing, Type.Missing,
                    Type.Missing, Type.Missing);
                wb.Close(false, Type.Missing, Type.Missing);

            }
            finally
            {
                app.Quit();
            }

        }

        private string GetString(object o)
        {
            if (o == null)
                return "";
            return o.ToString();
        }

        private void expExcelButton_Click(object sender, EventArgs e)
        {
            SaveFileDialog sfd = new SaveFileDialog();
            sfd.Filter = "Excel Documents (*.xls)|*.xls";
            sfd.FileName = "ToExport.xls";

            if (sfd.ShowDialog() == DialogResult.OK)
            {
                //MessageBox.Show(Path.GetFullPath(sfd.FileName));
                string pathWithName = Path.GetFullPath(sfd.FileName);
                SaveToExcelFile(mySqlClass.getSalaryReportInfoTable(), pathWithName);
            }
        }

        private void changePassCB_CheckedChanged(object sender, EventArgs e)
        {
            if(changePassCB.Checked)
            {
                currPassTB.Enabled = true;
                newPassTB.Enabled = true;
                confirmPassTB.Enabled = true;
            }
            else
            {
                currPassTB.Enabled = false;
                newPassTB.Enabled = false;
                confirmPassTB.Enabled = false;
            }
        }

        private void resetSystemButton_Click(object sender, EventArgs e)
        {
            try
            {
                string ans = "";

                if (InputBox("Reset", "Are you sure you want to reset the system?\n" +
                    "This will delete all the records and the finger prints\n" +
                    "Enter password to proceed.", ref ans) == DialogResult.OK)
                {
                    //MessageBox.Show(ans);

                    if(mySqlClass.isPasswordCorrect(ans))
                    {
                        if(portLoaded)
                        {
                            try
                            {

                                MessageBox.Show("Reset ready, click OK to continue.\n" +
                                    "This may take a few minute...", "Reset");
                                atmegaPort.Write("RESET");
                                string scriptCommands = File.ReadAllText("startdbscript.sql");

                                MessageBox.Show("Resetting please wait...", "Reset",
                          MessageBoxButtons.OK, MessageBoxIcon.Information);

                                mySqlClass.resetdatabase(scriptCommands);

                               // atmegaPort.Write("RESET");


                                MessageBox.Show("Database reset success!", "Success",
                           MessageBoxButtons.OK, MessageBoxIcon.Information);

                                refreshTables();
                                loadImages();
                            }
                            catch(Exception exp)
                            {
                                //MessageBox.Show(exp.ToString());

                                MessageBox.Show("Cannot connect to database", "Error",
                                MessageBoxButtons.OK, MessageBoxIcon.Error);
                            }

                        }
                        else
                        {
                            MessageBox.Show("Device not connected!", "Error",
                                MessageBoxButtons.OK, MessageBoxIcon.Error);
                        }
                    }
                    else
                    {
                        MessageBox.Show("Invalid current password!", "Error",
                                MessageBoxButtons.OK, MessageBoxIcon.Error);
                    }
                }
            }
            catch(Exception exp)
            {
               // MessageBox.Show(exp.ToString());
                MessageBox.Show("Cannot connect to database", "Error",
                              MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void updateLoggedUserButton_Click(object sender, EventArgs e)
        {
            try
            {
                if (MessageBox.Show("Are you sure you want to update username and/or password?",
                   "Update", MessageBoxButtons.OK, MessageBoxIcon.Information) == DialogResult.OK)
                {
                    string uname = uNameTB.Text;
                    uname = uname.Trim();

                    if(changePassCB.Checked)
                    {
                        string currPass = currPassTB.Text;
                        string newPass = newPassTB.Text;
                        string confirmPass = confirmPassTB.Text;

                        if (!String.IsNullOrWhiteSpace(uname) &&
                                !String.IsNullOrWhiteSpace(currPass) &&
                                !String.IsNullOrWhiteSpace(newPass) &&
                                !String.IsNullOrWhiteSpace(confirmPass))
                        {

                            if (mySqlClass.isPasswordCorrect(currPass))
                            {
                                // Change username and password.
                                if (newPass.Equals(confirmPass))
                                {
                                    mySqlClass.changeAdminInfo(uname, newPass);
                                    MessageBox.Show("User credentials updated!", "Success", MessageBoxButtons.OK,
                                    MessageBoxIcon.Information);

                                    currPassTB.Text = "";
                                    newPassTB.Text = "";
                                    confirmPassTB.Text = "";
                                    changePassCB.Checked = false;
                                }
                                else
                                {
                                    MessageBox.Show("Password confirmation failed.", "Error",
                                        MessageBoxButtons.OK, MessageBoxIcon.Error);
                                }
                            }
                            else
                            {
                                MessageBox.Show("Invalid current password!", "Error",
                                    MessageBoxButtons.OK, MessageBoxIcon.Error);
                            }
                        }
                        else
                        {
                            MessageBox.Show("All fields are required", "Error",
                                    MessageBoxButtons.OK, MessageBoxIcon.Error);
                        }
                    }
                    else
                    {
                        // Change username only.

                        if (!String.IsNullOrWhiteSpace(uname))
                        {
                            mySqlClass.changeAdminInfo(uname);
                            MessageBox.Show("User credentials updated!", "Success", MessageBoxButtons.OK,
                                MessageBoxIcon.Information);
                        }
                        else
                        {
                            MessageBox.Show("Empty username", "Error", MessageBoxButtons.OK,
                                MessageBoxIcon.Error);
                        }
                    }

                    loadAdminInfo();
                }
            }
            catch(Exception exp)
            {
                //MessageBox.Show("Invalid input!",
                //   "Error", MessageBoxButtons.OK, MessageBoxIcon.Information);
                MessageBox.Show("Cannot connect to database.", "Error",
                   MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void updateEmployeeSalaryButton_Click(object sender, EventArgs e)
        {
            try
            {
                if(MessageBox.Show("Are you sure you want to update employee's salary rate?",
                    "Update", MessageBoxButtons.OK,MessageBoxIcon.Information)==DialogResult.OK)
                {
                    int[] salaryList = new int[4];

                    salaryList[0] = int.Parse(FTSTB.Text);
                    salaryList[1] = int.Parse(HTSTB.Text);
                    salaryList[2] = int.Parse(OTTB.Text);
                    salaryList[3] = int.Parse(LateSalaryTB.Text);

                    mySqlClass.setSalaryIfo(salaryList);

                     MessageBox.Show("Employee salary credentials updated!", "Success", MessageBoxButtons.OK,
                        MessageBoxIcon.Information);

                    loadAdminInfo();
                }
            }
            catch(Exception exp)
            {
                //MessageBox.Show("Invalid input! Please enter a number!",
                //    "Error", MessageBoxButtons.OK, MessageBoxIcon.Information);
                MessageBox.Show(exp.ToString());
            }
        }

        public static DialogResult InputBox(string title, string promptText, ref string value)
        {
            Form form = new Form();
            System.Windows.Forms.Label label = new System.Windows.Forms.Label();
            System.Windows.Forms.TextBox textBox = new System.Windows.Forms.TextBox();
            System.Windows.Forms.Button buttonOk = new System.Windows.Forms.Button();
            System.Windows.Forms.Button buttonCancel = new System.Windows.Forms.Button();

            form.Text = title;
            label.Text = promptText;
            textBox.Text = value;

            buttonOk.Text = "OK";
            buttonCancel.Text = "Cancel";
            buttonOk.DialogResult = DialogResult.OK;
            buttonCancel.DialogResult = DialogResult.Cancel;

            label.SetBounds(9, 20, 372, 13);
            textBox.SetBounds(12, 70, 372, 20);
            textBox.UseSystemPasswordChar = true;
            buttonOk.SetBounds(228, 92, 75, 23);
            buttonCancel.SetBounds(309, 92, 75, 23);

            label.AutoSize = true;
            textBox.Anchor = textBox.Anchor | AnchorStyles.Right;
            buttonOk.Anchor = AnchorStyles.Bottom | AnchorStyles.Right;
            buttonCancel.Anchor = AnchorStyles.Bottom | AnchorStyles.Right;

            form.ClientSize = new Size(396, 140);
            form.Controls.AddRange(new Control[] { label, textBox, buttonOk, buttonCancel });
            form.ClientSize = new Size(Math.Max(300, label.Right + 10), form.ClientSize.Height);
            form.FormBorderStyle = FormBorderStyle.FixedDialog;
            form.StartPosition = FormStartPosition.CenterScreen;
            form.MinimizeBox = false;
            form.MaximizeBox = false;
            form.AcceptButton = buttonOk;
            form.CancelButton = buttonCancel;

            DialogResult dialogResult = form.ShowDialog();
            value = textBox.Text;
            return dialogResult;
        }

        private void remarksCB_SelectedIndexChanged(object sender, EventArgs e)
        {
            //MessageBox.Show(remarksCB.SelectedItem.ToString());

            if(remarksCB.SelectedItem.ToString().Equals("Over Time"))
            {
                OTHoursEdit.Enabled = true;
            }
            else
            {
                OTHoursEdit.Enabled = false;
            }
        }

        private void toolStripLabel1_Click(object sender, EventArgs e)
        {
            mySqlClass.closeDatabase();
            atmegaPort.Close();
            this.Hide();
            new LoginForm().Show();
        }

        private void dateSort_ValueChanged(object sender, EventArgs e)
        {
            //MessageBox.Show(dateSort.Value.ToShortDateString());

            WebertSqlClass.attendanceDateShown = dateSort.Value.ToShortDateString();
            refreshTables();
        }

        private void showAllAttendanceButton_Click(object sender, EventArgs e)
        {
            WebertSqlClass.attendanceDateShown = "1";
            refreshTables();
        }

        private void toolStripLabel2_Click(object sender, EventArgs e)
        {
            string aboutMessage = "Webert Employee Management and Weekly Gross Income System\n\nDeveloped by:\n- Divina, Paul Daniel \n- Felices, Philip John\n- Teves, Nicodemus";
     
            MessageBox.Show(aboutMessage,"About",
                MessageBoxButtons.OK,
                MessageBoxIcon.Information);
            
        }

        private void toolStripLabel3_Click(object sender, EventArgs e)
        {
            string helpMessage = "To add employees select add employee\n- Apply all fields.\n- Insert Picture of Employee.\n- Select how many fingers to register.\n- Register fingerprint.\n\nTo edit an employee select edit employee\n- Select an employee to be edited.\n- Edit desired fields.\n- Note: You cannot edit an employee’s finger.\n- To delete an employee select delete employee.\n- Select employee to be deleted, select .\n- Select yes, wait for complete deletion.\n\nTo delete an employee select delete employee\n- Select employee to be deleted, select \n- Select yes, wait for complete deletion\n\nTo edit the attendance remarks of employee select edit remarks\n- Select an employee to be edited.\n- Select what desired remarks must be selected.\n\nTo view and generate salary report select salary report\n- Select generate salary to generate salary of employee.\n- Select salary report to view the salary of employees in an excel file.\n\nTo manage admin select manage admin\n- Select manage admin.\n- Options can be selected such as editing salary, editing admin password, and resetting the system.\n- Changing admin passwords.";


            MessageBox.Show(helpMessage, "Help",
                MessageBoxButtons.OK,
                MessageBoxIcon.None);
        }

        private void addBrowse_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        {
            OpenFileDialog fileDialog = new OpenFileDialog();

            if(fileDialog.ShowDialog()==DialogResult.OK)
            {
                //MessageBox.Show(fileDialog.FileName);
                addPBox.ImageLocation = fileDialog.FileName;
                addPBox.SizeMode = PictureBoxSizeMode.StretchImage;
                WebertEmployeeClass.pictureName = fileDialog.FileName;
            }
        }

        private void editBrowse_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        {
            OpenFileDialog fileDialog = new OpenFileDialog();

            if (fileDialog.ShowDialog() == DialogResult.OK)
            {
                //MessageBox.Show(fileDialog.FileName);
                editPBox.ImageLocation = fileDialog.FileName;
                editPBox.SizeMode = PictureBoxSizeMode.StretchImage;
                WebertEmployeeClass.pictureName = fileDialog.FileName;
            }
        }

        public void  setNameLabel(string name, string activity)
        {
            nameLabel.Text = name;
            actLabel.Text = activity;
        }


    }
 }

