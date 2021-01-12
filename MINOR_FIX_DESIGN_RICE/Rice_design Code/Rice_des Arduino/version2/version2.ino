#include "DHT.h"
#include <SD.h>
#include <LiquidCrystal_I2C.h>
#include <Wire.h>

const int chipSelect = 10; //using SPI for SD card
LiquidCrystal_I2C lcd(0x27, 16, 2);

#define DHT11_PIN 3

#define DHTTYPE DHT11
double humid;
int val=0;
int soilPin=A3;
DHT dht(DHT11_PIN, DHTTYPE);

void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);
dht.begin();
pinMode(2,INPUT_PULLUP);
lcd.begin();

  // Turn on the blacklight and print a message.
  lcd.backlight();
  
lcd.clear();
  lcd.setCursor(0, 0); lcd.print("Initializing");
  lcd.setCursor(0, 1); lcd.print("SD card...");
  delay(1000);
if (!SD.begin(chipSelect)) { //check if sd card mod. is working
    lcd.clear();
    lcd.setCursor(0, 0); lcd.print("Card not FOUND");
    lcd.setCursor(0, 1); lcd.print("Please Restart.");
    while (1);
  }
  
}

void loop() {
  // put your main code here, to run repeatedly:
humid=dht.readHumidity();
val = analogRead(soilPin);
val = map(val, 1023,420,0,100);
lcd.clear();
lcd.setCursor(0,0); lcd.print("Moisture: "+String(val)+"%");
lcd.setCursor(0,1); lcd.print("Humid: "+String(humid)+"RH");
Serial.println(String(val)+","+String(humid));
if(digitalRead(2)==LOW)
saveData();
delay(1000);
}

void saveData(){
  File dataFile = SD.open("Data.txt", FILE_WRITE);
  if (dataFile){ // if the file is available, write to it:
    dataFile.print("Moisture: "); dataFile.print(val); dataFile.print(",");
    dataFile.print("Humidity: "); dataFile.print(humid); dataFile.println(" RH ");
    dataFile.close();
    lcd.clear();
    lcd.setCursor(0,0); lcd.print("Data Saved.");
  }
  else{ // if the file isn't open, pop up an error
    
    lcd.clear();
    lcd.setCursor(0,0); lcd.print("Error Saving Data.");
    lcd.setCursor(0,1); lcd.print("File not found");

  }
}

