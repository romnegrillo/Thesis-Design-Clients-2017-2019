using System;
using System.Windows.Forms;
using System.IO.Ports;
using System.Data.OleDb;

namespace Rice_design
{
    public partial class Form1 : Form
    {

        public static SerialPort Ard;
        public bool isConnected=false;
        string temp;
        string moist;
        string count;
        bool saveAllEnabled = false;

        public Form1()
        {
            InitializeComponent();
            loadPorts();
        }

        private void loadPorts()
        {
            string[] ports = SerialPort.GetPortNames();

            foreach (string item in ports)
            {
                comboBox1.Items.Add(item);
            }
        }

        private void button2_Click(object sender, EventArgs e)
        {
            //dis
            Dis();
        }

        private void button3_Click(object sender, EventArgs e)
        {

            string selected = comboBox1.GetItemText(this.comboBox1.SelectedItem);

            if (!String.IsNullOrEmpty(selected))
            {
                //MessageBox.Show(selected);
                Con(selected);
            }
            else
            {
                MessageBox.Show("Invalid serial port!",
                "Error",
                MessageBoxButtons.OK,
                MessageBoxIcon.Error);
            }

        }

        public void Con(string portName)
        {
            try
            {
                if (!isConnected)
                {
                    Ard = new SerialPort(portName);

                    Ard.BaudRate = 9600;
                    Ard.Parity = Parity.None;
                    Ard.StopBits = StopBits.One;
                    Ard.DataBits = 8;
                    Ard.Handshake = Handshake.None;
                    Ard.RtsEnable = true;
                    Ard.DataReceived += new SerialDataReceivedEventHandler(DataReceivedHandler);

                    Ard.Open();

                    isConnected = true;


                    MessageBox.Show("Port successfully connected!",
                    "Success",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Information);
                }
            }
            catch
            {
                MessageBox.Show("Cannot connect to the selected port!",
                    "Error",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error);
            }

        }

        public void Dis()
        {
            try
            {
                if (isConnected)
                {
                    Ard.Close();
                    isConnected = false;

                    MessageBox.Show("Port successfully disconnected!",
                    "Success",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Information);

                }
            }
            catch (System.NullReferenceException)
            {
                MessageBox.Show("Cannot connect to the selected port!",
                "Error",
                MessageBoxButtons.OK,
                MessageBoxIcon.Error);
            }
        }

        private void DataReceivedHandler(
                    object sender,
                    SerialDataReceivedEventArgs e)
        {
            try
            {
                SerialPort sp = (SerialPort)sender;
                string indata = sp.ReadLine();

                indata = indata.Substring(0, indata.Length - 1);
                string[] words = indata.Split(',');
                string count = DateTime.Now.ToString("h:mm:ss tt");

                this.count = count;
                this.moist = words[0];
                this.temp = words[1];

                //MessageBox.Show(count + " " + words[0] + " " + words[1]);


                if (InvokeRequired)
                {
                    // after we've done all the processing, 
                    this.Invoke(new MethodInvoker(delegate {
                        // load the control with the appropriate data
                        tempLabel.Text = this.temp;
                        moistLabel.Text = this.moist;
                    }));                  
         
                }
                else
                {
                    tempLabel.Text = this.temp;
                    moistLabel.Text = this.moist;
                }


                if (saveAllEnabled)
                {
                    OleDbConnection MyConnection;
                    OleDbCommand myCommand = new OleDbCommand();
                    string sql = null;

                    MyConnection = new OleDbConnection(@"provider=Microsoft.Jet.OLEDB.4.0; Data Source=Data.xlsx; Extended Properties=""Excel 8.0;HDR=Yes;""");
                    MyConnection.Open();

                    myCommand.Connection = MyConnection;

                    sql = "Insert into [Sheet1$] (Log,Moisture,Temperature) Values ('" + this.count + "'," + this.moist + "," + this.temp + ")";
                    myCommand.CommandText = sql;

                    myCommand.ExecuteNonQuery();

                    MyConnection.Close();

                }


            }
            catch(Exception exp)
            {
                MessageBox.Show("Error writing to excel file!",
                    "Error",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error);

                //MessageBox.Show(exp.ToString());
            }
        }

        private void button1_Click(object sender, EventArgs e)
        {
            if(isConnected && !saveAllEnabled)
            {
                try
                {
                    OleDbConnection MyConnection;
                    OleDbCommand myCommand = new OleDbCommand();
                    string sql = null;

                    MyConnection = new OleDbConnection(@"provider=Microsoft.Jet.OLEDB.4.0; Data Source=Data.xlsx; Extended Properties=""Excel 8.0;HDR=Yes;""");
                    MyConnection.Open();

                    myCommand.Connection = MyConnection;

                    sql = "Insert into [Sheet1$] (Log,Moisture,Temperature) Values ('" + this.count + "'," + this.moist + "," + this.temp + ")";
                    myCommand.CommandText = sql;

                    myCommand.ExecuteNonQuery();

                    MyConnection.Close();

                    MessageBox.Show("Reading saved!",
                            "Success",
                            MessageBoxButtons.OK,
                            MessageBoxIcon.Information);
                }
                catch
                {
                    MessageBox.Show("Error writing to excel file!",
                    "Error",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error);
                }
            }
        
            else
            {
                MessageBox.Show("You are not connected.",
                "Error",
                MessageBoxButtons.OK,
                MessageBoxIcon.Error);
            }
        }

        private void button4_Click(object sender, EventArgs e)
        {
            if(!saveAllEnabled)
            {
                saveAllEnabled = true;

                MessageBox.Show("Real time saving enabled!",
                    "Success",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Information);
            }
            else
            {
                saveAllEnabled = false;

                MessageBox.Show("Real time saving disabled!",
                "Success",
                MessageBoxButtons.OK,
                MessageBoxIcon.Information);
            }
        }
    }
}
