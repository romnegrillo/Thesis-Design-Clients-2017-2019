using System;
using System.Windows.Forms;

namespace Webert
{
    class WebertEmployeeClass
    {
        
        private string lastName, givenName, middleName;
        private int age;
        private string sex, homeAdd, contactNum, maritalStatus, contactPerson,
            relationship, contactPersonNumber;
        private decimal salary;
        private int numFingerprints;
        private int finger1, finger2, finger3, finger4;
        public static int employeeID;
        public static string pictureName;

        public static int fullTimeWorkHours = 9;
        public static int lateTimeWorkHours=6;
        public static int halfTimeWorkHours = 4;
        public static int overTimeWorkhouts = 10;
        public static int maxOverTimeHours = 13;

        public static int FTSalary;
        public static  int HTSalary;
        public static int LateSalary;
        public static int OTRate;

        public WebertEmployeeClass(params object[] items)
        {
            /*
             0 - LN
             1 - GN
             2 - MN
             3 - Age
             4 - Sex
             5 - HA
             6 - CN
             7 - MS
             8 - CP
             9 - R
             10 - CPN
             11 - Salary
             12 - NumFingerprint
             13 - PictureName
            */
  
            this.lastName=items[0].ToString();
            this.givenName=items[1].ToString();
            this.middleName = items[2].ToString();
            this.age = Convert.ToInt32(items[3]);
            this.sex = items[4].ToString();
            this.homeAdd = items[5].ToString();
            this.contactNum = items[6].ToString();
            this.maritalStatus = items[7].ToString();
            this.contactPerson = items[8].ToString();
            this.relationship = items[9].ToString();
            this.contactPersonNumber = items[10].ToString();

            if (items.Length == 12)
                this.numFingerprints = Convert.ToInt32(items[11]);
        }

        public string getLN()
        {
            return this.lastName;
        }

        public string getGN()
        {
            return this.givenName;
        }

        public string getMN()
        {
            return this.middleName;
        }

        public int getAge()
        {
            return this.age;
        }

        public string getSex()
        {
            return this.sex;
        }

        public string getHA()
        {
            return this.homeAdd;
        }

        public string getCN()
        {
            return this.contactNum;
        }

        public string getMarital()
        {
            return this.maritalStatus;
        }

        public string getContactPerson()
        {
            return this.contactPerson;
        }

        public string getCPNumber()
        {
            return this.contactPersonNumber;
        }

        public string getCPRelationship()
        {
            return this.relationship;
        }

        public int getNumFinger()
        {
            return this.numFingerprints;
        }

        public string workStatus { get; set; }

        public void setFinger1(int finger1)
        {
            this.finger1 = finger1;
        }

        public void setFinger2(int finger2)
        {
            this.finger2 = finger2;
        }

        public void setFinger3(int finger3)
        {
            this.finger3 = finger3;
        }

        public void setFinger4(int finger4)
        {
            this.finger4 = finger4;
        }

        public int getFinger1()
        {
            return this.finger1;
        }

        public int getFinger2()
        {
            return this.finger2;
        }

        public int getFinger3()
        {
            return this.finger3;
        }

        public int getFinger4()
        {
            return this.finger4;
        }

    }
}
