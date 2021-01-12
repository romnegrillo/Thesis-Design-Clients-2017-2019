using System;
using System.Data;
using System.Data.SQLite;
using System.Windows.Forms;

namespace DESIGN_COLORCODE
{
    class SMAInventory_Model
    {
        // Required fields:
        // id, materialNumber, description

        // Optional fields:
        // unitPrice,  invoice, stockBalance, 
        // actualCount, recount, finalCounts,
        // disrepancy, disrepancyAmount, remarks;C:\Users\Abram Magadia\Desktop\DESIGN_COLORINVENTORY-master\C#\DESIGN_COLORCODE\DESIGN_COLORCODE\SMAInventory_Model.cs

        private Nullable<int> id;
        private string colorCode = null;
        private string name;
        private Nullable<int> materialNumber;
        private string description;

        private Nullable<decimal> unitPrice;
        private Nullable<int> invoice, stockBalance, actualCount, recount, finalCount,
            disrepancy;
        private Nullable<decimal> disrepancyAmount;
        private string remarks, date_added, date_released;

        // For database.
        private const string dbName = "SMADatabase.db";
        private const string inventoryTableName = "SMAInventory";

        SQLiteConnection dbConnection;
        SQLiteCommand dbCommand;
        SQLiteDataReader dbReader;

        // Constructor for accessing inventory checking methods.
        public SMAInventory_Model() { }

        // Constructor for required fields.
        public SMAInventory_Model(string colorCode, string name, Nullable<int> materialNumber, string description, string date_added, string date_released)
        {
            this.colorCode = colorCode;
            this.name = name;
            this.materialNumber = materialNumber;
            this.description = description;
            this.date_added = date_added;
            this.date_released = date_released;

            //MessageBox.Show("Debug: " + this.name);
        }


        // Constructor for required fields and optional values.
        public SMAInventory_Model(string colorCode, string name, Nullable<int> materialNumber, string description,
           Nullable<decimal> unitPrice,
            Nullable<int> invoice,
             Nullable<int> stockBalance,
              Nullable<int> actualCount,
               Nullable<int> recount,
                Nullable<int> finalCounts,
                 Nullable<int> disrepancy,
                  Nullable<decimal> disrepancyAmount,
                  string remarks,
                  string date_added,
                  string date_released)
        {
            this.colorCode = colorCode;
            this.name = name;
            this.materialNumber = materialNumber;
            this.description = description;
            this.unitPrice = unitPrice;
            this.invoice = invoice;
            this.stockBalance = stockBalance;
            this.actualCount = actualCount;
            this.recount = recount;
            this.finalCount = finalCounts;
            this.disrepancy = disrepancy;
            this.disrepancyAmount = disrepancyAmount;
            this.remarks = remarks;
            this.date_added = date_added;
            this.date_released = date_released;

            //MessageBox.Show("Debug: " + this.recount.ToString());
        }

        private bool connectToDB()
        {
            dbConnection = new SQLiteConnection(string.Format("Data Source={0};Version=3;", dbName));

            try
            {
                dbConnection.Open();
                return true;
            }
            catch
            {
                return false;
            }
        }

        public DataTable getDatabase()
        {
            if (this.connectToDB())
            {
                // Return whole data in the database without the ID.
                string query = String.Format("SELECT name, materialNumber FROM {0};", inventoryTableName);

                dbCommand = new SQLiteCommand(query, dbConnection);
                SQLiteDataReader dbReader = dbCommand.ExecuteReader();
                DataTable dbTable = new DataTable();
                dbTable.Load(dbReader);

                return dbTable;
            }

            return null;
        }

        public DataTable getDataForExcel()
        {
            if (this.connectToDB())
            {
                // Return whole data in the database without the ID.
                string query = String.Format("SELECT colorCode, " +
                    "name," +
                    "materialNumber," +
                    "description," +
                    "unitPrice," +
                    "invoice," +
                    "stockBalance," +
                    "actualCount," +
                    "recount," +
                    "finalCount," +
                    "disrepancy," +
                    "disrepancyAmount," +
                    "remarks, date_added, date_released FROM {0};", inventoryTableName);

                dbCommand = new SQLiteCommand(query, dbConnection);
                SQLiteDataReader dbReader = dbCommand.ExecuteReader();
                DataTable dbTable = new DataTable();
                dbTable.Load(dbReader);

                return dbTable;
            }

            return null;
        }

