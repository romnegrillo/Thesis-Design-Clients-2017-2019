using System;
using System.Windows.Forms;

namespace DESIGN_COLORCODE
{
    public partial class ChangePasswordForm : Form
    {

        SMAAdmins_Model smaAdmin = new SMAAdmins_Model(0);

        public ChangePasswordForm()
        {
            InitializeComponent();
        }

        private void backButton_Click(object sender, EventArgs e)
        {
            AdminForm adminForm = new AdminForm();
            adminForm.Show();
            this.Hide();
        }

        private void confirmButton_Click(object sender, EventArgs e)
        {
            string currentPass = currentPassTB.Text;
            string newPass = newPassTB.Text;
            string confirmPass = confirmPassTB.Text;

            if(!String.IsNullOrWhiteSpace(currentPass) &&
                !String.IsNullOrWhiteSpace(newPass) && 
                !String.IsNullOrWhiteSpace(confirmPass) && 
                currentPass!="" && 
                newPass!="" &&
                confirmPass!="")
            {   
                if(newPass!=confirmPass)
                {
                    MessageBox.Show("New password and confirm password are not the same.",
                    "Error",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Warning);

                    smaAdmin.propNumTries++;
                    numTriesLabel.Text = smaAdmin.propNumTries.ToString();

                    return;
                }

                if(smaAdmin.changeAdminPassword(SMAAdmins_Model.adminUser, currentPass,newPass))
                {
                    MessageBox.Show("Password succeessfully changed.",
                        "Success",
                        MessageBoxButtons.OK,
                        MessageBoxIcon.Information);
                }
                else
                {
                    MessageBox.Show("Wrong current password.",
                    "Error",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error);

                    smaAdmin.propNumTries++;
                    numTriesLabel.Text = smaAdmin.propNumTries.ToString();
                }
            }
            else
            {
                MessageBox.Show("All fields are required.",
                "Warning",
                MessageBoxButtons.OK,
                MessageBoxIcon.Warning);
            }

            if (smaAdmin.propNumTries==SMAAdmins_Model.maxNumTries)
            {
                MessageBox.Show("You have reached the number maximum of attempts.\n" +
                    "Logging out...",
                "Error",
                MessageBoxButtons.OK,
                MessageBoxIcon.Error);

                LoginForm loginForm = new LoginForm();
                loginForm.Show();
                this.Close();
            }
        }

        private void ChangePasswordForm_FormClosing(object sender, FormClosingEventArgs e)
        {
            Application.Exit();
        }
    }
}
