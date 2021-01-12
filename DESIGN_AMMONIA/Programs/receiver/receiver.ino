#include<SoftwareSerial.h>

SoftwareSerial ss(3,2);
int buzzPin=9;
bool hazardOnce=false;
unsigned long int startTime;

void setup() 
{
  Serial.begin(9600);
  ss.begin(9600);
  pinMode(buzzPin,OUTPUT);
}

void loop() 
{
  //if(ss.available())
  if(true)
  {
    String dataIn=ss.readStringUntil("\n");
    Serial.print(dataIn);

    //int isFull=dataIn.substring(dataIn.length()-3,dataIn.length()).toInt();
    //Serial.println(isFull);
    float hazardLevel=dataIn.substring(0,6).toFloat();
 
    //Serial.println(hazardLevel);
    //hazardLevel=0.06;
    
    if(hazardLevel>0.05)
    {
  
      if(!hazardOnce)
      {
        startTime=millis();
        hazardOnce=true;

        digitalWrite(buzzPin,HIGH);
      }

      if( (millis()-startTime > 10000) && hazardOnce)
      {
         digitalWrite(buzzPin,LOW);
      }
    }
    else
    {
      digitalWrite(buzzPin,LOW);
      hazardOnce=false;
    }
  }


}
