using System;
using System.Windows.Forms;

namespace DESIGN_COLORCODE
{
    public partial class AdminForm : Form
    {
        public AdminForm()
        {
            InitializeComponent();
        }

        private void logoutButton_Click(object sender, EventArgs e)
        {
            LoginForm loginForm = new LoginForm();
            loginForm.Show();
            this.Hide();
        }

        private void addUserButton_Click(object sender, EventArgs e)
        {
            AddUserForm addUserForm = new AddUserForm();
            addUserForm.Show();
            this.Hide();
        }

        private void addScanButton_Click(object sender, EventArgs e)
        {
            ScanForm scanForm = new ScanForm();
            scanForm.Show();
            this.Hide();
        }

        private void viewInventoryButton_Click(object sender, EventArgs e)
        {
            ViewForm viewWindow = new ViewForm();
            viewWindow.Show();
            this.Hide();
        }

        private void editInventoryButton_Click(object sender, EventArgs e)
        {
            EditForm editform = new EditForm();
            editform.Show();
            this.Hide();
        }

        private void changePasswordButton_Click(object sender, EventArgs e)
        {
            ChangePasswordForm changePasswordForm = new ChangePasswordForm();
            changePasswordForm.Show();
            this.Hide();
        }

        private void addItemButton_Click(object sender, EventArgs e)
        {
            AddItemForm addItemForm = new AddItemForm();
            addItemForm.Show();
            this.Hide();
        }

        private void AdminForm_FormClosing(object sender, FormClosingEventArgs e)
        {
            Application.Exit();
        }
    }
}
