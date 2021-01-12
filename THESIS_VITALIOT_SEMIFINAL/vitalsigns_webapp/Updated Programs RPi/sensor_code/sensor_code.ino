#include <Wire.h>
#include "Protocentral_MAX30205.h"
MAX30205 tempSensor;

const int ecgPin = A0;
int delayInterval = 1000;

#include "Adafruit_FONA.h"

#define FONA_RX 2
#define FONA_TX 3
#define FONA_RST 4
char replybuffer[255];

#include <SoftwareSerial.h>
SoftwareSerial fonaSS = SoftwareSerial(FONA_TX, FONA_RX);
SoftwareSerial *fonaSerial = &fonaSS;

Adafruit_FONA fona = Adafruit_FONA(FONA_RST);

uint8_t readline(char *buff, uint8_t maxbuff, uint16_t timeout = 0);

uint8_t type;
float latitudeCoordinate = 0.0;
float longitudeCoordinate = 0.0;


void setup()
{
  Wire.begin();
  Serial.begin(9600);
  tempSensor.begin();
  pinMode(ecgPin, INPUT);

  fonaSerial->begin(9600);
  if (! fona.begin(*fonaSerial)) {
    Serial.println(F("Couldn't find FONA"));
    while (1);
  }

  type = fona.type();
  Serial.println(F("FONA is OK"));
  Serial.print(F("Found "));

  setAudioInOut();
  setVolume();

  turnGPSOn();
  getGPSData();
  flushSerial();
}

void loop()
{
  if (Serial.available())
  {
    String data = Serial.readStringUntil("\n");

    if (data == "1\r\n")
    {
      // Slow interval for reading temperature.
      delayInterval = 1000;
      ;
    }
    else if (data == "2\r\n")
    {
      // Fast Interval for reading ECG data.
      delayInterval = 100;

    }
    else if (data.startsWith("3"))
    {
      Serial.println("Start a call.");

      // Format 3,+639171709038
      // Index 2-15
      String number = data.substring(2,16);
      
      endDoctorCall();
      delay(200);
      startDoctorCall(number);

    }
    else if (data == "4\r\n")
    {
      Serial.println("End a call.");

    }
   
  }

  // Send pattern: X,tempData,ecgData,lat,lon

  float temp = tempSensor.getTemperature();
  int ecgData = analogRead(ecgPin);
  
//  getGPSData();
//  delay(100);

  String toSend = "XFLAG";
  toSend += ",";
  toSend += String(temp);
  toSend += ",";
  toSend += String(ecgData);
  toSend += ",";
  toSend += String(latitudeCoordinate);
  toSend += ",";
  toSend += String(longitudeCoordinate);

  Serial.println(toSend);

  delay(delayInterval);
}

void startDoctorCall(String numberString)
{

  
 
  char numberChar[14];


  numberString.toCharArray(numberChar, 14);

  Serial.println("Number char: ");
  Serial.println(numberChar);
 

  flushSerial();

  if (!fona.callPhone(numberChar)) {
    Serial.println(F("Can't start the call."));
  } else {
    Serial.println(F("Call started!"));
  }
}

void endDoctorCall()
{
  if (! fona.hangUp()) {
    Serial.println(F("Already hunged up."));
  } else {
    Serial.println(F("Hung up success."));
  }
}

void readMessages()
{
  // Read SMS
  int8_t smsnum = fona.getNumSMS();
  uint16_t smslen;
  int8_t smsn;

  if ( (type == FONA3G_A) || (type == FONA3G_E) ) {
    smsn = 0; // zero indexed
    smsnum--;
  } else {
    smsn = 1;  // 1 indexed
  }

  for ( ; smsn <= smsnum; smsn++) {
    Serial.print(F("\n\rReading SMS #")); Serial.println(smsn);
    if (!fona.readSMS(smsn, replybuffer, 250, &smslen)) {  // pass in buffer and max len!
      Serial.println(F("Failed!"));
      break;
    }
    // if the length is zero, its a special case where the index number is higher
    // so increase the max we'll look at!
    if (smslen == 0) {
      Serial.println(F("[empty slot]"));
      smsnum++;
      continue;
    }

    Serial.print(F("***** SMS #")); Serial.print(smsn);
    Serial.print(" ("); Serial.print(smslen); Serial.println(F(") bytes *****"));
    Serial.println(replybuffer);
    Serial.println(F("*****"));
  }
}

void getGPSData()
{
  //  char gpsdata[120];
  //  fona.getGPS(0, gpsdata, 120);
  //
  //  Serial.println(gpsdata);

  float latitude, longitude, speed_kph, heading, speed_mph, altitude;

  // if you ask for an altitude reading, getGPS will return false if there isn't a 3D fix
  boolean gps_success = fona.getGPS(&latitude, &longitude, &speed_kph, &heading, &altitude);

  if (gps_success) {

//    Serial.print("GPS lat:");
//    Serial.println(latitude, 6);
//    Serial.print("GPS long:");
//    Serial.println(longitude, 6);

    latitudeCoordinate = latitude;
    longitudeCoordinate = longitude;

    Serial.println("Coordinates: ");
    Serial.println(latitudeCoordinate);
    Serial.println(longitudeCoordinate);

    Serial.println("GPS 3D fixed.");

  } else {
    Serial.println("Waiting for FONA GPS 3D fix...");
  }
}

void setVolume()
{
  if (! fona.setVolume(100)) {
    Serial.println(F("Failed to set volume"));

  } else {

    Serial.println(F("Volume set to max."));
  }
}

void setAudioInOut()
{
  if (! fona.setAudio(FONA_HEADSETAUDIO)) {
    Serial.println(F("Failed to select headphone mode."));
  } else {
    Serial.println(F("Headphone mode selected."));
  }
  fona.setMicVolume(FONA_HEADSETAUDIO, 100);
}

void turnGPSOn()
{
  if (!fona.enableGPS(true))
    Serial.println(F("Failed to turn on"));
  else
    Serial.println("GPS turned on.");
}


void flushSerial() {
  while (Serial.available())
    Serial.read();
}
