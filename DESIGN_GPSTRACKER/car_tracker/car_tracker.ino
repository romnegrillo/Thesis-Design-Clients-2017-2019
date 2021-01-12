#include <LiquidCrystal.h>
#include <Wire.h>
#include <TinyGPS.h>
#include <SoftwareSerial.h>

// MPU6050 variables.
long accelX, accelY, accelZ;
float gForceX, gForceY, gForceZ;

long gyroX, gyroY, gyroZ;
float rotX, rotY, rotZ;
float gForceMagnitude;


// Calibration:
// rotX=7.xx
// rotY=4.xx
// rotZ=0.xx
float rotXCalib=7.00;
float rotYCalib=4.00;
float rotZCalib=0.00;


// Vibration sensitivity adjustment.
// Lower value, higher sensitivity.

float rotXSen=5;
float rotYSen=5;
float rotZSen=5;

// LCD constants and object.
const int rs = 12, en = 11, d4 = 2, d5 = 3, d6 = 4, d7 = 5;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

// GPS objects and variables.
TinyGPS gps;
SoftwareSerial ss(A0, A1);
float lat=0.00,lon=0.00;
bool newData=false;

// GSM object and variables.
SoftwareSerial gsmSerial(7,8);
String inText;
String googleLinkFormat="https://www.google.com/maps/search/?api=1&query=<lat>,<lon>";
String phoneNumber="+639171709038";
int sendingInterval=1000*60*5;

// Panic button and buzzer pins;
const int panicButtonPin=10;
const int buzzerPin=A2;
const int autoPowerPin=9;

// Timer variables.
unsigned long startTime;

void setup() 
{
   autoOnSIM900();
  pinMode(panicButtonPin,INPUT_PULLUP);
  pinMode(buzzerPin,OUTPUT);
   
      
  Wire.begin();
  setupMPU();

  Serial.begin(9600);
  ss.begin(9600);
  gsmSerial.begin(9600);
    
  lcd.begin(16, 2);
  lcd.print("Loading...");

   autoOnSIM900();
   
  delay(2000);

  getGPSData();
 
  initGSM();
  operatingMode();
}

void loop() 
{

  recordAccelRegisters();
  recordGyroRegisters();
  //printData();
  detecVibration();
  panicButtonListen();
  receiveSMS();

  if(millis()-startTime >= sendingInterval)
  {
    startTime=millis();

    String toSend="I'm already at ";
    toSend+=googleLinkFormat;
    toSend.replace("<lat>",String(lat));
    toSend.replace("<lon>",String(lon));

    sendSMS(toSend);
  }
  
  delay(500);
}

void setupMPU()
{
  Wire.beginTransmission(0b1101000); //This is the I2C address of the MPU (b1101000/b1101001 for AC0 low/high datasheet sec. 9.2)
  Wire.write(0x6B); //Accessing the register 6B - Power Management (Sec. 4.28)
  Wire.write(0b00000000); //Setting SLEEP register to 0. (Required; see Note on p. 9)
  Wire.endTransmission();  
  Wire.beginTransmission(0b1101000); //I2C address of the MPU
  Wire.write(0x1B); //Accessing the register 1B - Gyroscope Configuration (Sec. 4.4) 
  Wire.write(0x00000000); //Setting the gyro to full scale +/- 250deg./s 
  Wire.endTransmission(); 
  Wire.beginTransmission(0b1101000); //I2C address of the MPU
  Wire.write(0x1C); //Accessing the register 1C - Acccelerometer Configuration (Sec. 4.5) 
  Wire.write(0b00000000); //Setting the accel to +/- 2g
  Wire.endTransmission(); 
}

void recordAccelRegisters() 
{
  Wire.beginTransmission(0b1101000); //I2C address of the MPU
  Wire.write(0x3B); //Starting register for Accel Readings
  Wire.endTransmission();
  Wire.requestFrom(0b1101000,6); //Request Accel Registers (3B - 40)
  while(Wire.available() < 6);
  accelX = Wire.read()<<8|Wire.read(); //Store first two bytes into accelX
  accelY = Wire.read()<<8|Wire.read(); //Store middle two bytes into accelY
  accelZ = Wire.read()<<8|Wire.read(); //Store last two bytes into accelZ
  processAccelData();
}

void processAccelData()
{
  gForceX = accelX / 16384.0;
  gForceY = accelY / 16384.0; 
  gForceZ = accelZ / 16384.0;

  gForceMagnitude=pow(gForceX,2)+pow(gForceY,2)+pow(gForceZ,2);
}

void recordGyroRegisters() 
{
  Wire.beginTransmission(0b1101000); //I2C address of the MPU
  Wire.write(0x43); //Starting register for Gyro Readings
  Wire.endTransmission();
  Wire.requestFrom(0b1101000,6); //Request Gyro Registers (43 - 48)
  while(Wire.available() < 6);
  gyroX = Wire.read()<<8|Wire.read(); //Store first two bytes into accelX
  gyroY = Wire.read()<<8|Wire.read(); //Store middle two bytes into accelY
  gyroZ = Wire.read()<<8|Wire.read(); //Store last two bytes into accelZ
  processGyroData();
}

void processGyroData() 
{
  rotX = gyroX / 131.0;
  rotY = gyroY / 131.0; 
  rotZ = gyroZ / 131.0;
}

void printData() 
{
  Serial.print("Gyro (deg)");
  Serial.print(" X=");
  Serial.print(rotX);
  Serial.print(" Y=");
  Serial.print(rotY);
  Serial.print(" Z=");
  Serial.print(rotZ);
  Serial.print(" Accel (g)");
  Serial.print(" X=");
  Serial.print(gForceX);
  Serial.print(" Y=");
  Serial.print(gForceY);
  Serial.print(" Z=");
  Serial.println(gForceZ);
}

