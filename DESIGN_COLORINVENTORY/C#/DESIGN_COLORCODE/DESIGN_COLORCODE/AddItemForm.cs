using System;
using System.Windows.Forms;

namespace DESIGN_COLORCODE
{
    public partial class AddItemForm : Form
    {
        public AddItemForm()
        {
            InitializeComponent();
        }



        // Window opened when there is a color code in the scan form.
        public AddItemForm(string colorCode)
        {
            InitializeComponent();
            colorCodeTB.Text = colorCode;
        }

        private void addButton_Click(object sender, EventArgs e)
        {
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
                    try {  colorcode =colorCodeTB.Text; numValidInputs++; }
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

            string date_added = datePickerAdded.Value.ToString();
            string date_released = datePickerReleased.Value.ToString();

            if (numValidInputs != 0)
            {
                 //MessageBox.Show("All inputs are valid. Num inputs: " + numValidInputs.ToString());

                // If only the required fields have mark.
                if (numValidInputs == 3)
                {
                    // Call constructor with only only the required fields.
                    SMAInventory_Model smaInventory =
                        new SMAInventory_Model(
                            colorcode,
                            name,
                            materialNum,
                            description,
                            date_added,
                            date_released);

                    if(smaInventory.addItemsRequired())
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
                // If one or more optional fields have mark.
                else
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
                        date_added,
                        date_released);

                    if (smaInventory.addItemsRequiredAndOptional())
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

            return;
        }


        private void backButton_Click(object sender, EventArgs e)
        {
            AdminForm adminForm = new AdminForm();
            adminForm.Show();
            this.Hide();
        }

        private void AddItemForm_FormClosing(object sender, FormClosingEventArgs e)
        {
            Application.Exit();
        }
    }
}
