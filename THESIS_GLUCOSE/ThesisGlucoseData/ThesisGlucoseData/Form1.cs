using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO.Ports;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace ThesisGlucoseData
{
    public partial class Form1 : Form
    {

        SerialPort wemosPort;
        bool isPortConnected;

        public Form1()
        {
            InitializeComponent();
            this.load_ports();
        }
         
        private void ConnectButton_Click(object sender, EventArgs e)
        {
            string selectedPort = "";

            // Check first if there exists one port.
            if (comboBox1.Items.Count > 0)
            {
                selectedPort = comboBox1.SelectedItem.ToString();
            }

            // Connect to the selected port if it exists.
            if (!string.IsNullOrEmpty(selectedPort))
            {
                wemosPort = new SerialPort(selectedPort, 9600);


                if (!isPortConnected)
                {
                    wemosPort.Open();
                    wemosPort.DataReceived += new SerialDataReceivedEventHandler(DataReceivedHandler);
                    isPortConnected = true;
                }
            }
        }

        private void DisconnectButton_Click(object sender, EventArgs e)
        {
            if(isPortConnected)
            {
                wemosPort.Close();


                textBox1.Text = "";
                textBox2.Text = "";
                textBox3.Text = "";
                textBox4.Text = "";
                textBox5.Text = "";
                textBox6.Text = "";

                textBox7.Text = "";

            }
        }

        private void SaveButton_Click(object sender, EventArgs e)
        {
      

                if (String.IsNullOrEmpty(textBox1.Text) ||
                    String.IsNullOrEmpty(textBox2.Text) ||
                    String.IsNullOrEmpty(textBox3.Text) ||
                    String.IsNullOrEmpty(textBox4.Text) ||
                    String.IsNullOrEmpty(textBox5.Text) ||
                    String.IsNullOrEmpty(textBox6.Text) ||
                    String.IsNullOrEmpty(textBox7.Text)
                    )
                {
                    MessageBox.Show("Please complete the details above.");
                }
                else
                {
                    if (MessageBox.Show("Are you sure you want to save the current reading?",
                                          "Confirm",
                                          MessageBoxButtons.YesNo,
                                          MessageBoxIcon.Question) == DialogResult.Yes)
                    {
                        System.IO.StreamWriter writer = new System.IO.StreamWriter("records.txt", true);

                        String data = textBox7.Text;
                        data += ",";
                        data += textBox1.Text;
                        data += ",";
                        data += textBox2.Text;
                        data += ",";
                        data += textBox3.Text;
                        data += ",";
                        data += textBox4.Text;
                        data += ",";
                        data += textBox5.Text;
                        data += ",";
                        data += textBox6.Text;



                        writer.Write(data);
                        writer.Close();

                        MessageBox.Show("Data saved!");
                    }
                }
            
        }

        private void load_ports()
        {
            // List all available ports.
            string[] ports = SerialPort.GetPortNames();

            // Add available ports to combobox.
            foreach (string port in ports)
            {
                comboBox1.Items.Add(port);
            }

            // Make combobox non editable and select the first item on the list.
            comboBox1.DropDownStyle = ComboBoxStyle.DropDownList;

            // Check first if there is atleast one item available.
            if (comboBox1.Items.Count > 0)
            {
                comboBox1.SelectedIndex = 0;
            }
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

                string[] data = indata.Split(',');

                if (data.Length == 6)
                {
                    //foreach (String item in data)
                    //{
                    //    MessageBox.Show(item);
                    //}


                    // Start a new thread.

                    if (InvokeRequired)
                    {
                        // after we've done all the processing, 
                        this.Invoke(new MethodInvoker(delegate
                        {
                            // load the control with the appropriate data

                            textBox1.Text = data[0];
                            textBox2.Text = data[1];
                            textBox3.Text = data[2];
                            textBox4.Text = data[3];
                            textBox5.Text = data[4];
                            textBox6.Text = data[5];


                        }));
                        return;
                    }
                }

                
            }
        }
    }
}
