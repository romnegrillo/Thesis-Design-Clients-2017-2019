#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include "AS726X.h"

AS726X sensor;

#ifndef APSSID
#define APSSID "THESIS_GLUCOSE"
#define APPSK  "thesis_glucose"
#endif


/* Set these to your desired credentials. */
const char *ssid = APSSID;
const char *password = APPSK;

// Socket
int port = 8888;  //Port number
WiFiServer server(port);

// For testing only.
int ctr = 0;


void setup()
{
  delay(1000);
  
  Serial.begin(9600);

  Serial.println("Initializing...");

  Wire.begin(D2, D1);
  
  sensor.begin();
  sensor.disableBulb();




  Serial.println();
  Serial.print("Configuring access point...");
  /* You can remove the password parameter if you want the AP to be open. */
  WiFi.softAP(ssid, password);

  IPAddress myIP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(myIP);

  server.begin();

}

void loop()
{

  WiFiClient client = server.available();


  if (client) {

    while (client.connected()) {

      sensor.enableBulb();

      Serial.println("Client connected!");
      sensor.takeMeasurements();

      if (sensor.getVersion() == SENSORTYPE_AS7263)
      {
        //Near IR readings
        //    Serial.print(" Reading: R[");
        //    Serial.print(sensor.getCalibratedR(), 2);
        //    Serial.print("] S[");
        //    Serial.print(sensor.getCalibratedS(), 2);
        //    Serial.print("] T[");
        //    Serial.print(sensor.getCalibratedT(), 2);
        //    Serial.print("] U[");
        //    Serial.print(sensor.getCalibratedU(), 2);
        //    Serial.print("] V[");
        //    Serial.print(sensor.getCalibratedV(), 2);
        //    Serial.print("] W[");
        //    Serial.print(sensor.getCalibratedW(), 2);

        String data = String(sensor.getCalibratedR());

        Serial.println(data);
        client.println(data);
      }

      //      // Testing for receiving from client.
      //      while (client.available() > 0) {
      //        char c = client.read();
      //        Serial.write(c);
      //      }
      //
      //      while (Serial.available() > 0)
      //      {
      //        client.println(Serial.readString());
      //      }
      //
      //
      //      client.println(ctr);
      //      Serial.println(ctr);
      //      ctr++;



      delay(1000);

    }

    delay(1000);

    sensor.disableBulb();
    client.stop();

    Serial.println("Client disconnected");
  }

}
