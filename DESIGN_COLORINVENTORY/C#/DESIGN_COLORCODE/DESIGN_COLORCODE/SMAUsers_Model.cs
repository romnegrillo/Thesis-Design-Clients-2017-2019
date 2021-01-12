using System.Data.SQLite;
using System;
using System.Windows.Forms;

namespace DESIGN_COLORCODE
{
    class SMAUsers_Model
    {
        private string username;
        private const string dbName = "SMADatabase.db";
        private const string userTableName = "SMAUsers";

        SQLiteConnection dbConnection;
        SQLiteCommand dbCommand;
        SQLiteDataReader dbReader;

        public SMAUsers_Model(string username)
        {
            this.username = username;
        }

        public bool doesUserExists()
        {
            // Query database if user exists.

            if(this.connectToDB())
            {

                string query = String.Format("SELECT * FROM {0} WHERE username=@username", userTableName);

                dbCommand = new SQLiteCommand(query, dbConnection);
                dbCommand.Parameters.AddWithValue("@username", this.username);

                dbReader = dbCommand.ExecuteReader();

                if (dbReader.HasRows)
                {
                    dbReader.Close();
                    return true;
                }
            }

            dbReader.Close();
            return false;
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


    }
}
