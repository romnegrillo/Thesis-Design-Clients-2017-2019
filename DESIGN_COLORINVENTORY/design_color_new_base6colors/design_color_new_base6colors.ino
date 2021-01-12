#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
#include <avr/power.h>
#endif

#include <SoftwareSerial.h>


#define PIN        10
#define NUMPIXELS 10 // Popular NeoPixel ring size

Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

#define DELAYVAL 0 // Time (in milliseconds) to pause between pixels
#define SWITCHDELAY 50

const int LDRPins[5] = {A0, A1, A2, A3, A4};
const int numLDR = 5;


const double maxWhite = 700.0;

const int buttonPin = 6;

SoftwareSerial bluetoothSS(8, 7);

void setup()
{

#if defined(__AVR_ATtiny85__) && (F_CPU == 16000000)
  clock_prescale_set(clock_div_1);
#endif
  // END of Trinket-specific code.

  pixels.begin();

  for (int i = 0; i < numLDR; i++)
  {
    pinMode(LDRPins[i], INPUT);
  }

  pinMode(buttonPin, INPUT_PULLUP);

  Serial.begin(9600);
  bluetoothSS.begin(9600);

}

void loop()
{
  getLDRReadings();
}

void getLDRReadings()
{
  String detection = "";
  double redReading, greenReading, blueReading;
  double redPercentage, greenPercentage, bluePercentage;

  for (int i = 0; i < numLDR; i++)
  {
    //Serial.println(i);

    for (int j = 0; j < 1; j++)
    {
      red();
      delay(10);
      redReading = analogRead(LDRPins[i]);
      redPercentage = (redReading / maxWhite) * 100;
      delay(SWITCHDELAY);
    }

    for (int j = 0; j < 1; j++)
    {

      green();
      delay(10);
      greenReading = analogRead(LDRPins[i]);
      greenPercentage = (greenReading / maxWhite) * 100;
      delay(SWITCHDELAY);
    }

    for (int j = 0; j < 1; j++)
    {
      blue();
      delay(10);
      blueReading = analogRead(LDRPins[i]);
      bluePercentage = (blueReading / maxWhite) * 100;
      delay(SWITCHDELAY);
    }
    //
    bluetoothSS.println(i);
    bluetoothSS.println(redPercentage);
    bluetoothSS.println(greenPercentage);
    bluetoothSS.println(bluePercentage);

    int highest = getHighest(redPercentage, greenPercentage, bluePercentage);

    if (i == 0)
    {



      if (redPercentage < 30 &&
          greenPercentage < 30 &&
          bluePercentage < 30)
      {
        detection += "black";
      }
      else if (redPercentage > 45 &&
               greenPercentage > 45 &&
               bluePercentage > 45)
      {
        detection += "white";
      }

      else if (highest == 1)
      {
        if (greenPercentage > 55)
        {
          detection += "orange";
        }
        else
        {
          detection += "red";
        }
      }
      else if (highest == 2)
      {
        detection += "green";
      }
      else if (highest == 3)
      {
        detection += "blue";
      }
      else
      {
        detection += "black";
      }


    }
    else if (i == 1)
    {



      if (redPercentage < 40 &&
          greenPercentage < 40 &&
          bluePercentage < 40)
      {
        detection += "black";
      }
      else if (redPercentage > 45 &&
               greenPercentage > 45 &&
               bluePercentage > 45)
      {
        detection += "white";
      }

      else if (highest == 1)
      {
        if (greenPercentage > 65)
        {
          detection += "orange";
        }
        else
        {
          detection += "red";
        }
      }
      else if (highest == 2)
      {
        detection += "green";
      }
      else if (highest == 3)
      {
        detection += "blue";
      }
      else
      {
        detection += "black";
      }
    }
    else if (i == 2)
    {


      if (redPercentage < 40 &&
          greenPercentage < 40 &&
          bluePercentage < 40)
      {
        detection += "black";
      }
      else if (redPercentage > 45 &&
               greenPercentage > 45 &&
               bluePercentage > 45)
      {
        detection += "white";
      }

      else if (highest == 1)
      {
        if (greenPercentage > 60)
        {
          detection += "orange";
        }
        else
        {
          detection += "red";
        }
      }
      else if (highest == 2)
      {
        detection += "green";
      }
      else if (highest == 3)
      {
        detection += "blue";
      }
      else
      {
        detection += "black";
      }
    }
    else if (i == 3)
    {



      if (redPercentage < 45 &&
          greenPercentage < 45 &&
          bluePercentage < 45)
      {
        detection += "black";
      }
      else if (redPercentage > 60 &&
               greenPercentage > 60 &&
               bluePercentage > 60)
      {
        detection += "white";
      }

      else if (highest == 1)
      {
        if (greenPercentage > 68)
        {
          detection += "orange";
        }
        else
        {
          detection += "red";
        }
      }
      else if (highest == 2)
      {
        detection += "green";
      }
      else if (highest == 3)
      {
        detection += "blue";
      }
      else
      {
        detection += "black";
      }
    }
    else if (i == 4)
    {


      if (redPercentage < 20 &&
          greenPercentage < 20 &&
          bluePercentage < 20)
      {
        detection += "black";
      }
      else if (redPercentage > 30 &&
               greenPercentage > 30 &&
               bluePercentage > 30)
      {
        detection += "white";
      }

      else if (highest == 1)
      {
        if (greenPercentage > 45)
        {
          detection += "orange";
        }
        else
        {
          detection += "red";
        }
      }
      else if (highest == 2)
      {
        detection += "green";
      }
      else if (highest == 3)
      {
        detection += "blue";
      }
      else
      {
        detection += "black";
      }
    }






    if (i != (numLDR - 1))
    {
      detection += ",";
    }



  }

  if (!digitalRead(buttonPin) && detection != "")
  {
    Serial.println(detection);
    bluetoothSS.println(detection);
    delay(1000);
  }
  else
  {
    pixels.clear();
  }
}

void red()
{
  for (int i = 0; i < NUMPIXELS; i++) { // For each pixel...


    pixels.setPixelColor(i, pixels.Color(255, 0, 0));

    pixels.show();   // Send the updated pixel colors to the hardware.

    delay(DELAYVAL); // Pause before next pass through loop
  }
}

void green()
{
  for (int i = 0; i < NUMPIXELS; i++) { // For each pixel...


    pixels.setPixelColor(i, pixels.Color(0, 255, 0));

    pixels.show();   // Send the updated pixel colors to the hardware.

    delay(DELAYVAL); // Pause before next pass through loop
  }
}


void blue()
{
  for (int i = 0; i < NUMPIXELS; i++) { // For each pixel...


    pixels.setPixelColor(i, pixels.Color(0, 0, 255));

    pixels.show();   // Send the updated pixel colors to the hardware.

    delay(DELAYVAL); // Pause before next pass through loop
  }
}


int getHighest(double red, double green, double blue)
{
  if (red > green && red > blue)
  {
    return 1;
  }
  else if (green > red && green > blue)
  {
    return 2;
  }
  else if (blue > green && blue > red)
  {
    return 3;
  }
}
