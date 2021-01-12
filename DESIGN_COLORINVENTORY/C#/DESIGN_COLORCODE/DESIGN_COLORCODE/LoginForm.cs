using System;
using System.Windows.Forms;

namespace DESIGN_COLORCODE
{
    public partial class LoginForm : Form
    {
        private SMAUsers_Model smaUsers;
        private SMAAdmins_Model smaAdmins;

        public LoginForm()
        {
            InitializeComponent();
        }

        private void loginButton_Click(object sender, EventArgs e)
        {
            string username = this.unameTB.Text;
            string password = this.passTB.Text;

            if (!String.IsNullOrWhiteSpace(username) && 
                !String.IsNullOrWhiteSpace(password) && 
                username!="" &&
                password != "")
            {
                // If admin.
                // Has username and password.

                smaAdmins = new SMAAdmins_Model(username, password);

                if (smaAdmins.doesAdminExists())
                {
                    // If admin exists, redirect to admin page.

                    // MessageBox.Show("Admin exists.");
                    ViewForm.isAdmin = true;
                    AdminForm adminForm = new AdminForm();
                    adminForm.Show();
                    this.Hide();
                }
                else
                {
                    MessageBox.Show("Invalid username and/or password.",
                        "Error",
                        MessageBoxButtons.OK,
                        MessageBoxIcon.Error);
                }

            }
            else if (!String.IsNullOrWhiteSpace(username) &&
                username != "")
            {
                // If user.
                // Has username only.

                smaUsers = new SMAUsers_Model(username);

                if(smaUsers.doesUserExists())
                {
                    // If user exists, redirect to user page.

                    //MessageBox.Show("User exists.");
                    ViewForm.isAdmin = false;
                    ViewForm viewForm = new ViewForm();
                    viewForm.Show();
                    this.Hide();

                }
                else
                {
                    MessageBox.Show("Invalid username and/or password.",
                        "Error",
                        MessageBoxButtons.OK,
                        MessageBoxIcon.Error);
                }

            }
            else
            {
                MessageBox.Show("Invalid username and/or password!",
                    "Error",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error);
            }
        }

        private void LoginForm_FormClosing(object sender, FormClosingEventArgs e)
        {
            Application.Exit();
        }

        private void LoginForm_Load(object sender, EventArgs e)
        {

        }

        private void groupBox1_Enter(object sender, EventArgs e)
        {

        }
    }
}
