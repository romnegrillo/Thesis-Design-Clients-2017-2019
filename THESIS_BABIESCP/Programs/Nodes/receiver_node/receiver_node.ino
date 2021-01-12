#include <RF24.h>
#include <RF24Network.h>
#include <SPI.h>


RF24 radio(7, 8);                // nRF24L01 (CE,CSN)
RF24Network network(radio);      // Include the radio in the network
const uint16_t this_node = 00;   // Address of our node in Octal format ( 04,031, etc)

long accelX, accelY, accelZ;
float gForceX, gForceY, gForceZ;

long gyroX, gyroY, gyroZ;
float rotX, rotY, rotZ;

const int maxChar=24;
char toReceive[maxChar];
int receiveCtr=0;

String toBluetooth;

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

    String dataIn=String(toReceive);

   // Serial.println(dataIn);
    
    //Serial.println(dataIn);
    
    if(dataIn.indexOf("NODE1")>-1 && receiveCtr==0)
    {
       receiveCtr++;
       toBluetooth+=dataIn;
       toBluetooth+=",";
       
    }
    else if((dataIn.indexOf("NODE2")>-1)  && receiveCtr==1)
    {
      receiveCtr++;
      toBluetooth+=dataIn;
      toBluetooth+=",";
    }
    else if((dataIn.indexOf("NODE3")>-1)  && receiveCtr==2)
    {
       receiveCtr++;
       toBluetooth+=dataIn;
       toBluetooth+=",";
    }

    else if((dataIn.indexOf("NODE4")>-1)  && receiveCtr==3)
    {
       toBluetooth+=dataIn;
       toBluetooth+=",";
      //Serial.println("Data complete.");
      Serial.println(toBluetooth);

      
      toBluetooth="";
      receiveCtr=0;
    }
  }

  delay(300);
}
