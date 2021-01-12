package com.example.thesis_glucose;

public class GlucoseLevelMeasurement {

    private double BMI;
    private double glucoseLevel;

    public GlucoseLevelMeasurement() {

    }


    public double getInsulin()
    {
       if(this.BMI<25)
       {
            // Get glucose level.

           if(this.glucoseLevel<151)
           {
               return 0.0; // No insulin.
           }
           else
           {
               if(this.glucoseLevel>=151 && this.glucoseLevel<=175)
               {
                   return 1.4;
               }
               else if(this.glucoseLevel>=176 && this.glucoseLevel<=200)
               {
                   return 2.4;
               }
               else if(this.glucoseLevel>=201 && this.glucoseLevel<=225)
               {
                   return 3.4;
               }
               else if(this.glucoseLevel>=226 && this.glucoseLevel<=250)
               {
                   return 5.5;
               }
               else if(this.glucoseLevel>=251 && this.glucoseLevel<=275)
               {
                   return 7.5;
               }
               else if(this.glucoseLevel>=276 && this.glucoseLevel<=300)
               {
                   return 9.4;
               }
               else if(this.glucoseLevel<300)
               {
                   return 12;
               }
           }
       }
       else if(this.BMI>=25 && this.BMI<=30)
       {
           // Get glucose level.

           if(this.glucoseLevel<151)
           {
               return 0.0; // No insulin.
           }
           else
           {
               if(this.glucoseLevel>=151 && this.glucoseLevel<=175)
               {
                   return 2.5;
               }
               else if(this.glucoseLevel>=176 && this.glucoseLevel<=200)
               {
                   return 4.4;
               }
               else if(this.glucoseLevel>=201 && this.glucoseLevel<=225)
               {
                   return 6.6;
               }
               else if(this.glucoseLevel>=226 && this.glucoseLevel<=250)
               {
                   return 8.5;
               }
               else if(this.glucoseLevel>=251 && this.glucoseLevel<=275)
               {
                   return 10.5;
               }
               else if(this.glucoseLevel>=276 && this.glucoseLevel<=300)
               {
                   return 12.5;
               }
               else if(this.glucoseLevel<300)
               {
                   return 14.5;
               }
           }
       }
       else if(this.BMI>=25)
       {
           // Get glucose level.

           if(this.glucoseLevel<151)
           {
               return 0.0; // No insulin.
           }
           else
           {
               if(this.glucoseLevel>=151 && this.glucoseLevel<=175)
               {
                   return 3.6;
               }
               else if(this.glucoseLevel>=176 && this.glucoseLevel<=200)
               {
                   return 6.6;
               }
               else if(this.glucoseLevel>=201 && this.glucoseLevel<=225)
               {
                   return 7.6;
               }
               else if(this.glucoseLevel>=226 && this.glucoseLevel<=250)
               {
                   return 9.6;
               }
               else if(this.glucoseLevel>=251 && this.glucoseLevel<=275)
               {
                   return 11.6;
               }
               else if(this.glucoseLevel>=276 && this.glucoseLevel<=300)
               {
                   return 14.6;
               }
               else if(this.glucoseLevel<300)
               {
                   return 18.6;
               }
           }
       }

       return 0.0;
    }

    public double getBMILevel(double weight, double height) {
        // BMI formula, imperial
        // Weight in kg
        // Height in ft.
        // Convert height in ft to m
        // BMI resulting formula is kg/m^2
        height = height*(0.3048/1);

        this.BMI = Math.round(((weight)/Math.pow(height,2))*100.0)/100.0;

        return  this.BMI;
    }

    public double getGlucoseLevel()
    {
        return this.glucoseLevel;
    }

    public void setGlucoseLevel(double NIR_reading)
    {
        this.glucoseLevel=NIR_reading;

        //this.glucoseLevel = -0.0437*this.glucoseLevel + 358.66;

        // Form 1
        this.glucoseLevel = -0.0425*this.glucoseLevel + 323.18;

        // Form 2
        //this.glucoseLevel = -0.0437*this.glucoseLevel + 358.66;

    }


}
