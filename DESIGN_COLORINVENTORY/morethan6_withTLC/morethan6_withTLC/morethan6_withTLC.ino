#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
#include <avr/power.h>
#endif

#include <SoftwareSerial.h>


#define PIN        10
#define NUMPIXELS 10 // Popular NeoPixel ring size

Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);
#include "Tlc5940.h"

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

  // Initialize TLC.
  Tlc.init(0);

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
        TLCBlack(i);
      }
      else if (redPercentage > 45 &&
               greenPercentage > 45 &&
               bluePercentage > 45)
      {
        if (redPercentage > 60)
        {
          detection += "white";
          TLCWhite(i);
        }
        else
        {
          detection += "gray";
          TLCGray(i);
        }
      }

      else if (highest == 1)
      {
        if (greenPercentage > 55)
        {
          detection += "orange";
          TLCOrange(i);
        }
        else if (redPercentage < 51)
        {
          detection += "purple";
          TLCPurple(i);
        }
        else
        {
          detection += "red";
          TLCRed(i);
        }
      }
      else if (highest == 2)
      {
        if(greenPercentage<40)
        {
          detection += "purple";
        }
        else if (redPercentage > 25 )
        {
          detection += "lime";
          TLCLime(i);
        }
        else
        {
          detection += "green";
          TLCGreen(i);
        }
      }
      else if (highest == 3)
      {
        detection += "blue";
        TLCBlue(i);
      }
      else
      {
        detection += "black";
        TLCBlack(i);
      }


    }
    else if (i == 1)
    {



      if (redPercentage < 40 &&
          greenPercentage < 40 &&
          bluePercentage < 40)
      {
        detection += "black";
        TLCBlack(i);
      }
      else if (redPercentage > 45 &&
               greenPercentage > 45 &&
               bluePercentage > 45)
      {
        if (redPercentage > 80)
        {
          detection += "white";
          TLCWhite(i);
        }
        else
        {
          detection += "gray";
          TLCGray(i);
        }
      }

      else if (highest == 1)
      {
        if (greenPercentage > 65)
        {
          detection += "orange";
          TLCOrange(i);
        }
        else if (redPercentage < 78)
        {
          detection += "purple";
          TLCPurple(i);
        }
        else
        {
          detection += "red";
          TLCRed(i);
        }
      }
      else if (highest == 2)
      {
        if (redPercentage > 35 )
        {
          detection += "lime";
          TLCLime(i);
        }
        else
        {
          detection += "green";
          TLCGreen(i);
        }
      }
      else if (highest == 3)
      {
        detection += "blue";
        TLCBlue(i);
      }
      else
      {
        detection += "black";
        TLCBlack(i);
      }
    }
    else if (i == 2)
    {


      if (redPercentage < 40 &&
          greenPercentage < 40 &&
          bluePercentage < 40)
      {
        detection += "black";
        TLCBlack(i);
      }
      else if (redPercentage > 45 &&
               greenPercentage > 45 &&
               bluePercentage > 45)
      {
        if (redPercentage > 90)
        {
          detection += "white";
          TLCWhite(i);
        }
        else
        {
          detection += "gray";
          TLCGray(i);
        }
      }

      else if (highest == 1)
      {
        if (greenPercentage > 60)
        {
          detection += "orange";
          TLCOrange(i);
        }
        else if (redPercentage < 81)
        {
          detection += "purple";
          TLCPurple(i);
        }
        else
        {
          detection += "red";
          TLCRed(i);
        }
      }
      else if (highest == 2)
      {
        if (redPercentage > 50 )
        {
          detection += "lime";
          TLCLime(i);
        }
        else
        {
          detection += "green";
          TLCGreen(i);
        }
      }
      else if (highest == 3)
      {
        detection += "blue";
        TLCBlue(i);
      }
      else
      {
        detection += "black";
        TLCBlack(i);
      }
    }
    else if (i == 3)
    {



      if (redPercentage < 45 &&
          greenPercentage < 45 &&
          bluePercentage < 45)
      {
        detection += "black";
        TLCBlack(i);
      }
      else if (redPercentage > 60 &&
               greenPercentage > 60 &&
               bluePercentage > 60)
      {
        if (redPercentage > 90)
        {
          detection += "white";
          TLCWhite(i);
        }
        else
        {
          detection += "gray";
          TLCGray(i);
        }
      }

      else if (highest == 1)
      {
        if (greenPercentage > 68)
        {
          detection += "orange";
          TLCOrange(i);
        }
        else if (redPercentage < 91)
        {
          detection += "purple";
          TLCPurple(i);
        }
        else
        {
          detection += "red";
          TLCRed(i);
        }
      }
      else if (highest == 2)
      {
        if (redPercentage > 50 )
        {
          detection += "lime";
          TLCLime(i);
        }
        else
        {
          detection += "green";
          TLCGreen(i);
        }
      }
      else if (highest == 3)
      {
        detection += "blue";
        TLCBlue(i);
      }
      else
      {
        detection += "black";
        TLCBlack(i);
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
        if (redPercentage > 50)
        {
          detection += "white";
          TLCWhite(i);
        }
        else
        {
          detection += "gray";
          TLCGray(i);
        }
      }

      else if (highest == 1)
      {
        if (greenPercentage > 45)
        {
          detection += "orange";
          TLCOrange(i);
        }
        else if (redPercentage < 40)
        {
          detection += "purple";
          TLCPurple(i);
        }
        else
        {
          detection += "red";
          TLCRed(i);
        }
      }
      else if (highest == 2)
      {
        if (redPercentage > 20 )
        {
          detection += "lime";
          TLCLime(i);
        }
        else
        {
          detection += "green";
          TLCGreen(i);
        }
      }
      else if (highest == 3)
      {
        detection += "blue";
        TLCBlue(i);
      }
      else
      {
        detection += "black";
        TLCBlack(i);
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
    TLCClear();
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

void TLCBlack(int ledCount)
{
  if (ledCount == 0)
  {
    Tlc.set(0, 0);
    Tlc.set(1, 0);
    Tlc.set(2, 0);
  }
  else if (ledCount == 1)
  {
    Tlc.set(3, 0);
    Tlc.set(4, 0);
    Tlc.set(5, 0);
  }
  else if (ledCount == 2)
  {
    Tlc.set(6, 0);
    Tlc.set(7, 0);
    Tlc.set(8, 0);
  }
  else if (ledCount == 3)
  {
    Tlc.set(9, 0);
    Tlc.set(10, 0);
    Tlc.set(11, 0);
  }
  else if (ledCount == 4)
  {
    Tlc.set(12, 0);
    Tlc.set(13, 0);
    Tlc.set(14, 0);
  }
}


void TLCWhite(int ledCount)
{
  if (ledCount == 0)
  {
    Tlc.set(0, 4095);
    Tlc.set(1, 4095);
    Tlc.set(2, 4095);
  }
  else if (ledCount == 1)
  {
    Tlc.set(3, 4095);
    Tlc.set(4, 4095);
    Tlc.set(5, 4095);
  }
  else if (ledCount == 2)
  {
    Tlc.set(6, 4095);
    Tlc.set(7, 4095);
    Tlc.set(8, 4095);
  }
  else if (ledCount == 3)
  {
    Tlc.set(9, 4095);
    Tlc.set(10, 4095);
    Tlc.set(11, 4095);
  }
  else if (ledCount == 4)
  {
    Tlc.set(12, 4095);
    Tlc.set(13, 4095);
    Tlc.set(14, 4095);
  }
}

void TLCGray(int ledCount)
{
  if (ledCount == 0)
  {
    Tlc.set(0, 2000);
    Tlc.set(1, 2000);
    Tlc.set(2, 2000);
  }
  else if (ledCount == 1)
  {
    Tlc.set(3, 2000);
    Tlc.set(4, 2000);
    Tlc.set(5, 2000);
  }
  else if (ledCount == 2)
  {
    Tlc.set(6, 2000);
    Tlc.set(7, 2000);
    Tlc.set(8, 2000);
  }
  else if (ledCount == 3)
  {
    Tlc.set(9, 2000);
    Tlc.set(10, 2000);
    Tlc.set(11, 2000);
  }
  else if (ledCount == 4)
  {
    Tlc.set(12, 2000);
    Tlc.set(13, 2000);
    Tlc.set(14, 2000);
  }
}

void TLCDarkGray(int ledCount)
{
  if (ledCount == 0)
  {
    Tlc.set(0, 1000);
    Tlc.set(1, 1000);
    Tlc.set(2, 1000);
  }
  else if (ledCount == 1)
  {
    Tlc.set(3, 1000);
    Tlc.set(4, 1000);
    Tlc.set(5, 1000);
  }
  else if (ledCount == 2)
  {
    Tlc.set(6, 1000);
    Tlc.set(7, 1000);
    Tlc.set(8, 1000);
  }
  else if (ledCount == 3)
  {
    Tlc.set(9, 1000);
    Tlc.set(10, 1000);
    Tlc.set(11, 1000);
  }
  else if (ledCount == 4)
  {
    Tlc.set(12, 1000);
    Tlc.set(13, 1000);
    Tlc.set(14, 1000);
  }
}

void TLCRed(int ledCount)
{
  if (ledCount == 0)
  {
    Tlc.set(0, 4095);
    Tlc.set(1, 0);
    Tlc.set(2, 0);
  }
  else if (ledCount == 1)
  {
    Tlc.set(3, 4095);
    Tlc.set(4, 0);
    Tlc.set(5, 0);
  }
  else if (ledCount == 2)
  {
    Tlc.set(6, 4095);
    Tlc.set(7, 0);
    Tlc.set(8, 0);
  }
  else if (ledCount == 3)
  {
    Tlc.set(9, 4095);
    Tlc.set(10, 0);
    Tlc.set(11, 0);
  }
  else if (ledCount == 4)
  {
    Tlc.set(12, 4095);
    Tlc.set(13, 0);
    Tlc.set(14, 0);
  }
}

void TLCGreen(int ledCount)
{
  if (ledCount == 0)
  {
    Tlc.set(0, 0);
    Tlc.set(1, 4095);
    Tlc.set(2, 0);
  }
  else if (ledCount == 1)
  {
    Tlc.set(3, 0);
    Tlc.set(4, 4095);
    Tlc.set(5, 0);
  }
  else if (ledCount == 2)
  {
    Tlc.set(6, 0);
    Tlc.set(7, 4095);
    Tlc.set(8, 0);
  }
  else if (ledCount == 3)
  {
    Tlc.set(9, 0);
    Tlc.set(10, 4095);
    Tlc.set(11, 0);
  }
  else if (ledCount == 4)
  {
    Tlc.set(12, 0);
    Tlc.set(13, 4095);
    Tlc.set(14, 0);
  }
}

void TLCBlue(int ledCount)
{
  if (ledCount == 0)
  {
    Tlc.set(0, 0);
    Tlc.set(1, 0);
    Tlc.set(2, 4095);
  }
  else if (ledCount == 1)
  {
    Tlc.set(3, 0);
    Tlc.set(4, 0);
    Tlc.set(5, 4095);
  }
  else if (ledCount == 2)
  {
    Tlc.set(6, 0);
    Tlc.set(7, 0);
    Tlc.set(8, 4095);
  }
  else if (ledCount == 3)
  {
    Tlc.set(9, 0);
    Tlc.set(10, 0);
    Tlc.set(11, 4095);
  }
  else if (ledCount == 4)
  {
    Tlc.set(12, 0);
    Tlc.set(13, 0);
    Tlc.set(14, 4095);
  }
}

void TLCPurple(int ledCount)
{
  if (ledCount == 0)
  {
    Tlc.set(0, 2048);
    Tlc.set(1, 0);
    Tlc.set(2, 2048);
  }
  else if (ledCount == 1)
  {
    Tlc.set(3, 2048);
    Tlc.set(4, 0);
    Tlc.set(5, 2048);
  }
  else if (ledCount == 2)
  {
    Tlc.set(6, 2048);
    Tlc.set(7, 0);
    Tlc.set(8, 2048);
  }
  else if (ledCount == 3)
  {
    Tlc.set(9, 2048);
    Tlc.set(10, 0);
    Tlc.set(11, 2048);
  }
  else if (ledCount == 4)
  {
    Tlc.set(12, 2048);
    Tlc.set(13, 0);
    Tlc.set(14, 2048);
  }
}


void TLCLime(int ledCount)
{
  if (ledCount == 0)
  {
    Tlc.set(0, 2730);
    Tlc.set(1, 4095);
    Tlc.set(2, 0);
  }
  else if (ledCount == 1)
  {
    Tlc.set(3, 2730);
    Tlc.set(4, 4095);
    Tlc.set(5, 0);
  }
  else if (ledCount == 2)
  {
    Tlc.set(6, 2730);
    Tlc.set(7, 4095);
    Tlc.set(8, 0);
  }
  else if (ledCount == 3)
  {
    Tlc.set(9, 2730);
    Tlc.set(10, 4095);
    Tlc.set(11, 0);
  }
  else if (ledCount == 4)
  {
    Tlc.set(12, 2730);
    Tlc.set(13, 4095);
    Tlc.set(14, 0);
  }
}

void TLCOrange(int ledCount)
{
  if (ledCount == 0)
  {
    Tlc.set(0, 4095);
    Tlc.set(1, 2650);
    Tlc.set(2, 0);
  }
  else if (ledCount == 1)
  {
    Tlc.set(3, 4095);
    Tlc.set(4, 2650);
    Tlc.set(5, 0);
  }
  else if (ledCount == 2)
  {
    Tlc.set(6, 4095);
    Tlc.set(7, 2650);
    Tlc.set(8, 0);
  }
  else if (ledCount == 3)
  {
    Tlc.set(9, 4095);
    Tlc.set(10, 2650);
    Tlc.set(11, 0);
  }
  else if (ledCount == 4)
  {
    Tlc.set(12, 4095);
    Tlc.set(13, 2650);
    Tlc.set(14, 0);
  }
}

void TLCClear()
{
  for (int i = 0; i < 15; i++)
  {
    Tlc.set(i, 0);
    Tlc.update();

  }
}
