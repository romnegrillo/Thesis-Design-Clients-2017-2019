#include <RF24.h>
#include <RF24Network.h>
#include <SPI.h>
#include <Wire.h>
#include <SoftwareSerial.h>

RF24 radio(7, 8);                // nRF24L01 (CE,CSN)
RF24Network network(radio);      // Include the radio in the network
const uint16_t this_node = 00;   // Address of our node in Octal format ( 04,031, etc)

const int maxChar = 24;
char toReceive[maxChar];
int ctr = 0;

String toSend = "";

void setup()
{
  Serial.begin(9600);

  SPI.begin();
  radio.begin();
  radio.setPALevel(RF24_PA_MIN);
  network.begin(90, this_node); //(channel, node address)

}

void loop()
{

  network.update();

  // Is there any incoming data?
  while (network.available())
  {
    RF24NetworkHeader header;
    network.read(header, &toReceive, sizeof(toReceive)); // Read the incoming data

    String dataIn = String(toReceive);

    if (dataIn.indexOf("node1") > -1 && ctr == 0)
    {
      toSend += dataIn;
      toSend += ",";
      ctr++;
    }
    else if (dataIn.indexOf("node2") > -1 && ctr == 1)
    {
      toSend += dataIn;
      toSend += ",";
      ctr++;
    }
    else if (dataIn.indexOf("node3") > -1 && ctr == 2)
    {
      toSend += dataIn;
      toSend += ",";
      ctr++;
    }
    else if (dataIn.indexOf("node4") > -1 && ctr == 3)
    {
      toSend += dataIn;
      ctr++;
    }

    if (ctr == 4)
    {
      Serial.println(toSend);
      toSend="";
      ctr = 0;
    }

    Serial.println(ctr);
  }

  delay(1000);
}
