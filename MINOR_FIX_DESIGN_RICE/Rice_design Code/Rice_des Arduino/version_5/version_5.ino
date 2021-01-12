#include <DHT.h>
#include <SPI.h>
#include <SD.h>
#include <LiquidCrystal_I2C.h>
#include <Wire.h>

const int chipSelect = 10; //using SPI for SD card
LiquidCrystal_I2C lcd(0x27, 16, 2);

#define DHTPIN 3
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

char filename[]="data.txt";
int chk;

float hum, hum2;
float temp;

const int toggle=5;
int toggleSwitch=0;

void setup() 
{
  pinMode(toggle,INPUT_PULLUP);
  
  Serial.begin(9600);
  dht.begin();
  lcd.begin();

  lcd.backlight();  
  //initSDCard();
  lcd.clear(); 
}

void loop() 
{
  hum = dht.readHumidity();
  hum2 = dht.readHumidity();
  temp = dht.readTemperature();
  toggleSwitch=digitalRead(toggle);

  if(toggleSwitch == LOW)
  {
    if ((temp == 22)||(temp==23))
    {
      hum = map(hum, 50, 91, 11.2, 17.9);
    }
    else if ((temp==24)||(temp==25)||(temp==26)||(temp==27))
    {
       hum = (map(hum, 50, 91, 10.9, 17.7)/100.0);
    }
    else if ((temp==28)||(temp==29)||(temp==30)||(temp==31))
    {
       hum = map(hum, 50, 91, 10.7, 17.5)/100.0);
       //hum = map(hum, 50, 91, 10.7, 17.5);
    }
    else if ((temp==32)||(temp==33)||(temp==34)||(temp==35))
    {
       hum = map(hum, 50, 91, 10.5, 17.3);
    }
    else if ((temp==36)||(temp==37)||(temp==38)||(temp==39))
    {
       hum = map(hum, 50, 91, 10.2, 17.1);
    }
    else if ((temp==40)||(temp==41)||(temp==42)||(temp==43))
    {
       hum = map(hum, 50, 91, 10.0, 16.9);
    }
    else
    {
       hum = map(hum, 50, 91, 9.9, 16.7);
    }
  }
  else
  {
    hum = 0;
    lcd.clear();
  }
  
  String rowOne="Temp: " + String(temp) + String(char(223)) +String("C");
  String rowTwo="Moisture: " + String(hum)+ String("%");
  
  lcd.setCursor(0,0);
  lcd.print(rowOne);
  lcd.setCursor(0,1);
  lcd.print(rowTwo);
  

  Serial.println(String(hum) + String(",") + String(temp));
  Serial.println(String("H:")+String(hum2));
  //saveData();
  
  delay(2000);
}

/*void initSDCard()
{
  lcd.setCursor(0, 0); lcd.print("Initializing");
  lcd.setCursor(0, 1); lcd.print("SD card...");
  delay(500);
  lcd.setCursor(0, 0); lcd.print("WAIT 1 MINUTE");
  lcd.setCursor(0, 1); lcd.print("BEFORE MEASURE!!");
  
  delay(3000);
  
  if (!SD.begin(chipSelect)) 
  { //check if sd card mod. is working
    lcd.clear();
    lcd.setCursor(0, 0); lcd.print("Card not FOUND");
    lcd.setCursor(0, 1); lcd.print("Please Restart.");
    while (1);
  }
}
void saveData()
{
  File dataFile = SD.open(filename, FILE_WRITE);
  
  if (dataFile)
  { // if the file is available, write to it:
    dataFile.print("Temperature: "); dataFile.print(temp);dataFile.print(",");
    dataFile.print("Moisture: "); dataFile.print(hum); dataFile.println(" % ");
    dataFile.close();
  }
  else
  { // if the file isn't open, pop up an error
    
    lcd.clear();
    lcd.setCursor(0,0); lcd.print("Error Saving Data.");
    lcd.setCursor(0,1); lcd.print("File not found");

  }
}*/
