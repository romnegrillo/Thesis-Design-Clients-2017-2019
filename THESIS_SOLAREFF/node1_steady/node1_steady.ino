#include <RF24.h>
#include <RF24Network.h>
#include <SPI.h>

RF24 radio(7, 8);               // nRF24L01 (CE,CSN)
RF24Network network(radio);      // Include the radio in the network
const uint16_t this_node = 01;   // Address of this node in Octal format ( 04,031, etc)
const uint16_t node00 = 00;
char toSend[24];

const int currentSensorPin = A0;
const int voltageSensorPin = A1;
const int ldrSensorPin = A2;

void setup()
{
  pinMode(currentSensorPin, INPUT);
  pinMode(voltageSensorPin, INPUT);
  pinMode(ldrSensorPin, INPUT);

  Serial.begin(9600);

  SPI.begin();
  radio.begin();
  radio.setPALevel(RF24_PA_MIN);
  network.begin(90, this_node);  //(channel, node address)

}
void loop()
{
  readSendData();
  delay(1000);
}

void readSendData()
{
  network.update();
  RF24NetworkHeader header(node00);     // (Address where the data is going)

  float voltage = getVoltage();
  float current = voltage*10;
  float lux = getLux();

  String message = "node1,";
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