        public bool addItemsRequired()
        {
            if (this.connectToDB())
            {
                string query = String.Format("INSERT INTO {0}(colorCode, name, materialNumber, description, date_added, date_released)" +
                    " VALUES(@colorCode, @name, @materialNumber, @description, @date_added, @date_released);", inventoryTableName);


                dbCommand = new SQLiteCommand(query, dbConnection);
                dbCommand.Parameters.AddWithValue("@colorCode", this.colorCode);
                dbCommand.Parameters.AddWithValue("@name", this.name);
                dbCommand.Parameters.AddWithValue("@materialNumber", this.materialNumber);
                dbCommand.Parameters.AddWithValue("@description", this.description);
                dbCommand.Parameters.AddWithValue("@date_added", this.date_added);
                dbCommand.Parameters.AddWithValue("@date_released", this.date_released);

                try
                {
                    if (dbCommand.ExecuteNonQuery() != 0)
                    {
                        //this.removeNull();
                        return true;
                    }
                }
                catch(System.Data.SQLite.SQLiteException e)
                {
                    MessageBox.Show(e.ToString());
                    return false;
                }
            }

            return false;
        }

        public bool addItemsRequiredAndOptional()
        {
            if (this.connectToDB())
            {
                string query = String.Format("INSERT INTO {0}(colorCode, name, materialNumber, description," +
                "unitPrice, invoice, stockBalance, actualCount, recount, finalCount, " +
                "disrepancy, disrepancyAmount, remarks, date_added, date_released)" +
                " VALUES(@colorCode, @name, @materialNumber, @description," +
                "@unitPrice, @invoice, @stockBalance, @actualCount, @recount, @finalCount," +
                "@disrepancy, @disrepancyAmount, @remarks, @date_added, @date_released);", inventoryTableName);

                dbCommand = new SQLiteCommand(query, dbConnection);
                dbCommand.Parameters.AddWithValue("@colorCode", this.colorCode);
                dbCommand.Parameters.AddWithValue("@name", this.name);
                dbCommand.Parameters.AddWithValue("@materialNumber", this.materialNumber);
                dbCommand.Parameters.AddWithValue("@description", this.description);
                dbCommand.Parameters.AddWithValue("@unitPrice", this.unitPrice);
                dbCommand.Parameters.AddWithValue("@invoice", this.invoice);
                dbCommand.Parameters.AddWithValue("@stockBalance", this.stockBalance);
                dbCommand.Parameters.AddWithValue("@actualCount", this.actualCount);
                dbCommand.Parameters.AddWithValue("@recount", this.recount);
                dbCommand.Parameters.AddWithValue("@finalCount", this.finalCount);
                dbCommand.Parameters.AddWithValue("@disrepancy", this.disrepancy);
                dbCommand.Parameters.AddWithValue("@disrepancyAmount", this.disrepancyAmount);
                dbCommand.Parameters.AddWithValue("@remarks", this.remarks);
                dbCommand.Parameters.AddWithValue("@date_added", this.date_added);
                dbCommand.Parameters.AddWithValue("@date_released", this.date_released);

                try
                {
                    if (dbCommand.ExecuteNonQuery() != 0)
                    {
                        //this.removeNull();
                        return true;
                    }
                }
                catch (System.Data.SQLite.SQLiteException e)
                {
                    MessageBox.Show(e.ToString());
                    return false;
                }

            }

            return false;
        }

