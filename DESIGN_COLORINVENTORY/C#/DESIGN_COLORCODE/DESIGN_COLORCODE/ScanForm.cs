using System.IO.Ports;
using System.Windows.Forms;

namespace DESIGN_COLORCODE
{
    public partial class ScanForm : Form
    {
        SMAInventory_Model smaInventory = new SMAInventory_Model();

        private bool isPortConnected;
        SerialPort bluetoothPort;


        public ScanForm()
        {
            InitializeComponent();
            loadPortStatus();
            loadPorts();
        }

        private void backButton_Click(object sender, System.EventArgs e)
        {
            this.disconnectPort();

            AdminForm adminForm = new AdminForm();
            adminForm.Show();
            this.Hide();
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

        private void connectButton_Click(object sender, System.EventArgs e)
        {
            this.connectPort();

        }

        private void disconnect_Click(object sender, System.EventArgs e)
        {
            this.disconnectPort();
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
                // indata is the color code in the letter format.
                // Ex: red,red,red,orange,blue

                string indata = sp.ReadLine();

                //MessageBox.Show(indata.ToString());

                string colorStringNum = SMAInventory_Model.convertColorNameToStringNum(indata);

                if(MessageBox.Show("Color Pattern is: " + indata + "\nProceed?", "Confirm"
                    ,MessageBoxButtons.YesNo,
                    MessageBoxIcon.Information)==DialogResult.No)
                {
                    return;
                }

                SMAInventory_Model smaInventory = new SMAInventory_Model();
                

                if (smaInventory.isColorStringNumExists(indata))
                {
                    // First three color code exists.
                    // Open edit item window.


                    // Note that the port should be closed first before invoking a new thread.
                    bluetoothPort.Close();
                    isPortConnected = false;

                    // Start a new thread.
                    // Only use this if needed.

                    if (InvokeRequired)
                    {
                        // after we've done all the processing, 
                        this.Invoke(new MethodInvoker(delegate
                        {
                            // load the control with the appropriate data
                            //MessageBox.Show("New thread created.");

                           
                            this.disconnectPort();
                            string colorCode = smaInventory.convertStringNumToColorName(indata);
                            //MessageBox.Show(colorCode);

                            EditForm editForm = new EditForm(colorCode);
                            editForm.Show();
                            this.Hide();


                        }));

                    }

                }
                else
                {
                    // First  color code does not exists.
                    // Open add item window.

                     // Note that the port should be closed first before invoking a new thread.
                    bluetoothPort.Close();
                    isPortConnected = false;

                    // Start a new thread.
                    // Only use this if needed.

                    if (InvokeRequired)
                    {
                        // after we've done all the processing, 
                        this.Invoke(new MethodInvoker(delegate
                        {
                            // load the control with the appropriate data
                            //MessageBox.Show("New thread created.");


                            this.disconnectPort();
                            AddItemForm addItemForm = new AddItemForm(colorStringNum);
                            addItemForm.Show();
                            this.Hide();

                        }));

                    }


                }

                
            }
        }

        void connectPort()
        {
            string selectedPort = "";

            // Check first if there exists one port.
            if (portListCB.Items.Count > 0)
            {
                selectedPort = portListCB.SelectedItem.ToString();
            }

            // Connect to the selected port if it exists.
            if (!string.IsNullOrEmpty(selectedPort))
            {
                bluetoothPort = new SerialPort(selectedPort, 9600);


                if (!isPortConnected)
                {
                    bluetoothPort.Open();
                    bluetoothPort.DataReceived += new SerialDataReceivedEventHandler(DataReceivedHandler);
                    isPortConnected = true;
                }
            }

            loadPortStatus();

        }
        void disconnectPort()
        {
            if (isPortConnected)
            {
                bluetoothPort.Close();
                isPortConnected = false;
            }

            loadPortStatus();
        }

        private void ScanForm_FormClosing(object sender, FormClosingEventArgs e)
        {
            Application.Exit();
        }
    }
}
