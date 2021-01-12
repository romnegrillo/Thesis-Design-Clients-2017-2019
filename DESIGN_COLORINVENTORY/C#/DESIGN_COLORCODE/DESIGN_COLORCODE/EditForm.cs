using System;
using System.Globalization;
using System.Windows.Forms;

namespace DESIGN_COLORCODE
{
    public partial class EditForm : Form
    {
        SMAInventory_Model smaInventory = new SMAInventory_Model();

        public EditForm()
        {
            InitializeComponent();
            dataGridView1.ReadOnly = true;
            dataGridView1.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill;
            dataGridView1.SelectionMode = DataGridViewSelectionMode.FullRowSelect;

            this.showDatabase();

        }

        public EditForm(string colorCode)
        {
            InitializeComponent();
            dataGridView1.ReadOnly = true;
            dataGridView1.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill;
            dataGridView1.SelectionMode = DataGridViewSelectionMode.FullRowSelect;

            this.showDatabase();
            this.scannedItemExists(colorCode);
        }

        private void scannedItemExists(string colorCode)
        {
            string[] data=smaInventory.getDataWithColorCode(colorCode);

            //foreach(string item in items)
            //{
            //    MessageBox.Show(item);
            //}

            colorCodeTB.Text = data[0];
            nameTB.Text = data[1];
            materialNoTB.Text = data[2];
            descriptionTB.Text = data[3];
            unitPriceTB.Text = data[4];
            invoiceTB.Text = data[5];
            stockBalanceTB.Text = data[6];
            actualCountTB.Text = data[7];
            recountTB.Text = data[8];
            finalCountsTB.Text = data[9];
            disrepancyTB.Text = data[10];
            disrepancyAmtTB.Text = data[11];
            remarksTB.Text = data[12];

        
      
            datePickerAdded.Value = DateTime.Parse(data[13]);
            datePickerReleased.Value = DateTime.Parse(data[14]);

            // Auto select row that has that data.

            int ctr = 0;

            foreach (DataGridViewRow row in dataGridView1.Rows)
            {
                //MessageBox.Show(((row.Cells[1].Value.ToString())==materialNoTB.Text).ToString());

                //MessageBox.Show(row.Cells[1].Value.ToString());

                if (row.Cells[1].Value.ToString().Contains(materialNoTB.Text))
                {
                    //MessageBox.Show("Debug");
                    //dataGridView1.ClearSelection();
                    //row.Selected = true;
                    //dataGridView1.Rows[1].Selected = true;
                    dataGridView1.CurrentCell = dataGridView1[1, ctr];
                    break;
                }

                ctr++;
               
            }

 
        }

        private void showDatabase()
        {
            dataGridView1.DataSource = smaInventory.getDatabase();
            dataGridView1.AllowUserToAddRows = false;
        }


        private void backButton_Click(object sender, EventArgs e)
        {
            AdminForm adminForm = new AdminForm();
            adminForm.Show();
            this.Hide();
        }

        private void dataGridView1_SelectionChanged(object sender, EventArgs e)
        {
            foreach(DataGridViewRow row in dataGridView1.SelectedRows)
            {
                // If the first required column is not empty, there is a data.
                // We will query the database with the name and material number then
                // display it to the textboxes.

                
                string name = row.Cells[0].Value.ToString();
                string materialNumber = row.Cells[1].Value.ToString();

                if (!String.IsNullOrEmpty(name) && name!="" &&
                    !String.IsNullOrEmpty(materialNumber) && materialNumber!="")
                {
                     
                    SMAInventory_Model smaInventory = new SMAInventory_Model();
                    string[] data = smaInventory.getDataWithNameAndMaterialNumber(name, materialNumber);

                    SMAInventory_Model.propMaterialNumber = Convert.ToInt32(materialNumber);

                    colorCodeTB.Text = data[0];
                    nameTB.Text = data[1];
                    materialNoTB.Text = data[2];
                    descriptionTB.Text = data[3];
                    unitPriceTB.Text = data[4];
                    invoiceTB.Text = data[5];
                    stockBalanceTB.Text = data[6];
                    actualCountTB.Text = data[7];
                    recountTB.Text = data[8];
                    finalCountsTB.Text = data[9];
                    disrepancyTB.Text = data[10];
                    disrepancyAmtTB.Text = data[11];
                    remarksTB.Text = data[12];
                   // MessageBox.Show(data[13].ToString());
                    datePickerAdded.Value = DateTime.Parse(data[13]);
                    datePickerReleased.Value = DateTime.Parse(data[14]);
                }
            }
        }

