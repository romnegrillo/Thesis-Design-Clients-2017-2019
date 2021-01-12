#include <Wire.h>
#include "Protocentral_MAX30205.h"
MAX30205 tempSensor;

const int ECGPin = A0;

void setup()
{
  pinMode(ECGPin, INPUT);
  Wire.begin();
  Serial.begin(9600);
  tempSensor.begin();   // set continuos mode, active mode
}

void loop() {

  float temp = tempSensor.getTemperature(); // read temperature for every 100ms
  float ECGValue = analogRead(ECGPin);
  String toSend;

  toSend+=String(temp);
  toSend+=",";
  toSend+=String(ECGValue);
  
  Serial.println(toSend);
  
  delay(1000);
}
