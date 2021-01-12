using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace DESIGN_COLORCODE
{
    public partial class ViewFormDialog : Form
    {
        public ViewFormDialog()
        {
            InitializeComponent();
        }

        public ViewFormDialog(params string[] data)
        {
            InitializeComponent();

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

        }

        private void backButton_Click(object sender, EventArgs e)
        {
            this.Close();
        }
    }
}
