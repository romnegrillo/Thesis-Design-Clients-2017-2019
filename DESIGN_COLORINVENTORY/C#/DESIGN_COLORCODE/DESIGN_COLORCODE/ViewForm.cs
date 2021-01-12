using ClosedXML.Excel;
using System;
using System.Data;
using System.Windows.Forms;

namespace DESIGN_COLORCODE
{
    public partial class ViewForm : Form
    {
        SMAInventory_Model smaInventory = new SMAInventory_Model();
        public static bool isAdmin = false;

        public ViewForm()
        {
            InitializeComponent();
            showDatabase();
            dataGridView1.ReadOnly = true;
            dataGridView1.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill;
            dataGridView1.AllowUserToAddRows = false;
        }

        private void showDatabase()
        {
            dataGridView1.DataSource = smaInventory.getDatabase();
        }

        private void backButton_Click(object sender, EventArgs e)
        {
            if (isAdmin)
            {
                AdminForm adminForm = new AdminForm();
                adminForm.Show();
                this.Hide();
            }
            else
            {
                LoginForm loginForm = new LoginForm();
                loginForm.Show();
                this.Hide();
            }
        }

        private void viewButton_Click(object sender, EventArgs e)
        {
            if (dataGridView1.SelectedRows.Count > 0)
            {
                foreach (DataGridViewRow row in dataGridView1.SelectedRows)
                {
                    string name = row.Cells[0].Value.ToString();
                    string materialNumber = row.Cells[1].Value.ToString();

                    if (!String.IsNullOrEmpty(name) && name != "" &&
                  !String.IsNullOrEmpty(materialNumber) && materialNumber != "")
                    {


                        string[] data = smaInventory.getDataWithNameAndMaterialNumber(name, materialNumber);

                        //foreach (string item in data)
                        //{
                        //    MessageBox.Show(item.ToString());
                        //}

                        ViewFormDialog viewFormDialog = new ViewFormDialog(data);
                        viewFormDialog.ShowDialog();

                    }

                }
            }
            else
            {
                MessageBox.Show("Select row to view.",
                    "Error",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error);
            }
        }

        private void exportButton_Click(object sender, EventArgs e)
        {
            SaveFileDialog sfd = new SaveFileDialog();
            sfd.Filter = "Excel Documents (*.xlsx)|*.xlsx";
            sfd.FileName = "ToExport.xlsx";

            if (sfd.ShowDialog() == DialogResult.OK)
            {
                //MessageBox.Show(sfd.FileName.ToString());

                XLWorkbook wb = new XLWorkbook();

                DataTable dt = smaInventory.getDataForExcel();

                wb.Worksheets.Add(dt);

                wb.SaveAs(sfd.FileName.ToString());

            }
        }

        private void ViewForm_FormClosing(object sender, FormClosingEventArgs e)
        {
            Application.Exit();
        }

        private void ViewForm_Load(object sender, EventArgs e)
        {

        }
    }
}