        public bool editItems()
        {
            if (this.connectToDB())
            {
                int id = 0;

                string getIDQuery = String.Format("SELECT id FROM {0} WHERE materialNumber=@materialNumber;", inventoryTableName);
                dbCommand = new SQLiteCommand(getIDQuery, dbConnection);
                dbCommand.Parameters.AddWithValue("@id", id);
                dbCommand.Parameters.AddWithValue("@materialNumber", SMAInventory_Model.propMaterialNumber);
                dbReader = dbCommand.ExecuteReader();
               

                if(dbReader.HasRows)
                {
                    dbReader.Read();

                    id = Convert.ToInt32(dbReader.GetInt32(0));
                    //MessageBox.Show(id.ToString());
                }

                dbReader.Close();

                string query = String.Format("UPDATE {0} SET " +
                    "colorCode=@colorCode, " +
                    "name=@name, " +
                    "materialNumber=@materialNumber, " +
                    "description=@description, " +
                    "unitPrice=@unitPrice, " +
                    "invoice=@invoice, " +
                    "stockBalance=@stockBalance, " +
                    "actualCount=@actualCount, " +
                    "recount=@recount, " +
                    "finalCount=@finalCount, " +
                    "disrepancy=@disrepancy, " +
                    "disrepancyAmount=@disrepancyAmount, " +
                    "remarks=@remarks, " +
                    "date_added=@date_added, " +
                    "date_released=@date_released " +
                    "WHERE id=@id;", inventoryTableName);

                dbCommand = new SQLiteCommand(query, dbConnection);
                dbCommand.Parameters.AddWithValue("@colorCode", this.colorCode);
                dbCommand.Parameters.AddWithValue("@name", this.name);
                dbCommand.Parameters.AddWithValue("@materialNumber", this.materialNumber);
                dbCommand.Parameters.AddWithValue("@description", this.description);
                dbCommand.Parameters.AddWithValue("@unitPrice", this.unitPrice);
                dbCommand.Parameters.AddWithValue("@invoice", this.invoice);
                dbCommand.Parameters.AddWithValue("@stockBalance", this.stockBalance);
                dbCommand.Parameters.AddWithValue("@actualCount", this.actualCount);
                dbCommand.Parameters.AddWithValue("@recount", this.recount);
                dbCommand.Parameters.AddWithValue("@finalCount", this.finalCount);
                dbCommand.Parameters.AddWithValue("@disrepancy", this.disrepancy);
                dbCommand.Parameters.AddWithValue("@disrepancyAmount", this.disrepancyAmount);
                dbCommand.Parameters.AddWithValue("@remarks", this.remarks);
                dbCommand.Parameters.AddWithValue("@date_added", this.date_added);
                dbCommand.Parameters.AddWithValue("@date_released", this.date_released);
                dbCommand.Parameters.AddWithValue("@id", id);


                try
                {
                    if (dbCommand.ExecuteNonQuery() != 0)
                    {
                        //this.removeNull();
                        return true;
                    }
                }
                catch (System.Data.SQLite.SQLiteException e)
                {
                    MessageBox.Show(e.ToString());
                    return false;
                }

            }

            return false;
        }

        public bool deleteItem()
        {
            if (this.connectToDB())
            {
                string query = String.Format("DELETE FROM {0} WHERE materialNumber=@materialNumber;", inventoryTableName);

                dbCommand = new SQLiteCommand(query, dbConnection);
                dbCommand.Parameters.AddWithValue("@materialNumber", SMAInventory_Model.propMaterialNumber);


                //MessageBox.Show(SMAInventory_Model.propMaterialNumber.ToString());

                try
                {
                    if (dbCommand.ExecuteNonQuery() != 0)
                    {
                        //this.removeNull();
                        return true;
                    }
                }
                catch (System.Data.SQLite.SQLiteException)
                {
                    return false;
                }

            }

            return false;
        }

