using System;
using System.Windows.Forms;
using System.IO.Ports;

namespace Webert
{
    public partial class LoginForm : Form
    {
        WebertSqlClass mySqlClass = new WebertSqlClass();

        public LoginForm()
        {
            InitializeComponent();
            bool oneExists = false;

            portsCB.DropDownStyle = ComboBoxStyle.DropDownList;

            foreach (string port in SerialPort.GetPortNames())
            {
                oneExists = true;
                portsCB.Items.Add(port);
            }

            if(oneExists)
            {
                portsCB.SelectedIndex = 0;

            }
        }

        private void loginButton_Click(object sender, EventArgs e)
        {
            try
            {
                if (mySqlClass.isUserExist(uNameTB.Text, passTB.Text))
                {
                    try
                    {
                        // Used to connect to the device.
                        new AdminForm(portsCB.SelectedItem.ToString()).Show();

                        // For debugging purposes, fake port passed.
                        //new AdminForm("COM1").Show();

                        mySqlClass.closeDatabase();
                        this.Hide();
                    }
                    catch
                    {
                        MessageBox.Show("Device not connected!", "Error", MessageBoxButtons.OK,
                            MessageBoxIcon.Error);
                    }
                }
                else
                {
                    MessageBox.Show("Invalid username and/or password!", "Error", MessageBoxButtons.OK,
                           MessageBoxIcon.Error);
                }
            }
            catch
            {
                MessageBox.Show("Cannot connect to database!", "Error",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
            }

        }

        private void LoginForm_FormClosing(object sender, FormClosingEventArgs e)
        {
            System.Windows.Forms.Application.Exit();
        }
    }
}
