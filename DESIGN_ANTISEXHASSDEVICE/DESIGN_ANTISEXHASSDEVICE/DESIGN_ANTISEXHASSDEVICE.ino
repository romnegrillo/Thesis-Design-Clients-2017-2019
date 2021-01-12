// Libraries used.
#include <SoftwareSerial.h>
#include <TinyGPS.h>
#include <LiquidCrystal_I2C.h>
#include <Keypad.h>

// Pins for pulse rate.
const int pulsePin = A0;
int heartRate;

// Object for bluetooth.
SoftwareSerial bluetoothSS(2, 3);

// Objects and variables for GPS.
TinyGPS gps;
SoftwareSerial gpsSS(4, 5);
String lat = "0", lon = "0";
bool gpsConnected = false;
String toSend;

// Variables for button and buzzer.
const int buzzPin = A4;
const int buttonPin = A5;

// Variable to keep track how long the response
// is received from the bluetooth.
unsigned long startTime;

// For keypad.

const byte ROWS = 4; //four rows
const byte COLS = 4; //four columns
//define the cymbols on the buttons of the keypads
char hexaKeys[ROWS][COLS] = {
  {'d', '#', '0', '*'},
  {'C', '9', '8', '7'},
  {'B', '6', '5', '4'},
  {'A', '3', '2', '1'}
};

byte rowPins[ROWS] = {9, 8, 7, 6}; //connect to the row pinouts of the keypad
byte colPins[COLS] = {13, 12, 11, 10}; //connect to the column pinouts of the keypad

//initialize an instance of class NewKeypad
Keypad customKeypad = Keypad( makeKeymap(hexaKeys), rowPins, colPins, ROWS, COLS);

String passTarget = "3A6B";
String passInput = "";

bool isSent=false;

void setup()
{
  pinMode(buzzPin, OUTPUT);
  pinMode(buttonPin, INPUT_PULLUP);

  Serial.begin(9600);
  bluetoothSS.begin(9600);
  gpsSS.begin(9600);

  while (!gpsConnected)
  {
    getLatLon();

    Serial.println("Connecting to GPS...");

    // Bypass GPS for testing.
    if (!digitalRead(buttonPin))
    {
      digitalWrite(buzzPin, HIGH);
      delay(1000);
      digitalWrite(buzzPin, LOW);
      break;
    }
  }
  
  Serial.println("GPS connected!");

  bluetoothSS.listen();
}

void loop()
{
  int bpm = getPulse();
  //Serial.println(bpm);

  if (bpm > 150 && !startTime)
  {
    // Update GPS connection.
    //getLatLon();

    toSend = "";
    toSend += lat;
    toSend += ",";
    toSend += lon;

    //Serial.println(toSend);
    bluetoothSS.println(toSend);
  }

  if(checkBluetoothResponse())
{
  // Check time for response. If is more than 10 seconds
  // since an alerts is received, send GPS  data.
  while(1)
  {
  if (((millis() - startTime) > 10000) && startTime != 0)
  {
    //Serial.println("Debug");

    // Update GPS connection.
    //getLatLon();

    toSend = "";
    toSend += lat;
    toSend += ",";
    toSend += lon;

    Serial.println(toSend);
    bluetoothSS.println(toSend);

    isSent=true;
    startTime = 0;

    delay(1000);
  }

  // Turnoff buzzer when button a specific code is pressed.

  char customKey = customKeypad.getKey();

  if (customKey)
  {

    if (customKey == '*')
    {
      passInput = "";
    }
    else
    {

      passInput += customKey;

      Serial.print("Pass input: ");
      Serial.println(passInput);

      if (passInput == passTarget)
      {
        passInput = "";

        Serial.println("Timer stopped.");
        digitalWrite(buzzPin, LOW);
        startTime = 0;
        bluetoothSS.flush();
        break;
      }
    }
  }
  }
}

  delay(500);
}

int getPulse()
{
  heartRate = analogRead(pulsePin);
  heartRate = map(heartRate, 0, 1023, 0, 200);

  return heartRate;
}

void getLatLon()
{
  gpsSS.listen();

  bool newData = false;
  unsigned long chars;
  unsigned short sentences, failed;

  // For one second we parse GPS data and report some key values
  for (unsigned long start = millis(); millis() - start < 1000;)
  {
    while (gpsSS.available())
    {
      char c = gpsSS.read();
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
    lat = flat == TinyGPS::GPS_INVALID_F_ANGLE ? 0.0 : flat, 6;
    lon = flon == TinyGPS::GPS_INVALID_F_ANGLE ? 0.0 : flon, 6;
    gpsConnected = true;
  }
}

bool checkBluetoothResponse()
{
  bluetoothSS.listen();

  if (bluetoothSS.available())
  {
    String message = bluetoothSS.readString();

    Serial.print("From bluetooth: ");
    Serial.println(message);

    if (message == "ALERTSMS")
    {
      Serial.println("Timer started.");
      digitalWrite(buzzPin, HIGH);
      startTime = millis();
      return true;
    }
  }

  return false;
}