        public static string convertColorNameToStringNum(string colorCodeName)
        {
            // Ex: red, red, red, green, blue
            colorCodeName = colorCodeName.Substring(0, colorCodeName.Length - 1);
            string[] colorNames = colorCodeName.Split(',');

            // Ex: 11123
            string colorStringNum = "";



            if (colorNames.Length == 5)
            {
                for (int i = 0; i < colorNames.Length; i++)
                {
                    if (colorNames[i] == "black")
                    {
                        colorStringNum += "0";
                    }
                    else if (colorNames[i] == "white")
                    {
                        colorStringNum += "1";
                    }
                    else if (colorNames[i] == "red")
                    {
                        colorStringNum += "2";
                    }
                    else if (colorNames[i] == "orange")
                    {
                        colorStringNum += "3";
                    }
                    else if (colorNames[i] == "blue")
                    {
                        colorStringNum += "4";
                    }
                    else if (colorNames[i] == "purple")
                    {
                        colorStringNum += "5";
                    }
                    else if (colorNames[i] == "green")
                    {
                        colorStringNum += "6";
                    }
                    else if (colorNames[i] == "lime")
                    {
                        colorStringNum += "7";
                    }
                    else if (colorNames[i] == "gray")
                    {
                        colorStringNum += "8";
                    }
                    else if (colorNames[i] == "darkgray")
                    {
                        colorStringNum += "9";
                    }
                    else
                    {
                        colorStringNum += "0";
                    }
                }

                //MessageBox.Show(colorStringNum);
                return colorStringNum;
            }

            return "";
        }

        public string convertStringNumToColorName(string colorNames)
        {
            // Remove \r
            colorNames = colorNames.Substring(0, colorNames.Length - 1);

            string[] colorNameSub = colorNames.Split(',');
            string colorCode = "";

            //MessageBox.Show(colorNameSub[3].Length.ToString());
            

            if (colorNameSub.Length == 5)
            {
                for (int i = 0; i < colorNameSub.Length; i++)
                {
                    if (colorNameSub[i] == "black")
                    {
                        colorCode += "0";
                    }
                    else if (colorNameSub[i] == "white")
                    {
                        colorCode += "1";
                    }
                    else if (colorNameSub[i] == "red")
                    {
                        colorCode += "2";
                    }
                    else if (colorNameSub[i] == "orange")
                    {
                        colorCode += "3";
                    }
                    else if (colorNameSub[i] == "blue")
                    {
                        colorCode += "4";
                    }
                    else if (colorNameSub[i] == "purple")
                    {
                        colorCode += "5";
                    }
                    else if (colorNameSub[i] == "green")
                    {
                        colorCode += "6";
                    }
                    else if (colorNameSub[i] == "lime")
                    {
                        colorCode += "7";
                    }
                    else if (colorNameSub[i] == "gray")
                    {
                        colorCode += "8";
                    }
                    else if (colorNameSub[i] == "darkgray")
                    {
                        colorCode += "9";
                    }
                }
            }
            else
            {
                return "";
            }

           // MessageBox.Show(colorCode.ToString());

            return colorCode;
        }

        public bool isColorStringNumExists(string colorStringNum)
        {
            if (this.connectToDB())
            {
                string colorCodeFirstThree = convertStringNumToColorName(colorStringNum);
                //MessageBox.Show(colorCodeFirstThree);

                if (colorCodeFirstThree == "")
                {
                    return false;
                }

                string query = String.Format("SELECT colorCode FROM {0} WHERE substr(colorCode,1,3)=@colorCodeFirstThree", inventoryTableName);

                dbCommand = new SQLiteCommand(query, dbConnection);
                dbCommand.Parameters.AddWithValue("@colorCodeFirstThree", colorCodeFirstThree.Substring(0,3));

                dbReader = dbCommand.ExecuteReader();


                if(dbReader.HasRows)
                {

                    dbReader.Close();

                    return true;
                }

            }

            dbReader.Close();
            return false;
        }

