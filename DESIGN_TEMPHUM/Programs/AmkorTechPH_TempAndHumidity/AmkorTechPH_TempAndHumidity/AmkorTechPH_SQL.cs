using System;
using System.Data;
using System.Data.SQLite;
using System.Windows.Forms;

namespace AmkorTechPH_TempAndHumidity
{
    class AmkorTechPH_SQL
    {
        SQLiteConnection dbConnection;
        SQLiteCommand dbCommand;
        string dbName;
        bool isDBConnected;

        public AmkorTechPH_SQL(string dbName)
        {
            //createDatabase(dbName);
            connectDatabase(dbName);
            this.dbName = dbName;
            isDBConnected = false;
        }

        private void createDatabase(string dbName)
        {
            SQLiteConnection.CreateFile(dbName);
            dbConnection=new SQLiteConnection(string.Format("Data Source={0};Version=3;",dbName));
            dbConnection.Open();

            string query = "CREATE TABLE monitor(id INT PRIMARY KEY, temp REAL, humidity REAL, " +
                "time DATETIME);";

            dbCommand = new SQLiteCommand(query, dbConnection);
            dbCommand.ExecuteNonQuery();
        }

        private void connectDatabase(string dbName)
        {
            dbConnection = new SQLiteConnection(string.Format("Data Source={0};Version=3;", dbName));
            dbConnection.Open();
            this.isDBConnected = true;
        }

        public bool isDbConnected()
        {
            return this.isDBConnected;
        }

        public void addData(int temperature, int relHumidity)
        {
            // Add to the database the temperature and relative
            // humidity.

            // Time is generated in this function when it is received.
            DateTime now = DateTime.Now;
            //MessageBox.Show(now.ToString("yyyy-MM-dd hh:mm tt"));
            string time = now.ToString("yyyy-MM-dd hh:mm");

            string query = "INSERT INTO monitor(temp,humidity,time) VALUES(@2,@3,@4);";
            dbCommand = new SQLiteCommand(query, dbConnection);
            dbCommand.Parameters.AddWithValue("@1", this.dbName);
            dbCommand.Parameters.AddWithValue("@2",temperature);
            dbCommand.Parameters.AddWithValue("@3",relHumidity);
            dbCommand.Parameters.AddWithValue("@4", time);

            dbCommand.ExecuteNonQuery();
        
            // ID will also increment in this function.
        }

        public DataTable getData()
        {
            // Return whole data in the database without the ID.
            string query = "SELECT `temp`,`humidity`,`time` FROM monitor ORDER BY id DESC;";

            dbCommand = new SQLiteCommand(query, dbConnection);
            SQLiteDataReader dbReader = dbCommand.ExecuteReader();
            DataTable dbTable = new DataTable();
            dbTable.Load(dbReader);

            return dbTable;
        }

        public void clearData()
        {
            // No truncate in sqlite. This i the equivalent of truncate.
            string query = "DELETE FROM monitor;";

            dbCommand = new SQLiteCommand(query, dbConnection);
            dbCommand.ExecuteNonQuery();
        }
    }
}
