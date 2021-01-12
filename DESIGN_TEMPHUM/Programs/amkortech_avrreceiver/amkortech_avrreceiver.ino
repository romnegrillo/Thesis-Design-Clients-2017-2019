#include <RH_ASK.h>
#include <SPI.h> // Not actualy used but needed to compile

RH_ASK driver; // PIN11

int ledPin=13;

void setup()
{
  pinMode(ledPin,OUTPUT);
  
    Serial.begin(9600); // Debugging only'
    if (!driver.init()) 
    {
      //Serial.println("init failed");
    }
    else
    {
      digitalWrite(ledPin,HIGH);
    }
     
}

void loop()
{
  //Serial.println("test");
    //Serial.println("Test");
    uint8_t buf[5];
    uint8_t buflen = sizeof(buf);
    if (driver.recv(buf, &buflen)) // Non-blocking
    {
      int i;
      // Message with a good checksum received, dump it.
      //Serial.print("Message: ");
      String toSend=(char*)buf;
      toSend=toSend.substring(0,5);
      Serial.println(toSend);       
      //Serial.println(toSend.length());  
      Serial.flush();
    }
    delay(2000);
}
