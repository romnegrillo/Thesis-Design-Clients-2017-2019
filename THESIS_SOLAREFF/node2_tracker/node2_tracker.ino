#include <RF24.h>
#include <RF24Network.h>
#include <SPI.h>
#include <Servo.h>  

// 180 horizontal MAX
Servo horizontal; // horizontal servo
int servoh = 180;   // 90;     // stand horizontal servo

int servohLimitHigh = 180;
int servohLimitLow = 65;

// 65 degrees MAX
Servo vertical;   // vertical servo 
int servov = 45;    //   90;     // stand vertical servo

int servovLimitHigh = 80;
int servovLimitLow = 15;


// LDR pin connections
//  name  = analogpin;
int ldrlt = 0; //LDR top left - BOTTOM LEFT    <--- BDG
int ldrrt = 1; //LDR top rigt - BOTTOM RIGHT 
int ldrld = 2; //LDR down left - TOP LEFT
int ldrrd = 3; //ldr down rigt - TOP RIGHT

RF24 radio(7, 8);               // nRF24L01 (CE,CSN)
RF24Network network(radio);      // Include the radio in the network
const uint16_t this_node = 02;   // Address of this node in Octal format ( 04,031, etc)
const uint16_t node00 = 00;
char toSend[24];

const int currentSensorPin = A4;
const int voltageSensorPin = A5;
const int ldrSensorPin = A6;

void setup()
{
    pinMode(currentSensorPin, INPUT);
  pinMode(voltageSensorPin, INPUT);
  pinMode(ldrSensorPin, INPUT);

  SPI.begin();
  radio.begin();
  radio.setPALevel(RF24_PA_MIN);
  network.begin(90, this_node);  //(channel, node address)
  
  Serial.begin(9600);
// servo connections
// name.attacht(pin);
  horizontal.attach(6); 
  vertical.attach(10);
  
  horizontal.write(90);
  vertical.write(45);

  delay(1000);
}

void loop() 
{
    readSendData();
    
  int lt = analogRead(ldrlt); // top left
  int rt = analogRead(ldrrt); // top right
  int ld = analogRead(ldrld); // down left
  int rd = analogRead(ldrrd); // down rigt
  
  // int dtime = analogRead(4)/20; // read potentiometers  
  // int tol = analogRead(5)/4;
  int dtime = 10;
  int tol = 50;
  
  int avt = (lt + rt) / 2; // average value top
  int avd = (ld + rd) / 2; // average value down
  int avl = (lt + ld) / 2; // average value left
  int avr = (rt + rd) / 2; // average value right

  int dvert = avt - avd; // check the diffirence of up and down
  int dhoriz = avl - avr;// check the diffirence og left and rigt
  
  
 
  
    
  if (-1*tol > dvert || dvert > tol) // check if the diffirence is in the tolerance else change vertical angle
  {
  if (avt > avd)
  {
    servov = ++servov;
     if (servov > servovLimitHigh) 
     { 
      servov = servovLimitHigh;
     }
  }
  else if (avt < avd)
  {
    servov= --servov;
    if (servov < servovLimitLow)
  {
    servov = servovLimitLow;
  }
  }
  vertical.write(servov);
  }
  
  if (-1*tol > dhoriz || dhoriz > tol) // check if the diffirence is in the tolerance else change horizontal angle
  {
  if (avl > avr)
  {
    servoh = --servoh;
    if (servoh < servohLimitLow)
    {
    servoh = servohLimitLow;
    }
  }
  else if (avl < avr)
  {
    servoh = ++servoh;
     if (servoh > servohLimitHigh)
     {
     servoh = servohLimitHigh;
     }
  }
  else if (avl = avr)
  {
    // nothing
  }
  horizontal.write(servoh);
  }
   delay(1000);
}

void readSendData()
{
  network.update();
  RF24NetworkHeader header(node00);     // (Address where the data is going)
  
  float voltage = getVoltage();
  float current = voltage*10;
  float lux = getLux();

  String message = "node2,";
  message += String(current);
  message += ",";
  message += String(voltage);
  message += ",";
  message += String(lux);
  message.toCharArray(toSend, 24);

  bool ok = network.write(header, &toSend, sizeof(toSend)); // Send the data
  Serial.println(message);

  if (ok)
  {
    Serial.println("Message sent.");
  }
  else
  {
    Serial.println("Message not sent.");
  }
}

float getCurrent()
{
  // 2A ACS712 have a sensitivity of 100mV/1A.

  float reading = analogRead(currentSensorPin);
  float acsOffset = 0.0;

  float current = (reading * (5000.0 / 1023.0) - acsOffset) * (1 / 100);
  //float current = (reading);
  return current;
}

float getVoltage()
{
  // Sensor is just a voltage divider.

  float reading = analogRead(voltageSensorPin);
  float R1 = 30000;
  float R2 = 7500;

  float voltage = reading * (5.0 / 1023.0) * ((R1 + R2) / R2);

  return voltage;
}

float getLux()
{
  // 5V-LDR-3.3k-Gnd

  float reading = analogRead(ldrSensorPin);

  float voltageReading = reading * (5.0 / 1023.0);
 
  float lux = (250.0 / voltageReading) - 50.0;  

  return lux;
}
