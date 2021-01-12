#include "DHT.h"
#define DHTPIN 2
#define DHTTYPE DHT11
#include <Servo.h>

DHT dht(DHTPIN, DHTTYPE);

const int mq2Pin=A0;
const int servoPin=3;

Servo myServo;

void setup() 
{
   Serial.begin(9600);
   dht.begin();
   myServo.attach(servoPin);
   myServo.write(0);
   delay(5000);

   pinMode(mq2Pin, INPUT);
}

void loop() 
{
  float temp=dht.readTemperature();
  float smoke=analogRead(mq2Pin);
  fuzzifyAndDefuzzify(temp,smoke);

  delay(1000);
}

void fuzzifyAndDefuzzify(float temp, float smoke)
{
  /* Rules
   * if temp is LOW and smoke is LOW then fan speed is STOP
   * if temp is MEDIUM and smoke is LOW then fan speed is MEDIUM LOW
   * if temp is HIGH and smoke is LOW then fan speed is MEDIUM LOW
   * 
   * if temp is LOW and smoke is MEDIUM then fan speed is MEDIUM HIGH
   * if temp is MEDIUM and smoke is MEDIUM then fan speed is MEDIUM HIGH
   * if temp is HIGH and smoke is MEDIUM then fan speed is MEDIUM HIGH
   * 
   * if temp is LOW and smoke is HIGH then fan speed is MEDIUM HIGH
   * if temp is MEDIUM and smoke is HIGH then fan speed is MEDIUM HIGH
   * if temp is HIGH and smoke is HIGH then fan speed is HIGH
   * 
   * 
   * MAP servo to 5 outputs depending on the angle.
   * 0 degrees = STOP
   * 45 degrees = MEDIUM LOW
   * 135 degrees = MEDIUM HIGH
   * 180 degrees= HIGH
   * 
   * LOW temp = 0-20 deg
   * MEDIUM temp = 21-35 deg
   * HIGH temp = >35 deg
   * 
   * 750 is the analog reading for no smoke.
   * LOW smoke = 0-800
   * MEDIUM smoke = 800-900
   * HIGH smoke = 900-1023
   */
  
  
  String tempFuzz="";
  String smokeFuzz="";
  String fanspeedFuzz="";
  
  if(temp>=0 && temp<=20)
  {
    tempFuzz="LOW";
  }
  else if(temp>=21 && temp<=35)
  {
    tempFuzz="MEDIUM";
  }
  else if(temp>35)
  {
    tempFuzz="HIGH";
  }

  // ===============================
  
  if ((smoke>=0 && smoke<800))
  {
    smokeFuzz="LOW";
  }
  else if(smoke>=800 && smoke <900)
  {
    smokeFuzz="MEDIUM";
  }
  else if(smoke>=900)
  {
    smokeFuzz="HIGH";
  }

  // Map to outputs

  if(tempFuzz=="LOW" && smokeFuzz=="LOW")
  {
    myServo.write(0);
    fanspeedFuzz="STOP";
  }
  else if(tempFuzz=="MEDIUM" && smokeFuzz=="LOW")
  {
    myServo.write(45);
    fanspeedFuzz="MEDIUM LOW";
  }
  else if(tempFuzz=="HIGH" && smokeFuzz=="LOW")
  {
     myServo.write(45);
    fanspeedFuzz="MEDIUM LOW";
  }
    else if(tempFuzz=="LOW" && smokeFuzz=="MEDIUM")
  {
    myServo.write(135);
    fanspeedFuzz="MEDIUM HIGH";
  }
    else if(tempFuzz=="MEDIUM" && smokeFuzz=="MEDIUM")
  {
    myServo.write(135);
        fanspeedFuzz="MEDIUM HIGH";
  }
    else if(tempFuzz=="HIGH" && smokeFuzz=="MEDIUM")
  {
    myServo.write(135);
        fanspeedFuzz="MEDIUM HIGH";
  }
  else if(tempFuzz=="LOW" && smokeFuzz=="HIGH")
  {
    myServo.write(135);
        fanspeedFuzz="MEDIUM HIGH";
  }
  else if(tempFuzz=="MEDIUM" && smokeFuzz=="HIGH")
  {
    myServo.write(135);
        fanspeedFuzz="MEDIUM HIGH";
  }
  else if(tempFuzz=="HIGH" && smokeFuzz=="HIGH")
  {
    myServo.write(180);
        fanspeedFuzz="HIGH";
  }

  String toPrint="";
  toPrint+=String(temp);
  toPrint+=",";
  toPrint+=tempFuzz;
  toPrint+=",";
  toPrint+=String(smoke);
  toPrint+=",";
  toPrint+=smokeFuzz;
  toPrint+=",";
  toPrint+=fanspeedFuzz;

  Serial.println(toPrint);
}