        private void editButton_Click(object sender, EventArgs e)
        {
            if (!(dataGridView1.SelectedRows.Count > 0))
            {
                MessageBox.Show("Select row to edit.",
                    "Error",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error);

                return;

            }
                int textBoxNum = 0;
            int numValidInputs = 3;

            string name = null;
            Nullable<int> materialNum;
            string description = null;
            string colorcode = null;
            Nullable<decimal> unitPrice = null;
            Nullable<int> invoice = null;
            Nullable<int> stockBalance = null;
            Nullable<int> actualCount = null;
            Nullable<int> recount = null;
            Nullable<int> finalCounts = null;
            Nullable<int> disrepancy = null;
            Nullable<decimal> disrepancyAmt = null;
            string remarks = null;

            try
            {


                // Required fields are name, materialNumber, description.
                // ===========================================================

                // Check first if all required fields are not empty.

                if (!(!String.IsNullOrWhiteSpace(nameTB.Text) &&
                    !String.IsNullOrWhiteSpace(materialNoTB.Text) &&
                    !String.IsNullOrWhiteSpace(descriptionTB.Text) &&
                    nameTB.Text != "" &&
                    materialNoTB.Text != "" &&
                    descriptionTB.Text != ""))
                {
                    MessageBox.Show("Fields with asterisk are required.",
                        "Error",
                        MessageBoxButtons.OK,
                        MessageBoxIcon.Error);

                    return;
                }

                name = nameTB.Text;

                try { materialNum = Convert.ToInt32(materialNoTB.Text); }
                catch { textBoxNum = 3; throw new System.FormatException(); }

                description = descriptionTB.Text;


                // ===========================================================

                // Only check other parts if it not empty and not whitespace.
                // Then throw necessary exceptions when the input is invalid.

                if (!String.IsNullOrWhiteSpace(colorCodeTB.Text) && colorCodeTB.Text != "")
                {
                    try { colorcode = colorCodeTB.Text; numValidInputs++; }
                    catch { textBoxNum = 1; throw new System.FormatException(); }
                }

                if (!String.IsNullOrWhiteSpace(unitPriceTB.Text) && unitPriceTB.Text != "")
                {
                    try { unitPrice = Convert.ToDecimal(unitPriceTB.Text); numValidInputs++; }
                    catch { textBoxNum = 5; throw new System.FormatException(); }
                }

                if (!String.IsNullOrWhiteSpace(invoiceTB.Text) && invoiceTB.Text != "")
                {
                    try { invoice = Convert.ToInt32(invoiceTB.Text); numValidInputs++; }
                    catch { textBoxNum = 6; throw new System.FormatException(); }
                }

                if (!String.IsNullOrWhiteSpace(stockBalanceTB.Text) && stockBalanceTB.Text != "")
                {
                    try { stockBalance = Convert.ToInt32(stockBalanceTB.Text); numValidInputs++; }
                    catch { textBoxNum = 7; throw new System.FormatException(); }
                }

                if (!String.IsNullOrWhiteSpace(actualCountTB.Text) && actualCountTB.Text != "")
                {
                    try { actualCount = Convert.ToInt32(actualCountTB.Text); numValidInputs++; }
                    catch { textBoxNum = 8; throw new System.FormatException(); }
                }

                if (!String.IsNullOrWhiteSpace(recountTB.Text) && recountTB.Text != "")
                {
                    try { recount = Convert.ToInt32(recountTB.Text); numValidInputs++; }
                    catch { textBoxNum = 9; throw new System.FormatException(); }
                }

                if (!String.IsNullOrWhiteSpace(finalCountsTB.Text) && finalCountsTB.Text != "")
                {
                    try { finalCounts = Convert.ToInt32(finalCountsTB.Text); numValidInputs++; }
                    catch { textBoxNum = 10; throw new System.FormatException(); }
                }

                if (!String.IsNullOrWhiteSpace(disrepancyTB.Text) && disrepancyTB.Text != "")
                {
                    try { disrepancy = Convert.ToInt32(disrepancyTB.Text); numValidInputs++; }
                    catch { textBoxNum = 11; throw new System.FormatException(); }
                }

                if (!String.IsNullOrWhiteSpace(disrepancyAmtTB.Text) && disrepancyAmtTB.Text != "")
                {
                    try { disrepancyAmt = Convert.ToDecimal(disrepancyAmtTB.Text); numValidInputs++; }
                    catch { textBoxNum = 12; throw new System.FormatException(); }
                }

                remarks = remarksTB.Text;
            }
            catch (System.FormatException)
            {
                if (textBoxNum == 1)
                {
                    MessageBox.Show("Color Code should be a number.",
                        "Error",
                        MessageBoxButtons.OK,
                        MessageBoxIcon.Error);
                }
                else if (textBoxNum == 3)
                {
                    MessageBox.Show("Material Number should be a number.",
                        "Error",
                        MessageBoxButtons.OK,
                        MessageBoxIcon.Error);
                }
                else if (textBoxNum == 5)
                {
                    MessageBox.Show("Unit Price should be a number.",
                        "Error",
                        MessageBoxButtons.OK,
                        MessageBoxIcon.Error);
                }
                else if (textBoxNum == 6)
                {
                    MessageBox.Show("Invoice should be a number.",
                        "Error",
                        MessageBoxButtons.OK,
                        MessageBoxIcon.Error);
                }
                else if (textBoxNum == 7)
                {
                    MessageBox.Show("Stock Balance should be a number.",
                        "Error",
                        MessageBoxButtons.OK,
                        MessageBoxIcon.Error);
                }
                else if (textBoxNum == 8)
                {
                    MessageBox.Show("Actual Count should be a number.",
                        "Error",
                        MessageBoxButtons.OK,
                        MessageBoxIcon.Error);
                }
                else if (textBoxNum == 9)
                {
                    MessageBox.Show("Recount should be a number.",
                        "Error",
                        MessageBoxButtons.OK,
                        MessageBoxIcon.Error);
                }
                else if (textBoxNum == 10)
                {
                    MessageBox.Show("Final Counts should be a number.",
                        "Error",
                        MessageBoxButtons.OK,
                        MessageBoxIcon.Error);
                }
                else if (textBoxNum == 11)
                {
                    MessageBox.Show("Disrepancy should be a number.",
                        "Error",
                        MessageBoxButtons.OK,
                        MessageBoxIcon.Error);
                }
                else if (textBoxNum == 12)
                {
                    MessageBox.Show("Disrepanct Amount should be a number.",
                        "Error",
                        MessageBoxButtons.OK,
                        MessageBoxIcon.Error);
                }

                return;
            }



            if (numValidInputs != 0)
            {
                //MessageBox.Show("All inputs are valid. Num inputs: " + numValidInputs.ToString());

                // If only the required fields have mark.
                if (numValidInputs == 3)
                {

                    DialogResult message = MessageBox.Show("Are you sure you want to update changes?",
                        "Confirm Edit",
                        MessageBoxButtons.YesNo,
                        MessageBoxIcon.Question);

                    if (message == DialogResult.Yes)
                    {
                        // Call constructor with only only the required fields.
                        SMAInventory_Model smaInventory =
                            new SMAInventory_Model(
                                colorcode,
                                name,
                                materialNum,
                                description,
                                datePickerAdded.Value.ToString(),
                        datePickerReleased.Value.ToString());

                        if (smaInventory.editItems())
                        {
                            MessageBox.Show("Items successfully added.",
                                "Success",
                                MessageBoxButtons.OK,
                                MessageBoxIcon.Information);
                        }
                        else
                        {
                            MessageBox.Show("Material number already exists.",
                                "Error",
                                MessageBoxButtons.OK,
                                MessageBoxIcon.Error);
                        }
                    }

                }
                // If one or more optional fields have mark.
                else
                {

                    DialogResult message = MessageBox.Show("Are you sure you want to update changes?",
                            "Confirm Edit",
                            MessageBoxButtons.YesNo,
                            MessageBoxIcon.Question);

                    if (message == DialogResult.Yes)
                    {
                        // Call constructor with required and optional fields.
                        // Fields with no value are automatically empty string.
                        SMAInventory_Model smaInventory =
                    new SMAInventory_Model(
                        colorcode,
                        name,
                        materialNum,
                        description,
                        unitPrice,
                        invoice,
                        stockBalance,
                        actualCount,
                        recount,
                        finalCounts,
                        disrepancy,
                        disrepancyAmt,
                        remarks,
                        datePickerAdded.Value.ToString(),
                        datePickerReleased.Value.ToString()); 

                        if (smaInventory.editItems())
                        {
                            MessageBox.Show("Items successfully edited.",
                                "Success",
                                MessageBoxButtons.OK,
                                MessageBoxIcon.Information);
                        }
                        else
                        {
                            MessageBox.Show("Material number already exists.",
                                "Error",
                                MessageBoxButtons.OK,
                                MessageBoxIcon.Error);
                        }
                    }
                }
            }

            this.showDatabase();

            return;
        }

        private void deleteButton_Click(object sender, EventArgs e)
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

                        DialogResult message = MessageBox.Show("Are you sure you want to delete the selected item?",
                            "Confirm Edit",
                            MessageBoxButtons.YesNo,
                            MessageBoxIcon.Question);

                        if (message == DialogResult.Yes)
                        {
                            SMAInventory_Model.propMaterialNumber = Convert.ToInt32(materialNumber);

                            if (smaInventory.deleteItem())
                            {
                                MessageBox.Show("Items successfully deleted.",
                                    "Success",
                                    MessageBoxButtons.OK,
                                    MessageBoxIcon.Information);

                                this.showDatabase();

                                return;
                            }
                            else
                            {
                                MessageBox.Show("Selected item cannot be deleted.",
                                    "Error",
                                    MessageBoxButtons.OK,
                                    MessageBoxIcon.Error);

                                return;
                            }
                        }
                    }
                }
            }
            else
            {

                MessageBox.Show("Select row to delete.",
                    "Error",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error);
            }

        }

        private void EditForm_FormClosing(object sender, FormClosingEventArgs e)
        {
            Application.Exit();
        }

        private void dataGridView1_CurrentCellChanged(object sender, EventArgs e)
        {
            
        }
    }
}
