using System;
using System.Data.SQLite;
using System.Windows.Forms;

namespace DESIGN_COLORCODE
{
    class SMAAdmins_Model
    {
        private string username, password;
        private int numTries;

        // As per client requirements, admin name and password is hardcoded only.
        // Admin name and password are stored in the database. 
        // Maximum number of attempted login and change password is 5.
        public static int maxNumTries = 5;
        public static string adminUser = "";
        public static string adminPassword = "";

        private const string dbName = "SMADatabase.db";
        private const string adminTableName = "SMAAdmin";
        private const string userTableName = "SMAUsers";

        SQLiteConnection dbConnection;
        SQLiteCommand dbCommand;
        SQLiteDataReader dbReader;
        
        // Constructor for accessing admin checking methods.
        public SMAAdmins_Model() { }

        // Constructor for checking number of attempts in changing password.
        public SMAAdmins_Model(int numTries)
        {
            // Get the username and password in the database when in the
            // change password window because username will be needed.
            // Only one username should be in the database, else the top
            // one will be selected.
            this.getAdminUserPassInDB();
            this.numTries = 0;
        }

        // Constructor for checking username and password of the admin.
        public SMAAdmins_Model(string username, string password)
        {
            this.username = username;
            this.password = password;
        }

        private void getAdminUserPassInDB()
        {
            if (this.connectToDB())
            {
                string query = String.Format("SELECT username,password FROM {0};", adminTableName);

                dbCommand = new SQLiteCommand(query, dbConnection);
                dbReader = dbCommand.ExecuteReader();

                if (dbReader.HasRows)
                {
                    dbReader.Read();
                    string[] data = { dbReader.GetString(0), dbReader.GetString(1)};

                    SMAAdmins_Model.adminUser = data[0];
                    //MessageBox.Show(data[0] + " " + data[1]);
                }
                dbReader.Close();
            }
        }

        public bool doesAdminExists()
        {
            // Query database if admin exists.

            if(this.connectToDB())
            {
                string query = String.Format("SELECT * FROM {0} WHERE username=@username AND password=@password;",adminTableName );

                dbCommand = new SQLiteCommand(query, dbConnection);
                dbCommand.Parameters.AddWithValue("@username", this.username);
                dbCommand.Parameters.AddWithValue("@password", this.password);

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

        private bool checkAdminPassword(string username, string currentPass)
        {
            // Query database if current password is correct for the admin.

            if (this.connectToDB())
            {
                string query = String.Format("SELECT * FROM {0} WHERE username=@username AND password=@password;", adminTableName);

                dbCommand = new SQLiteCommand(query, dbConnection);
                dbCommand.Parameters.AddWithValue("@username", username);
                dbCommand.Parameters.AddWithValue("@password", currentPass);

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

        public bool changeAdminPassword(string username, string currentPass, string newPass)
        {
            // Query database to change admin password.
            // Check first if the current password is correct.
   
            if (this.checkAdminPassword(username, currentPass))
            {
                if (this.connectToDB())
                { 
                    string query = String.Format("UPDATE {0} SET password=@password WHERE username=@username;", adminTableName);
         
                    dbCommand = new SQLiteCommand(query, dbConnection);
                    dbCommand.Parameters.AddWithValue("@username", username);
                    dbCommand.Parameters.AddWithValue("@password", newPass);

                    int isSuccess = dbCommand.ExecuteNonQuery();

                    if(isSuccess!=0)
                    {
                       
                        return true;
                    }

                  
                }
            }
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


        public bool registerUser(string username)
        {
            // Query database to register user.
            // Check first if user exists.
            SMAUsers_Model smaUsers = new SMAUsers_Model(username);

            if (!smaUsers.doesUserExists())
            {

                if (this.connectToDB())
                {
                    string query = String.Format("INSERT INTO {0}(username) VALUES(@username);", userTableName);


                    dbCommand = new SQLiteCommand(query, dbConnection);
                    dbCommand.Parameters.AddWithValue("@username", username);
                    dbCommand.ExecuteNonQuery();

                    return true;
                }
            }

            return false;
        }

        public int propNumTries
        {
            get { return this.numTries; }
            set { this.numTries = value; }
        }
    }
}