void clearLCD()
{
  lcd.setCursor(0,0);
  lcd.println("                ");
  lcd.setCursor(0,1);
  lcd.println("                ");
  lcd.setCursor(0,0);
}

void getGPSData()
{
  ss.listen();
  
  clearLCD();
  lcd.print("Updating GPS...");
  lcd.setCursor(0,1);
  lcd.print("Please wait...");

  //newData = false;
  unsigned long chars;
  unsigned short sentences, failed;

  while(!newData)
  {
    // For one second we parse GPS data and report some key values
    for (unsigned long start = millis(); millis() - start < 1000;)
    {
      while (ss.available())
      {
        char c = ss.read();
         //Serial.write(c); // uncomment this line if you want to see the GPS data flowing
        if (gps.encode(c)) // Did a new valid sentence come in?
          newData = true;
      }
    }
  
    if (newData)
    {
      float flat, flon;
      unsigned long age;
      gps.f_get_position(&flat, &flon, &age);
  
       lat = flat == TinyGPS::GPS_INVALID_F_ANGLE ? 0.0 : flat, 6;
       lon = flon == TinyGPS::GPS_INVALID_F_ANGLE ? 0.0 : flon, 6;

       //Serial.println(lat);
       //Serial.println(lon);
  
    }
  }

  delay(1000);
  
  clearLCD();
  lcd.print("Location");
  lcd.setCursor(0,1);
  lcd.print("recorded!");

  delay(1000);

  gsmSerial.listen();
}

void operatingMode()
{
  clearLCD();
  lcd.print("Operating mode");
}

void detecVibration()
{
  if(abs(rotX) > (rotXCalib+rotXSen) || 
     abs(rotY) > (rotYCalib+rotYSen) || 
     abs(rotZ) > (rotZCalib+rotZSen) 

  )
  {
    String toSend="Vibration detected at ";
    toSend+=googleLinkFormat;
    toSend.replace("<lat>",String(lat));
    toSend.replace("<lon>",String(lon));

    clearLCD();
    lcd.setCursor(0,0);
    lcd.print("Vibration");
    lcd.setCursor(0,1);
    lcd.print("detected!");

    digitalWrite(buzzerPin,HIGH);
    
    Serial.println(toSend);
    sendSMS(toSend);
    
    operatingMode();

    digitalWrite(buzzerPin,LOW);
  }
}

void initGSM()
{
  gsmSerial.listen();

  clearLCD();
  lcd.print("Connecting");
  lcd.setCursor(0,1);
  lcd.print("to network...");
  
    while (!gsmSerial.available())
  {
    gsmSerial.println("AT");
    delay(1000);
    Serial.println("Connecting...");
  }

  clearLCD();
  lcd.print("Connected");
  lcd.setCursor(0,1);
  lcd.print("to Globe...");
  
  delay(2000);
  
  Serial.println("Connected!");
  
  gsmSerial.println("AT+CMGF=1");
  delay(500);
  
  gsmSerial.println("AT + CMGS = \"" + phoneNumber + "\""); 
  delay(500);
  
  gsmSerial.println("GSM initialized!"); 
  delay(500);

  gsmSerial.println((char)26); 
  delay(500);
  
  gsmSerial.println();
  
  delay(1000); 
  
  // Go back to receive mode.

  gsmSerial.print("AT+CMGF=1\r"); 
  delay(500);
  
  // Set module to send SMS data to serial out upon receipt 
  gsmSerial.print("AT+CNMI=2,2,0,0,0\r");
  delay(500);
}

void sendSMS(String message)
{
  gsmSerial.listen();
  
  gsmSerial.println("AT+CMGF=1");
  delay(500);
  
  gsmSerial.println("AT + CMGS = \"" + phoneNumber + "\""); 
  delay(500);
  
  gsmSerial.println(message); 
  delay(500);

  gsmSerial.println((char)26); 
  delay(500);
  
  gsmSerial.println();
  
  delay(1000); 

  // Go back to receive mode.

  gsmSerial.print("AT+CMGF=1\r"); 
  delay(500);
  
  // Set module to send SMS data to serial out upon receipt 
  gsmSerial.print("AT+CNMI=2,2,0,0,0\r");
  delay(500);
}

void receiveSMS()
{ 
  bool isNewText=false;
  
  if(gsmSerial.available()>0) 
  {
    //Get the character from the cellular serial port
    inText=gsmSerial.readString(); 

    Serial.println("Received Text: ");
    Serial.println(inText);

    if(inText.indexOf("WHEREAREYOU") > -1)
    {
      String toSend="I'm already at ";
      toSend+=googleLinkFormat;
      toSend.replace("<lat>",String(lat));
      toSend.replace("<lon>",String(lon));
  
      clearLCD();
      lcd.setCursor(0,0);
      lcd.print("Location");
      lcd.setCursor(0,1);
      lcd.print("request!");
  
      Serial.println(toSend);
      sendSMS(toSend);
      
      operatingMode();
    }

    inText="";
  }
}

void panicButtonListen()
{
  if(!digitalRead(panicButtonPin))
  {
    String toSend="An emergency occurred at ";
    toSend+=googleLinkFormat;
    toSend.replace("<lat>",String(lat));
    toSend.replace("<lon>",String(lon));

    clearLCD();
    lcd.setCursor(0,0);
    lcd.print("Panic button");
    lcd.setCursor(0,1);
    lcd.print("pressed!");

    Serial.println(toSend);
    sendSMS(toSend);
    
    operatingMode();
  }
}

void autoOnSIM900()
{
  pinMode(autoPowerPin,OUTPUT);

// digitalWrite(autoPowerPin,HIGH);
// delay(2000);
// digitalWrite(autoPowerPin,LOW);
//  delay(3000);
}
