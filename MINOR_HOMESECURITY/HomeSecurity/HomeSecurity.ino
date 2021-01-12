#include <GPRS_Shield_Arduino.h>
#include <SoftwareSerial.h>
#include <Wire.h>

SoftwareSerial gsmSerial(2, 3);  

int pirPin=4;
int flamePin=5;                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
int gasPin=6;
int buzzerPin=7;

void setup() 
{
  pinMode(pirPin, INPUT);
  pinMode(flamePin, INPUT);
  pinMode(gasPin, INPUT);
  pinMode(buzzerPin, OUTPUT);

  Serial.begin(9600);
  gsmSerial.begin(9600);
  
  initGSM();
  sendSMS("Device Connected");
}

void loop() 
{
  int pirDetected=digitalRead(pirPin);
  int flameDetected=!digitalRead(flamePin); // Inverse logic.
  int gasDetected=!digitalRead(gasPin);     // Inverse logic.

  if(pirDetected)
  {
     digitalWrite(buzzerPin, HIGH);
     //Serial.println("Motion detected.");
     delay(1000);
  }

  if(flameDetected)
  {
    digitalWrite(buzzerPin, HIGH);
    //Serial.println("Flame detected.");
    delay(1000);
  }

  if(gasDetected)
  {
    digitalWrite(buzzerPin, HIGH);
    //Serial.println("Gas detected.");
    delay(1000);
  }

  if(pirDetected || flameDetected || gasDetected)
  {
    String toSend="";
    
    if(pirDetected)
    {
      toSend+=" Motion Detected!";
    }

    if(flameDetected)
    {
      toSend+=" Flame Detected!";
    }

    if(gasDetected)
    {
      toSend+=" Gas detected!";
      
    }

    Serial.println(toSend);
    sendSMS(toSend);
    toSend="";
    
    digitalWrite(buzzerPin, LOW);
    delay(1000);
  }

}

void initGSM()
{
  while (!gsmSerial.available())
  {
    gsmSerial.println("AT");
    delay(500);
    Serial.println("Connecting...");
  }

  Serial.println("Connected!");

  gsmSerial.println("AT+CMGF=1");
  delay(500);
  gsmSerial.println("AT+CNMI=1,2,0,0,0");
  delay(500);
  gsmSerial.println("AT+CMGL=\"REC UNREAD\"");
  delay(500);
  gsmSerial.println("AT+CMGDA=\"DEL ALL\"");
  delay(500);

  Serial.println("All messages deleted!");

  Serial.println("Sending Text...");

  gsmSerial.println("AT+CMGF=1");
  delay(500);
  
  gsmSerial.print("AT+CMGS=\"+639159793640\"\r");
  delay(500);

  gsmSerial.print("Device Initialized!");
  delay(500);

  gsmSerial.print((char)26);
  delay(500);

  gsmSerial.println();

  Serial.println("Message sent!");
  delay(500);
}

void sendSMS(String text)
{
  Serial.println("Sending Text...");
  
  gsmSerial.println("AT+CMGF=1");
  delay(500);

  gsmSerial.print("AT+CMGS=\"+639159793640\"\r");

  delay(500);

  gsmSerial.print(text);
  delay(500);

  gsmSerial.print((char)26);
  delay(500);

  gsmSerial.println();
  
  Serial.println("Message sent!");
}