        public string[] getDataWithColorCode(string colorCode)
        {
            if (this.connectToDB())
            {
                string query = String.Format("SELECT colorCode," +
                    "name," +
                    "materialNumber," +
                    "description," +
                    "unitPrice," +
                    "invoice," +
                    "stockBalance," +
                    "actualCount," +
                    "recount," +
                    "finalCount," +
                    "disrepancy," +
                    "disrepancyAmount," +
                    "remarks, date_added, date_released FROM {0} WHERE " +
                    "colorCode=@colorCode;", inventoryTableName);

                dbCommand = new SQLiteCommand(query, dbConnection);
                dbCommand.Parameters.AddWithValue("@colorCode", colorCode);

                dbReader = dbCommand.ExecuteReader();
                string[] retData = new string[15];

                if (dbReader.HasRows)
                {
                    dbReader.Read();

                    for (int i = 0; i < 15; i++)
                    {
                        if (!dbReader.IsDBNull(i))
                        {
                            retData[i] = dbReader.GetString(i);
                            
                        }
                        else
                        {
                            retData[i] = "";
                        }

                        MessageBox.Show(retData[i]);
                    }

                }

                dbReader.Close();
                return retData;

            }


            dbReader.Close();
            return null;

        }

        public string[] getDataWithNameAndMaterialNumber(string name, string materialNumber)
        {
            if (this.connectToDB())
            {
                string query = String.Format("SELECT colorCode," +
                    "name," +
                    "materialNumber," +
                    "description," +
                    "unitPrice," +
                    "invoice," +
                    "stockBalance," +
                    "actualCount," +
                    "recount," +
                    "finalCount," +
                    "disrepancy," +
                    "disrepancyAmount," +
                    "remarks, date_added, date_released FROM {0} WHERE " +
                    "name=@name AND " +
                    "materialNumber=@materialNumber;", inventoryTableName);

                dbCommand = new SQLiteCommand(query, dbConnection);
                dbCommand.Parameters.AddWithValue("@name", name);
                dbCommand.Parameters.AddWithValue("@materialNumber", materialNumber);

                dbReader = dbCommand.ExecuteReader();
                string[] retData = new string[15];

                if (dbReader.HasRows)
                {
                    dbReader.Read();

                    for (int i = 0; i < 15; i++)
                    {
                        if (!dbReader.IsDBNull(i))
                        {
                            retData[i] = dbReader.GetString(i);
                        }
                        else
                        {
                            retData[i] = "";
                        }

                        //MessageBox.Show(retData[i]);
                    }

                }

                dbReader.Close();
                return retData;
 
            }
        

            dbReader.Close();
            return null;
        }

        // Not used, just for testing purposes.
        private void removeNull()
        {
            // UPDATE SMAInventory set colorCode = ifnull(colorCode,''), materialNumber = ifnull(materialNumber,''), description = ifnull(description,''), unitPrice = ifnull(unitPrice,''), invoice = ifnull(invoice,''), stockBalance = ifnull(stockBalance,''), actualCount = ifnull(actualCount,''), recount = ifnull(recount,''),  finalCount = ifnull(finalCount,''), disrepancy = ifnull(disrepancy,''), disrepancyAmount = ifnull(disrepancyAmount,''), remarks = ifnull(remarks,'');

            if (this.connectToDB())
            {
                string query = String.Format("UPDATE {0} set colorCode = ifnull(colorCode,''), " +
                    "materialNumber = ifnull(materialNumber,''), " +
                    "description = ifnull(description,''), " +
                    "unitPrice = ifnull(unitPrice,''), " +
                    "invoice = ifnull(invoice,''), " +
                    "stockBalance = ifnull(stockBalance,''), " +
                    "actualCount = ifnull(actualCount,''), " +
                    "recount = ifnull(recount,''),  " +
                    "finalCount = ifnull(finalCount,''), " +
                    "disrepancy = ifnull(disrepancy,''), " +
                    "disrepancyAmount = ifnull(disrepancyAmount,''), " +
                    "remarks = ifnull(remarks,'');"
                        , inventoryTableName);

                dbCommand = new SQLiteCommand(query, dbConnection);
                dbCommand.ExecuteNonQuery();
            }
        }

        private static int selectedMaterialNumber;

        public static int propMaterialNumber
        {
            get { return selectedMaterialNumber;  }
            set { selectedMaterialNumber = value; }
        }

    }
}
