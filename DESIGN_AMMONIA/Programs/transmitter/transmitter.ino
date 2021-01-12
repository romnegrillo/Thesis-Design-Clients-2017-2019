#include <LiquidCrystal.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <SoftwareSerial.h>

// LCD Definitons
const int rs = 12, en = 11, d4 = 2, d5 = 3, d6 = 4, d7 = 5;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

// =================================================================

// pH Sensor Definitions
#define SensorPin A3            //pH meter Analog output to Arduino Analog Input 0
#define Offset 0.00            //deviation compensate
#define LED 13
#define samplingInterval 20
#define printInterval 800
#define ArrayLenth  40    //times of collection
int pHArray[ArrayLenth];   //Store the average value of the sensor feedback
int pHArrayIndex=0; 

// =================================================================

// DS18B20 Sensor Definitions
// Data wire is plugged into port 2 on the Arduino
#define ONE_WIRE_BUS A0

// Setup a oneWire instance to communicate with any OneWire devices (not just Maxim/Dallas temperature ICs)
OneWire oneWire(ONE_WIRE_BUS);

// Pass our oneWire reference to Dallas Temperature. 
DallasTemperature sensors(&oneWire);

// =================================================================

// Sonar definitions,
const int trigger=A4;
const int echo=A5;

// =================================================================

// Relay definitions.
int relayPump=A1;
int relayDrain=A2;

// =================================================================

// SoftwareSerial for Zigbee.
SoftwareSerial ZigbeeSS(8,7);

// Helper variables.
bool DEBUG=false;
String offset="                ";
bool isReadyToSend=false;
bool drainStarted=false;
unsigned long int sendStartTime;
unsigned long int startDraining;
int fullDistanceInCM=20;
int drainingTimeInMS=20000;
int sonarStatus=0;

// To send to receiver.
String toReceiver;

void setup() 
{
  pinMode(relayPump,OUTPUT);
  pinMode(relayDrain, OUTPUT);
  waterPumpOFF();
  drainOFF();
    
  Serial.begin(9600);
  ZigbeeSS.begin(9600);

  lcd.begin(16, 2);
  lcd.setCursor(0,0);

  pinMode(trigger, OUTPUT);
  pinMode(echo, INPUT);

  sensors.begin();

  lcd.print("Loading...");

  unsigned long startTime=millis();

  // Warm up the sensor.
  warmUpSensor();
  
  lcd.clear();
  lcd.print("Loading done!");
  delay(2000);
}

void warmUpSensor()
{
  // 5 seconds warmp up.
  
  unsigned long startTime=millis();

  // Warm up the sensor for 5 seconds.
  while((millis()-startTime)<5000)
  {
    getPhValue();
    getTemperatureInC();
  }
}

void loop() 
{
  double pHValue=getPhValue();
  double tempCValue=getTemperatureInC();
  double af=getAmmoniaFactor(pHValue,tempCValue);
  int sonarDistance=getDistance();
  
  if(DEBUG)
  {
    Serial.print("ph Value: ");
    Serial.println(pHValue);
    Serial.print("AF: ");
    Serial.println(af,4);
    Serial.print("Temperature: ");
    Serial.println(tempCValue);
    Serial.print("Sonar Distance: ");
    Serial.println(sonarDistance);
    Serial.println("=============================");
  }

  // Arrangment 1
  lcd.setCursor(0,0);
  lcd.print(String("pH:") + String(pHValue) + String(" A:") + String(af,4));
  lcd.setCursor(0,1);
  lcd.print("Temp " + String(tempCValue) + String (" C") + offset);

  if(drainStarted)
  {
      lcd.setCursor(15,1);
      lcd.print("*");
  }

  // Arrangement 2
  //lcd.setCursor(0,0);
  //lcd.print(String("pH: ") + String(" AF:  ") + String("  Temp:") + offset);
  //lcd.setCursor(0,1);
  //lcd.print(String(pHValue) + String(" ") + String("0.0001") + String(" ") + String(tempCValue) + offset);


    // Check first if the water level is max.
    // I'll set water level is max if the reading of
    // sonar is less than or equal to 20 cm.
   if(sonarDistance<=fullDistanceInCM && sonarDistance!=0)
   {
      // Drain.
      sonarStatus=1;

      if(!drainStarted)
      {
        startDraining=millis();        
        drainON();
        drainStarted=true;
      }
   }


  if(((millis()-startDraining)>drainingTimeInMS) && drainStarted)
  {
    drainOFF();
    drainStarted=false;
    sonarStatus=0;
  }
    
  if(af>=0.05 && drainStarted==false)
  {
    waterPumpON();
  }
  else
  {
    waterPumpOFF();
  }
  
  if(!isReadyToSend)
  {
    sendStartTime=millis();
    isReadyToSend=true;
  }

  // Format: af,pHValue,tempCValue,sonarStatus
  toReceiver="";
  toReceiver+=String(af,4);
  toReceiver+=",";
  toReceiver+=String(pHValue);
  toReceiver+=",";
  toReceiver+=String(tempCValue);
  toReceiver+=",";
  toReceiver+=String(sonarStatus);

  
  // Send data to zigbee every 1 second only.
  if(((millis()-sendStartTime)>1000))
  {
    if (DEBUG) {Serial.println("Sending to zigbee...");}
    ZigbeeSS.println(toReceiver);
    Serial.println(toReceiver);
    isReadyToSend=false;
  }
}

