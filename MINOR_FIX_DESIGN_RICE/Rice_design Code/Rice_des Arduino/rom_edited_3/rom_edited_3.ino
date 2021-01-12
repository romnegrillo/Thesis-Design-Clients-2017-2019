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

float savedHum=0;
float hum;
int temp;

String offset="             ";

const int saveButtton=5;
int saveState=0;

void setup() 
{
  pinMode(saveButtton,INPUT_PULLUP);

  
  Serial.begin(9600);
  dht.begin();
  lcd.begin();

  lcd.backlight();  
  lcd.clear();
  initSDCard();

}

void loop() 
{
  hum = dht.readHumidity();
  temp = dht.readTemperature();

  // Save last reading pag pinindot.  
  // Isang pindot lang, may indicator naman sa lcd 
  // pag nakasave na yung last reading.
  if(!digitalRead(saveButtton))
  {
    //Serial.println("Save button is pressed!");

    if(saveState==0)
    { 
      savedHum=hum;
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("Last moisture");
      lcd.setCursor(0,1);
      lcd.print("reading saved");
      saveState=1;
    }
    else
    {
      saveState=0;
      savedHum=0;
    }
    
    // Delay para mabasa message.
    delay(1000);
  }

  if(saveState)
  {
    hum=hum-savedHum;
  }


  String rowOne="T:" + String(temp) +  String("C") + " P.M:" + String(savedHum);
  String rowTwo="C.Moisture:" + String(hum);
  
  lcd.setCursor(0,0);
  lcd.print(rowOne);
  lcd.setCursor(0,1);
  lcd.print(rowTwo);
  
  //Serial.println("========================");
  //Serial.println(rowOne);
  //Serial.println(rowTwo);
  //Serial.println("========================");

  Serial.println(String(hum) + String(",") + String(temp));
  saveData();
  
  delay(2000);
}

void initSDCard()
{
  lcd.setCursor(0, 0); lcd.print("Initializing");
  lcd.setCursor(0, 1); lcd.print("SD card...");
  
  delay(1000);
  
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
}
