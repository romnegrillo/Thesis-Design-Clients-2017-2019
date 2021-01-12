#include <SoftwareSerial.h>
#include <TinyGPS.h>

TinyGPS gps;
SoftwareSerial ss(2, 3);
SoftwareSerial gsmSerial(7, 8);  

String lat;
String lon;
String googleLink="http://www.google.com/maps/place/lat,lon";

int buttonPin=A1;

void setup()
{
  pinMode(buttonPin,INPUT_PULLUP);
  
  Serial.begin(9600);
  gsmSerial.begin(9600);

  delay(2000);
  
  initGSM();
  ss.begin(9600);
}

void loop()
{
  bool newData = false;
  unsigned long chars;
  unsigned short sentences, failed;

  // For one second we parse GPS data and report some key values
  for (unsigned long start = millis(); millis() - start < 1000;)
  {
    while (ss.available())
    {
      char c = ss.read();
      // Serial.write(c); // uncomment this line if you want to see the GPS data flowing
      if (gps.encode(c)) // Did a new valid sentence come in?
        newData = true;
    }
  }

  if (newData)
  {
    float flat, flon;
    unsigned long age;
    gps.f_get_position(&flat, &flon, &age);

    lat=String(flat == TinyGPS::GPS_INVALID_F_ANGLE ? 0.0 : flat, 6);
    lon=String(flon == TinyGPS::GPS_INVALID_F_ANGLE ? 0.0 : flon, 6);
    googleLink.replace("lat",lat);
    googleLink.replace("lon",lon);
    
    Serial.println(lat);
    Serial.println(lon);
    Serial.println(googleLink);

    String toSend="Help, I'm in the location: "+googleLink;
    gsmSerial.listen();
    sendSMS(toSend);
    ss.listen();
  }

  if(!digitalRead(buttonPin))
  {
      // Removed.
  }
  
//  gps.stats(&chars, &sentences, &failed);
//  Serial.print(" CHARS=");
//  Serial.print(chars);
//  Serial.print(" SENTENCES=");
//  Serial.print(sentences);
//  Serial.print(" CSUM ERR=");
//  Serial.println(failed);
//  if (chars == 0)
//    Serial.println("** No characters received from GPS: check wiring **");

delay(1000);
}

void sendSMS(String text)
{

  /////////////////////////////////////////////////////////////
  
  Serial.println("Sending Text...");
  gsmSerial.println("AT+CMGF=1");
  delay(1000);

  gsmSerial.print("AT+CMGS=\"+639165737387\"\r");
  //gsmSerial.print("AT+CMGS=\"+639776811077\"\r");
  
  delay(1000);

  gsmSerial.print(text);
  delay(1000);

  gsmSerial.print((char)26);
  delay(1000);

  gsmSerial.println();
  Serial.println("Message sent!");
  delay(1000);

  ///////////////////////////////////////////////////////////

}

void initGSM()
{
  while (!gsmSerial.available())
  {
    gsmSerial.println("AT");
    delay(500);
    Serial.println("Connecting...");
  }

  Serial.println("Connected!");

  gsmSerial.println("AT+CMGF=1");
  delay(500);
  gsmSerial.println("AT+CNMI=1,2,0,0,0");
  delay(500);
  gsmSerial.println("AT+CMGL=\"REC UNREAD\"");
  delay(500);
  gsmSerial.println("AT+CMGDA=\"DEL ALL\"");
  delay(500);

  Serial.println("All messages deleted!");

  Serial.println("Sending Text...");

  gsmSerial.println("AT+CMGF=1");
  delay(500);

  gsmSerial.print("AT+CMGS=\"+639165737387\"\r");
  //gsmSerial.print("AT+CMGS=\"+639776811077\"\r");
  
  delay(500);

  gsmSerial.print("Umbrella Device Initialized!");
  delay(500);

  gsmSerial.print((char)26);
  delay(500);

  gsmSerial.println();

  Serial.println("Message sent!");
  delay(500);
}