double getPhValue()
{
  static unsigned long samplingTime = millis();
  static unsigned long printTime = millis();
  static float pHValue,voltage;
  if(millis()-samplingTime > samplingInterval)
  {
      pHArray[pHArrayIndex++]=analogRead(SensorPin);
      if(pHArrayIndex==ArrayLenth)pHArrayIndex=0;
      voltage = avergearray(pHArray, ArrayLenth)*5.0/1024;
      pHValue = 3.5*voltage+Offset;
      samplingTime=millis();
  }
  if(millis() - printTime > printInterval)   //Every 800 milliseconds, print a numerical, convert the state of the LED indicator
  {
      return pHValue;
  }  
}


double getAmmoniaFactor(double pHValue, double tempInC)
{
  // A=[10^((0.0901821)+((2729.92)/(273.15-tempInC))-pHValue)+1]^-1

  double base10=10.0;
  double exponent=0.0901821+((2729.92)/(273.15-tempInC))-pHValue;
  // For testing formula.
  //exponent=1;
  double af=1.0/(pow(base10,exponent)+1);
  af=round(af*10000.0)/10000.0;

  return af;
}

int getDistance()
{
  digitalWrite(trigger, LOW);
  delayMicroseconds(2);

  digitalWrite(trigger, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigger, LOW);

  int distance = pulseIn(echo, HIGH);
  distance = distance * 0.034 / 2;

  // Check sensor distance ranger.
  if(!(distance>=2 && distance<=400))
  {
    return 0;
  }

  return distance;
}

void waterPumpON()
{
  digitalWrite(relayPump,LOW);
}

void waterPumpOFF()
{
  digitalWrite(relayPump,HIGH);
}

void drainON()
{
  digitalWrite(relayDrain,LOW);
}

void drainOFF()
{
  digitalWrite(relayDrain,HIGH);
}

double getTemperatureInC()
{
   sensors.requestTemperatures(); // Send the command to get temperatures
   return sensors.getTempCByIndex(0);
}

double avergearray(int* arr, int number){
  int i;
  int max,min;
  double avg;
  long amount=0;
  if(number<=0){
    if(DEBUG)
    Serial.println("Error number for the array to avraging!/n");
    return 0;
  }
  if(number<5){   //less than 5, calculated directly statistics
    for(i=0;i<number;i++){
      amount+=arr[i];
    }
    avg = amount/number;
    return avg;
  }else{
    if(arr[0]<arr[1]){
      min = arr[0];max=arr[1];
    }
    else{
      min=arr[1];max=arr[0];
    }
    for(i=2;i<number;i++){
      if(arr[i]<min){
        amount+=min;        //arr<min
        min=arr[i];
      }else {
        if(arr[i]>max){
          amount+=max;    //arr>max
          max=arr[i];
        }else{
          amount+=arr[i]; //min<=arr<=max
        }
      }//if
    }//for
    avg = (double)amount/(number-2);
  }//if
  return avg;
}

