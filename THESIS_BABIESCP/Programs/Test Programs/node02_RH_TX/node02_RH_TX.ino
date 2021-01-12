#include <RF24.h>
#include <RF24Network.h>
#include <SPI.h>

RF24 radio(7, 8);               // nRF24L01 (CE,CSN)
RF24Network network(radio);      // Include the radio in the network
const uint16_t this_node = 02;   // Address of this node in Octal format ( 04,031, etc)
const uint16_t node00 = 00;      
char toSend[24];

void setup() 
{
  Serial.begin(9600);
  SPI.begin();
  radio.begin();
  network.begin(90, this_node);  //(channel, node address)
}
void loop() 
{
  network.update();
  RF24NetworkHeader header(node00);     // (Address where the data is going)

  String message="Hello";
  message=String(this_node)+message;
  
  message.toCharArray(toSend,24);
  
  bool ok = network.write(header, &toSend, sizeof(toSend)); // Send the data

  if(ok)
  {
    Serial.println("Message sent.");
  }
  else
  {
    Serial.println("Message failed.");
  }

  delay(1000);
}
