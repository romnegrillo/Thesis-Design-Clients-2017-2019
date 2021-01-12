using System;
using System.Windows.Forms;

namespace DESIGN_COLORCODE
{
    public partial class AddUserForm : Form
    {
        SMAAdmins_Model smaAdmins;

        public AddUserForm()
        {
            InitializeComponent();
        }

        private void backButton_Click(object sender, EventArgs e)
        {
            AdminForm adminForm = new AdminForm();
            adminForm.Show();
            this.Hide();
        }

        private void addButton_Click(object sender, EventArgs e)
        {
            string username = usernameTB.Text;

            if (!String.IsNullOrWhiteSpace(username) &&
                username != "")
            {
                smaAdmins = new SMAAdmins_Model();

                if(smaAdmins.registerUser(username))
                {
                    // User successfully added.

                    MessageBox.Show("User added.",
                        "Success",
                        MessageBoxButtons.OK,
                        MessageBoxIcon.Information);
                }
                else
                {
                    MessageBox.Show("User already exists.",
                    "Success",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error);
                }
            }
        }

        private void AddUserForm_FormClosing(object sender, FormClosingEventArgs e)
        {
            Application.Exit();
        }
    }
}
