// Slave Vibration Robot

#include<SoftwareSerial.h>

SoftwareSerial ss(2,3);

// Default move command.
String moveStatus="NONE";

// Motor pins.
const int leftMPin=4;
const int rightMPin=5;

void setup() 
{
  Serial.begin(9600);
  ss.begin(9600);

  pinMode(leftMPin,OUTPUT);
  pinMode(rightMPin,OUTPUT);
}

void loop() 
{
  String toReceive="";
  
  if(ss.available())
  {
    toReceive=ss.readString();
    moveStatus=toReceive;
  }

  //Serial.println(moveStatus);

  if(moveStatus=="UP")
  {
    Serial.println("UP");
    forwardMotor();
  }
  else if(moveStatus=="LEFT")
  {
    Serial.println("LEFT");
    leftMotor();
  }
  else if(moveStatus=="RIGHT")
  {
    Serial.println("RIGHT");
    rightMotor();
  }
  else if(moveStatus=="DOWN")
  {
    Serial.println("DOWN");
  }
  else
  {
    Serial.println("STOP");
    stopMotor();
  }

  delay(10);
}

void forwardMotor()
{
  digitalWrite(leftMPin,HIGH);
  digitalWrite(rightMPin,LOW);

  delay(500);

  digitalWrite(leftMPin,LOW);
  digitalWrite(rightMPin,HIGH);

  delay(500);
}

void leftMotor()
{
  digitalWrite(leftMPin,HIGH);
  digitalWrite(rightMPin,LOW);
}

void rightMotor()
{
  digitalWrite(leftMPin,LOW);
  digitalWrite(rightMPin,HIGH);
}
void stopMotor()
{
  digitalWrite(leftMPin,LOW);
  digitalWrite(rightMPin,LOW);
}

