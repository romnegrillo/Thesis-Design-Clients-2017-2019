#include <RF24.h>
#include <RF24Network.h>
#include <SPI.h>

RF24 radio(7, 8);                // nRF24L01 (CE,CSN)
RF24Network network(radio);      // Include the radio in the network
const uint16_t this_node = 00;   // Address of our node in Octal format ( 04,031, etc)

char toReceive[24];

void setup() 
{
  Serial.begin(9600);
  
  SPI.begin();
  radio.begin();
   radio.setPALevel(RF24_PA_MAX);
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

    Serial.println(toReceive);
  }
}
