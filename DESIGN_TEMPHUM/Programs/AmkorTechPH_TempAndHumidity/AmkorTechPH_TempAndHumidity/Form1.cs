using System.Windows.Forms;
using System.IO.Ports;

namespace AmkorTechPH_TempAndHumidity
{
    public partial class MainForm : MetroFramework.Forms.MetroForm
    {
        AmkorTechPH_SQL sqlObj;
        SerialPort atmegaPort;
        bool isPortConnected;

        public MainForm()
        {
            InitializeComponent();

            isPortConnected = false;

            loadDatabase();
            loadPortStatus();
            loadPorts();

            metroTabControl1.SelectedIndex = 0;
        }

        private void loadPortStatus()
        {
            if (!isPortConnected)
            {
                connectionLabel.Text = "Not Connected";
                connectionLabel.ForeColor = System.Drawing.Color.Red;
                disconnect.Enabled = false;
                connectButton.Enabled = true;
                portListCB.Enabled = true;
            }
            else
            {
                connectionLabel.Text = "Connected";
                connectionLabel.ForeColor = System.Drawing.Color.Green;
                connectButton.Enabled = false;
                disconnect.Enabled = true;
                portListCB.Enabled = false;
            }
        }

        // This funciton loads the database.
        private void loadDatabase()
        {
            sqlObj = new AmkorTechPH_SQL("amkortechph_database.db");

            // Fill the space.
            dgv.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill;
            dgv.DataSource = sqlObj.getData();
        }

        // This function loads all available serial ports.
        private void loadPorts()
        {
            // List all available ports.
            string[] ports = SerialPort.GetPortNames();

           // Add available ports to combobox.
            foreach (string port in ports)
            {
                portListCB.Items.Add(port);
            }

            // Make combobox non editable and select the first item on the list.
            portListCB.DropDownStyle = ComboBoxStyle.DropDownList;

            // Check first if there is atleast one item available.
            if (portListCB.Items.Count > 0)
            {
                portListCB.SelectedIndex = 0;
            }
        }

        // This function is called when you want to connect to the selected port
        // on button press. It will open the serial port and connect that port
        // on a serial event when data is sent from the device, atmega.
        private void connectButton_Click(object sender, System.EventArgs e)
        {
            //MessageBox.Show(portListCB.SelectedItem.ToString());

            string selectedPort = "";

            // Check first if there exists one port.
            if (portListCB.Items.Count > 0)
            {
                selectedPort = portListCB.SelectedItem.ToString();
            }

            // Connect to the selected port if it exists.
            if(!string.IsNullOrEmpty(selectedPort))
            {
                atmegaPort = new SerialPort(selectedPort,9600);
                

                if (!isPortConnected)
                {
                    atmegaPort.Open();
                    atmegaPort.DataReceived += new SerialDataReceivedEventHandler(DataReceivedHandler);
                    isPortConnected = true;
                }
            }

            loadPortStatus();

        }

        private void disconnect_Click(object sender, System.EventArgs e)
        {
            if (isPortConnected)
            {
                atmegaPort.Close();
                tempLabel.Text = "-";
                relHumidLabel.Text = "-";
                isPortConnected = false;
            }

            loadPortStatus();
        }

        // This function is called when a serial data is received from the device.
        private void DataReceivedHandler(
                       object sender,
                       SerialDataReceivedEventArgs e)
        {
            // Check first if port is open.
            if (isPortConnected)
            {
                SerialPort sp = (SerialPort)sender;
                string indata = sp.ReadLine();

                // Check if the length of indata is seven.
                // Seven because of the pattern XX,YY\r\n
                // where XX is the temperature data and YY 
                // is the humidity data.

                //MessageBox.Show(indata.ToString());

                if (indata.Length==6)
                //if(true)
                {
                    // Start a new thread.

                    if (InvokeRequired)
                    {
                        // after we've done all the processing, 
                        this.Invoke(new MethodInvoker(delegate
                        {
                            // load the control with the appropriate data

                            // If it is seven, we extract the XX and YY pattern then display
                            // it and update the database.

                            try
                            {
                                int temp = int.Parse(indata.Substring(0, 2));
                                int relHumid = int.Parse(indata.Substring(3, 2));

                                tempLabel.Text = temp.ToString() + "°C";
                                relHumidLabel.Text = relHumid.ToString() + "%";

                                sqlObj.addData(temp, relHumid);

                                loadDatabase();
                            }
                            catch
                            {
                                return;
                            }

                            //atmegaPort.DiscardInBuffer();
                            //atmegaPort.DiscardOutBuffer();

                        }));
                        return;
                    }

                }
            }
        }

        private void clearHistoryButton_Click(object sender, System.EventArgs e)
        {
            var result=MetroFramework.MetroMessageBox.Show(this, "Are you sure you want to clear history?",
                "Clear History", MessageBoxButtons.YesNo, MessageBoxIcon.Warning);

            if (result == DialogResult.Yes)
            {
                sqlObj.clearData();
                loadDatabase();
            }
        }
    }
}
