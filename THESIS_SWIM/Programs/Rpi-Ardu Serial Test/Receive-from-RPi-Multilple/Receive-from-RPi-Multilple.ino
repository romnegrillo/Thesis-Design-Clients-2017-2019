// Receives data from RPi
// and display it to LCD.

#include<LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x3F, 2, 1, 0, 4, 5, 6, 7, 3, POSITIVE);

String dataIn;

void setup()
{
  Serial.begin(9600);
  lcd.begin(16, 2);

  Serial.flush();
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

      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print(ORPValue);
      lcd.setCursor(0, 1);
      lcd.print(pHValue);
    }
    
Skip:
    dataIn = "";
    Serial.flush();
  }

}
