#include<Servo.h>

const int servoPin=12;
const int leftLDRPin=A7;
const int rightLDRPin=A6;
 
Servo myServo;

bool DEBUG=false;

void setup() 
{
  Serial.begin(9600);
  myServo.attach(servoPin);
  pinMode(leftLDRPin,INPUT);
  pinMode(rightLDRPin, INPUT);
  
  // Set to center.
  myServo.write(90);
  delay(1000);
}

void loop() 
{
   int leftLDRReading=analogRead(leftLDRPin);
   int rightLDRReading=analogRead(rightLDRPin);

   moveServo(leftLDRReading,rightLDRReading);
   
   delay(1000);
}

void moveServo(int leftLDRReading, int rightLDRReading)
{
   int leftRightDifferent=leftLDRReading-rightLDRReading;
   
   if(DEBUG)
   {
      Serial.println("=================");
      Serial.print("Left LDR: ");
      Serial.println(leftLDRReading);
      Serial.print("Right LDR: ");
      Serial.println(rightLDRReading);  
      Serial.print("Left - Right: ");
      Serial.println(leftRightDifferent);
      Serial.println("=================");  
   }

   // Map difference of left and right reading to a corresponding angle in the servo.
       
   float leftLDRReadingV=(leftLDRReading/1023.0)*5.0;
   float rightLDRReadingV=(rightLDRReading/1023.0)*5.0;   

   String toSend=String(leftLDRReadingV)+","+String(rightLDRReadingV);
   Serial.println(toSend);
}

