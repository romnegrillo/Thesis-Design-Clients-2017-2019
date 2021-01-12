#include <SoftwareSerial.h>
#include <RH_ASK.h>
#include<LiquidCrystal_I2C.h>
#include "DHT.h"

#define DHTPIN 10  
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);
LiquidCrystal_I2C lcd(0x3F,2,1,0,4,5,6,7,3, POSITIVE);

SoftwareSerial picSS(3,2);
SoftwareSerial gsmSerial(7,8);

String data;
int temp;
int relHum;
bool DEBUG=false;
int powerLEDPin=13;
int buzzPin=9;
int buzz=9;
String toReceiver;

RH_ASK driver; // PIN12
char msg[4];

void setup() 
{
  dht.begin();
  pinMode(powerLEDPin, OUTPUT);
  pinMode(buzzPin, OUTPUT);
  //digitalWrite(buzzPin,HIGH);
  
  Serial.begin(9600);

  gsmSerial.begin(9600);
  //initGSM();
    picSS.begin(9600);
  if (!driver.init() && DEBUG)
  {
         //Serial.println("init failed");
  }

    lcd.begin(16,2);
  lcd.print("Loading...");
  delay(2000);
 
}

void loop() 
{
    
  picSS.listen();
  
  int h = dht.readHumidity();
  // Read temperature as Celsius (the default)
  int t = dht.readTemperature();


  if(true)
  {
    //picSS.flush();
 
 

    toReceiver=String(t)+","+String(h);

    int tempTemp=t;
    int tempRelHum=h;

        if (isnan(h) || isnan(t) ) {
 
    return;
  }

    String rowOne="Temp: " + String(tempTemp) +  String(" C          ");
    String rowTwo="Humidity: " + String(tempRelHum)+  String(" %          ");
  
      lcd.setCursor(0,0);
      lcd.print(rowOne);
      lcd.setCursor(0,1);
      lcd.print(rowTwo);
    
    if(DEBUG)
    {
      Serial.println(data); 
      Serial.print("Temperature: ");
      Serial.println(String(temp));
      Serial.print("Relative Humidity: ");
      Serial.println(String(relHum));
      Serial.print("To Receiver: ");
      Serial.println(toReceiver);
    }

      toReceiver.toCharArray(msg,6);
      //Serial.println(msg);
 
      //Serial.println(tempTemp);
      //Serial.println(tempRelHum);
      
      if(tempTemp!=0 && tempRelHum!=0)
      {
      driver.send((uint8_t *)msg, strlen(msg));
      driver.waitPacketSent();

      if(tempTemp<22 || tempTemp>29 || tempRelHum<55 || tempRelHum>65)
      {
            digitalWrite(powerLEDPin,HIGH);
        // Send SMS and alarm.
        //digitalWrite(buzzPin,HIGH);
        tone(buzzPin, 35000000);
        //Serial.println(String(relHum));
        //Serial.println("buzz");
        //sendSMS("Warning, temperature is: " + String(tempTemp) + " C" + ". Relative humidity is: " + String(tempRelHum) + "%");
      } 
      else
      {
        noTone(buzzPin);
      }
      }
  }



     delay(8000);
}

void sendSMS(String text)
{

  /////////////////////////////////////////////////////////////
  
  Serial.println("Sending Text...");
  gsmSerial.println("AT+CMGF=1");
  delay(1000);
  //siren();
  gsmSerial.print("AT+CMGS=\"+639776811077\"\r");
  //gsmSerial.print("AT+CMGS=\"+639396182624\"\r");
  
  
  delay(1000);
  //siren();
  gsmSerial.print(text);
  delay(1000);
  //siren();
  gsmSerial.print((char)26);
  delay(1000);
  //siren();
  gsmSerial.println();
  Serial.println("Message sent!");
  delay(1000);

  ///////////////////////////////////////////////////////////

}

void initGSM()
{
  while (!gsmSerial.available())
  {
    gsmSerial.println("AT");
    delay(1000);
    Serial.println("Connecting...");
  }

  Serial.println("Connected!");

  gsmSerial.println("AT+CMGF=1");
  
  delay(1000);
  gsmSerial.println("AT+CNMI=1,2,0,0,0");
  delay(1000);

  Serial.println("DEBUG");
  gsmSerial.println("AT+CMGL=\"REC UNREAD\"");
  delay(1000);
  gsmSerial.println("AT+CMGDA=\"DEL ALL\"");
  delay(1000);

  Serial.println("All messages deleted!");

  Serial.println("Sending Text...");

  gsmSerial.println("AT+CMGF=1");
  delay(1000);

  gsmSerial.print("AT+CMGS=\"+639776811077\"\r");
  //gsmSerial.print("AT+CMGS=\"+639396182624\"\r");
  delay(1000);

  gsmSerial.print("Amkortech Device Initialized!");
  delay(1000);

  gsmSerial.print((char)26);
  delay(1000);

  gsmSerial.println();

  Serial.println("Message sent!");
 
}

void siren() {         
  // Whoop up
  for(int hz = 440; hz < 1000; hz+=25){
    tone(buzz, hz, 50);
    delay(20);
   //for(int i=3;i<=7;i++)
    //digitalWrite(i,HIGH);
  }
  // Whoop down
  for(int hz = 1000; hz > 440; hz-=25){
    tone(buzz, hz, 50);
    delay(20);
    //for(int i=3;i<=7;i++)
   // {
    //  digitalWrite(i,LOW);
     // digitalWrite(i+5,HIGH);
    //  }
  }
  noTone(buzz);
  digitalWrite(buzz,HIGH);
}

void sirenv2()
{
  for(int i=0; i<5; i++)
  {
      digitalWrite(buzzPin, HIGH);
      delay(500);
      digitalWrite(buzzPin, LOW);
      delay(500);
  }
}

