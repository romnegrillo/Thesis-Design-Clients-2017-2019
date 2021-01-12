#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
#include <avr/power.h>
#endif

#define PIN 2

// Parameter 1 = number of pixels in strip
// Parameter 2 = Arduino pin number (most are valid)
// Parameter 3 = pixel type flags, add together as needed:
//   NEO_KHZ800  800 KHz bitstream (most NeoPixel products w/WS2812 LEDs)
//   NEO_KHZ400  400 KHz (classic 'v1' (not v2) FLORA pixels, WS2811 drivers)
//   NEO_GRB     Pixels are wired for GRB bitstream (most NeoPixel products)
//   NEO_RGB     Pixels are wired for RGB bitstream (v1 FLORA pixels, not v2)
//   NEO_RGBW    Pixels are wired for RGBW bitstream (NeoPixel RGBW products)
Adafruit_NeoPixel strip = Adafruit_NeoPixel(50, PIN, NEO_GRB + NEO_KHZ800);

// IMPORTANT: To reduce NeoPixel burnout risk, add 1000 uF capacitor across
// pixel power leads, add 300 - 500 Ohm resistor on first pixel's data input
// and minimize distance between Arduino and first pixel.  Avoid connecting
// on a live circuit...if you must, connect GND first.

String dataIn;
int stripDelay=30;

void setup()
{
  Serial.begin(9600);
  Serial.flush();

  // This is for Trinket 5V 16MHz, you can remove these three lines if you are not using a Trinket
#if defined (__AVR_ATtiny85__)
  if (F_CPU == 16000000) clock_prescale_set(clock_div_1);
#endif
  // End of trinket special code


  strip.begin();
  strip.show(); // Initialize all pixels to 'off'
}

void loop()
{
  if (Serial.available())
  {
    dataIn = Serial.readStringUntil("\n");
    int seperator = dataIn.indexOf(",");

    if (seperator < 0)
    {
      goto Skip;
    }
    else
    {
      float ORPValue = dataIn.substring(0, seperator).toFloat();
      float pHValue = dataIn.substring(seperator + 1, -1).toFloat();

      /*
        0 - 255,0,0
        1 - 255,128,0
        2 - 255,178,102
        3 - 255,255,0
        4 - 204,204,0
        5 - 128,255,0
        6 - 76,153,0
        7.0-7.19, 7.81-7.99 - 0,153,0
        8 - 0,153,76
        9 - 0,204,204
        10 - 102,178,255
        11 - 0,76,153
        12 - 178,102,255
        13 - 127,0,255
        14 - 102,0,102
      */

      if (pHValue >= 0 && pHValue < 1)
      {
        colorWipe(strip.Color(255, 0, 0), stripDelay);
      }
      else if (pHValue >= 1 && pHValue < 2)
      {
        colorWipe(strip.Color(255, 128, 0), stripDelay);
      }
      else if (pHValue >= 2 && pHValue < 3)
      {
        colorWipe(strip.Color(255, 178, 102), stripDelay);
      }
      else if (pHValue >= 3 && pHValue < 4)
      {
        colorWipe(strip.Color(255, 255, 0), stripDelay);
      }
      else if (pHValue >= 4 && pHValue < 5)
      {
        colorWipe(strip.Color(204, 204, 0), stripDelay);
      }
      else if (pHValue >= 5 && pHValue < 6)
      {
        colorWipe(strip.Color(128, 255, 0), stripDelay);
      }
      else if (pHValue >= 6 && pHValue < 7)
      {
        colorWipe(strip.Color(76, 153, 0), stripDelay);
      }
      else if (pHValue >= 7 && pHValue < 8)
      {
        colorWipe(strip.Color(0, 153, 0), stripDelay);
      }
      else if (pHValue >= 8 && pHValue < 9)
      {
        colorWipe(strip.Color(0, 153, 76), stripDelay);
      }
      else if (pHValue >= 9 && pHValue < 1)
      {
        colorWipe(strip.Color(0, 204, 204), stripDelay);
      }
      else if (pHValue >= 10 && pHValue < 11)
      {
        colorWipe(strip.Color(102, 178, 255), stripDelay);
      }
      else if (pHValue >= 11 && pHValue < 12)
      {
        colorWipe(strip.Color(0, 76, 153), stripDelay);
      }
      else if (pHValue >= 12 && pHValue < 13)
      {
        colorWipe(strip.Color(178, 102, 255), stripDelay);
      }
      else if (pHValue >= 13 && pHValue < 14)
      {
        colorWipe(strip.Color(127, 0, 255), stripDelay);
      }
      else if (pHValue >= 14)
      {
        colorWipe(strip.Color(102, 0, 102), stripDelay);
      }

      if(ORPValue<720)
      {
        ORPWipe(strip.Color(50, 50, 50), stripDelay);
      }
      else
      {
        ORPWipe(strip.Color(0, 0, 0), stripDelay);
      }
    }

Skip:
    if(dataIn.substring(0,1)=="X")
    {
      wipeOut(strip.Color(0, 0, 0), 10);
    }
    dataIn = "";

    Serial.flush();

  }

  // Some example procedures showing how to display to the pixels:
  //colorWipe(strip.Color(255, 0, 0), 50); // Red
  //colorWipe(strip.Color(0, 255, 0), 50); // Green
  //colorWipe(strip.Color(0, 0, 255), 50); // Blue
  //colorWipe(strip.Color(0, 0, 0, 255), 50); // White RGBW
  // Send a theater pixel chase in...
  //theaterChase(strip.Color(127, 127, 127), 50); // White
  //theaterChase(strip.Color(127, 0, 0), 50); // Red
  //theaterChase(strip.Color(0, 0, 127), 50); // Blue

  //rainbow(20);
  //rainbowCycle(20);
  //theaterChaseRainbow(50);
}

// Fill the dots one after the other with a color
void colorWipe(uint32_t c, uint8_t wait) {
  for (uint16_t i = 0; i < strip.numPixels(); i=i+2) {
    strip.setPixelColor(i, c);
    strip.show();
    delay(wait);
  }
}

void ORPWipe(uint32_t c, uint8_t wait) {
  for (uint16_t i = 1; i < strip.numPixels(); i=i+2) {

    if(i<strip.numPixels())
    {
      strip.setPixelColor(i, c);
      strip.show();
      delay(wait);
    }
  }
}

void wipeOut(uint32_t c, uint8_t wait) {
  for (uint16_t i = 0; i < strip.numPixels(); i++) {
    strip.setPixelColor(i, c);
    strip.show();
    delay(wait);
  }
}



