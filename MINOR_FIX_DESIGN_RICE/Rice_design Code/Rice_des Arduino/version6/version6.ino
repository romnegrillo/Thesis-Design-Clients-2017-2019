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

float hum, emc;
int temp;

const int toggle=5;
int toggleSwitch=0;

void setup() 
{
  pinMode(toggle,INPUT_PULLUP);
  
  Serial.begin(9600);
  dht.begin();
  lcd.begin();

  lcd.backlight();  
  initSDCard();
  lcd.clear(); 
}

void loop() 
{
  hum = dht.readHumidity();
  temp = dht.readTemperature();
  toggleSwitch=digitalRead(toggle);

  if(toggleSwitch == LOW)
  {
    if(temp == 22)
  {
    if((hum>=50)&&(hum<55))
    {
      emc=11.2;
    }
    else if((hum>=55)&&(hum<60))
    {
      emc=11.7;
    }
    else if((hum>=60)&&(hum<65))
    {
      emc=12.3;
    }
    else if((hum>=65)&&(hum<70))
    {
      emc=12.7;
    }
    else if((hum>=70)&&(hum<75))
    {
      emc=13.5;
    }
    else if((hum>=75)&&(hum<77))
    {
      emc=14.3;
    }
    else if((hum>=77)&&(hum<79))
    {
      emc=14.6;
    }
    else if((hum>=79)&&(hum<81))
    {
      emc=14.9;
    }
    else if((hum>=81)&&(hum<83))
    {
      emc=15.3;
    }
    else if((hum>=83)&&(hum<85))
    {
      emc=15.7;
    }
    else if((hum>=85)&&(hum<87))
    {
      emc=16.1;
    }
    else if((hum>=87)&&(hum<89))
    {
      emc=16.6;
    }
    else if((hum>=89)&&(hum<91))
    {
      emc=17.2;
    }
    else
    {
      emc=17.9;
    }
  }
 //--------------------------------------------------------------
  else if(temp==23)
  {
  if((hum>=50)&&(hum<55))
    {
      emc=11.05;
    }
    else if((hum>=55)&&(hum<60))
    {
      emc=11.6;
    }
    else if((hum>=60)&&(hum<65))
    {
      emc=12.15;
    }
    else if((hum>=65)&&(hum<70))
    {
      emc=12.65;
    }
    else if((hum>=70)&&(hum<75))
    {
      emc=13.4;
    }
    else if((hum>=75)&&(hum<77))
    {
      emc=14.15;
    }
    else if((hum>=77)&&(hum<79))
    {
      emc=14.45;
    }
    else if((hum>=79)&&(hum<81))
    {
      emc=14.8;
    }
    else if((hum>=81)&&(hum<83))
    {
      emc=15.2;
    }
    else if((hum>=83)&&(hum<85))
    {
      emc=15.7;
    }
    else if((hum>=85)&&(hum<87))
    {
      emc=16;
    }
    else if((hum>=87)&&(hum<89))
    {
      emc=16.5;
    }
    else if((hum>=89)&&(hum<91))
    {
      emc=17.1;
    }
    else
    {
      emc=17.8;
    }
  }
 //--------------------------------------------------------------
  else if((temp==24)||(temp==25))
  {
    if((hum>=50)&&(hum<55))
    {
      emc=10.9;
    }
    else if((hum>=55)&&(hum<60))
    {
      emc=11.5;
    }
    else if((hum>=60)&&(hum<65))
    {
      emc=12;
    }
    else if((hum>=65)&&(hum<70))
    {
      emc=12.6;
    }
    else if((hum>=70)&&(hum<75))
    {
      emc=13.3;
    }
    else if((hum>=75)&&(hum<77))
    {
      emc=14;
    }
    else if((hum>=77)&&(hum<79))
    {
      emc=14.3;
    }
    else if((hum>=79)&&(hum<81))
    {
      emc=14.7;
    }
    else if((hum>=81)&&(hum<83))
    {
      emc=15.1;
    }
    else if((hum>=83)&&(hum<85))
    {
      emc=15.7;
    }
    else if((hum>=85)&&(hum<87))
    {
      emc=15.9;
    }
    else if((hum>=87)&&(hum<89))
    {
      emc=16.4;
    }
    else if((hum>=89)&&(hum<91))
    {
      emc=17;
    }
    else
    {
      emc=17.7;
    }
  }
 //--------------------------------------------------------------
  else if(temp==26)
  {
    if((hum>=50)&&(hum<55))
    {
      emc=10.8;
    }
    else if((hum>=55)&&(hum<60))
    {
      emc=11.35;
    }
    else if((hum>=60)&&(hum<65))
    {
      emc=11.9;
    }
    else if((hum>=65)&&(hum<70))
    {
      emc=12.5;
    }
    else if((hum>=70)&&(hum<75))
    {
      emc=13.2;
    }
    else if((hum>=75)&&(hum<77))
    {
      emc=13.9;
    }
    else if((hum>=77)&&(hum<79))
    {
      emc=14.2;
    }
    else if((hum>=79)&&(hum<81))
    {
      emc=14.6;
    }
    else if((hum>=81)&&(hum<83))
    {
      emc=15;
    }
    else if((hum>=83)&&(hum<85))
    {
      emc=15.5;
    }
    else if((hum>=85)&&(hum<87))
    {
      emc=15.8;
    }
    else if((hum>=87)&&(hum<89))
    {
      emc=16.3;
    }
    else if((hum>=89)&&(hum<91))
    {
      emc=16.9;
    }
    else
    {
      emc=17.6;
    }
  }
 //--------------------------------------------------------------
  else if((temp==27)||(temp==28))
  {
    if((hum>=50)&&(hum<55))
    {
      emc=10.75;
    }
    else if((hum>=55)&&(hum<60))
    {
      emc=11.275;
    }
    else if((hum>=60)&&(hum<65))
    {
      emc=11.85;
    }
    else if((hum>=65)&&(hum<70))
    {
      emc=12.45;
    }
    else if((hum>=70)&&(hum<75))
    {
      emc=13.15;
    }
    else if((hum>=75)&&(hum<77))
    {
      emc=13.85;
    }
    else if((hum>=77)&&(hum<79))
    {
      emc=14.15;
    }
    else if((hum>=79)&&(hum<81))
    {
      emc=14.55;
    }
    else if((hum>=81)&&(hum<83))
    {
      emc=14.95;
    }
    else if((hum>=83)&&(hum<85))
    {
      emc=15.4;
    }
    else if((hum>=85)&&(hum<87))
    {
      emc=15.75;
    }
    else if((hum>=87)&&(hum<89))
    {
      emc=16.25;
    }
    else if((hum>=89)&&(hum<91))
    {
      emc=16.85;
    }
    else
    {
      emc=17.55;
    }
  }
 //--------------------------------------------------------------
  else if(temp==29)
  {
    if((hum>=50)&&(hum<55))
    {
      emc=10.65;
    }
    else if((hum>=55)&&(hum<60))
    {
      emc=11.15;
    }
    else if((hum>=60)&&(hum<65))
    {
      emc=11.75;
    }
    else if((hum>=65)&&(hum<70))
    {
      emc=12.35;
    }
    else if((hum>=70)&&(hum<75))
    {
      emc=13.03;
    }
    else if((hum>=75)&&(hum<77))
    {
      emc=13.75;
    }
    else if((hum>=77)&&(hum<79))
    {
      emc=14.05;
    }
    else if((hum>=79)&&(hum<81))
    {
      emc=14.45;
    }
    else if((hum>=81)&&(hum<83))
    {
      emc=14.85;
    }
    else if((hum>=83)&&(hum<85))
    {
      emc=15.25;
    }
    else if((hum>=85)&&(hum<87))
    {
      emc=15.65;
    }
    else if((hum>=87)&&(hum<89))
    {
      emc=16.15;
    }
    else if((hum>=89)&&(hum<91))
    {
      emc=16.75;
    }
    else
    {
      emc=17.45;
    }
  }
 //--------------------------------------------------------------
  else if(temp==30)
  {
    if((hum>=50)&&(hum<55))
    {
      emc=10.6;
    }
    else if((hum>=55)&&(hum<60))
    {
      emc=11.1;
    }
    else if((hum>=60)&&(hum<65))
    {
      emc=11.7;
    }
    else if((hum>=65)&&(hum<70))
    {
      emc=12.3;
    }
    else if((hum>=70)&&(hum<75))
    {
      emc=12.95;
    }
    else if((hum>=75)&&(hum<77))
    {
      emc=13.7;
    }
    else if((hum>=77)&&(hum<79))
    {
      emc=14;
    }
    else if((hum>=79)&&(hum<81))
    {
      emc=14.4;
    }
    else if((hum>=81)&&(hum<83))
    {
      emc=14.8;
    }
    else if((hum>=83)&&(hum<85))
    {
      emc=15.2;
    }
    else if((hum>=85)&&(hum<87))
    {
      emc=15.6;
    }
    else if((hum>=87)&&(hum<89))
    {
      emc=16.1;
    }
    else if((hum>=89)&&(hum<91))
    {
      emc=16.7;
    }
    else
    {
      emc=17.4;
    }
  }
 //--------------------------------------------------------------
    else if(temp==31)
  {
    if((hum>=50)&&(hum<55))
    {
      emc=10.55;
    }
    else if((hum>=55)&&(hum<60))
    {
      emc=11.05;
    }
    else if((hum>=60)&&(hum<65))
    {
      emc=11.65;
    }
    else if((hum>=65)&&(hum<70))
    {
      emc=12.25;
    }
    else if((hum>=70)&&(hum<75))
    {
      emc=12.875;
    }
    else if((hum>=75)&&(hum<77))
    {
      emc=13.65;
    }
    else if((hum>=77)&&(hum<79))
    {
      emc=13.95;
    }
    else if((hum>=79)&&(hum<81))
    {
      emc=14.35;
    }
    else if((hum>=81)&&(hum<83))
    {
      emc=14.7;
    }
    else if((hum>=83)&&(hum<85))
    {
      emc=15.15;
    }
    else if((hum>=85)&&(hum<87))
    {
      emc=15.55;
    }
    else if((hum>=87)&&(hum<89))
    {
      emc=16.05;
    }
    else if((hum>=89)&&(hum<91))
    {
      emc=16.65;
    }
    else
    {
      emc=17.35;
    }
  }
 //--------------------------------------------------------------   
    else if(temp==32)
  {
    if((hum>=50)&&(hum<55))
    {
      emc=10.5;
    }
    else if((hum>=55)&&(hum<60))
    {
      emc=11.0;
    }
    else if((hum>=60)&&(hum<65))
    {
      emc=11.6;
    }
    else if((hum>=65)&&(hum<70))
    {
      emc=12.2;
    }
    else if((hum>=70)&&(hum<75))
    {
      emc=12.8;
    }
    else if((hum>=75)&&(hum<77))
    {
      emc=13.6;
    }
    else if((hum>=77)&&(hum<79))
    {
      emc=13.9;
    }
    else if((hum>=79)&&(hum<81))
    {
      emc=14.3;
    }
    else if((hum>=81)&&(hum<83))
    {
      emc=14.6;
    }
    else if((hum>=83)&&(hum<85))
    {
      emc=15.1;
    }
    else if((hum>=85)&&(hum<87))
    {
      emc=15.5;
    }
    else if((hum>=87)&&(hum<89))
    {
      emc=16.0;
    }
    else if((hum>=89)&&(hum<91))
    {
      emc=16.6;
    }
    else
    {
      emc=17.3;
    }
  }
 //--------------------------------------------------------------
    else if(temp==33)
  {
    if((hum>=50)&&(hum<55))
    {
      emc=10.425;
    }
    else if((hum>=55)&&(hum<60))
    {
      emc=10.95;
    }
    else if((hum>=60)&&(hum<65))
    {
      emc=11.55;
    }
    else if((hum>=65)&&(hum<70))
    {
      emc=12.15;
    }
    else if((hum>=70)&&(hum<75))
    {
      emc=12.75;
    }
    else if((hum>=75)&&(hum<77))
    {
      emc=13.55;
    }
    else if((hum>=77)&&(hum<79))
    {
      emc=13.85;
    }
    else if((hum>=79)&&(hum<81))
    {
      emc=14.25;
    }
    else if((hum>=81)&&(hum<83))
    {
      emc=14.575;
    }
    else if((hum>=83)&&(hum<85))
    {
      emc=15.05;
    }
    else if((hum>=85)&&(hum<87))
    {
      emc=15.45;
    }
    else if((hum>=87)&&(hum<89))
    {
      emc=15.95;
    }
    else if((hum>=89)&&(hum<91))
    {
      emc=16.55;
    }
    else
    {
      emc=17.25;
    }
  }
//--------------------------------------------------------------
    else if(temp==34)
  {
    if((hum>=50)&&(hum<55))
    {
      emc=10.35;
    }
    else if((hum>=55)&&(hum<60))
    {
      emc=10.9;
    }
    else if((hum>=60)&&(hum<65))
    {
      emc=11.5;
    }
    else if((hum>=65)&&(hum<70))
    {
      emc=12.1;
    }
    else if((hum>=70)&&(hum<75))
    {
      emc=12.7;
    }
    else if((hum>=75)&&(hum<77))
    {
      emc=13.5;
    }
    else if((hum>=77)&&(hum<79))
    {
      emc=13.8;
    }
    else if((hum>=79)&&(hum<81))
    {
      emc=14.2;
    }
    else if((hum>=81)&&(hum<83))
    {
      emc=14.55;
    }
    else if((hum>=83)&&(hum<85))
    {
      emc=15.0;
    }
    else if((hum>=85)&&(hum<87))
    {
      emc=15.4;
    }
    else if((hum>=87)&&(hum<89))
    {
      emc=15.9;
    }
    else if((hum>=89)&&(hum<91))
    {
      emc=16.5;
    }
    else
    {
      emc=17.2;
    }
  }
//--------------------------------------------------------------
    else if(temp==35)
  {
    if((hum>=50)&&(hum<55))
    {
      emc=10.275;
    }
    else if((hum>=55)&&(hum<60))
    {
      emc=10.85;
    }
    else if((hum>=60)&&(hum<65))
    {
      emc=11.45;
    }
    else if((hum>=65)&&(hum<70))
    {
      emc=12.05;
    }
    else if((hum>=70)&&(hum<75))
    {
      emc=12.65;
    }
    else if((hum>=75)&&(hum<77))
    {
      emc=13.45;
    }
    else if((hum>=77)&&(hum<79))
    {
      emc=13.75;
    }
    else if((hum>=79)&&(hum<81))
    {
      emc=14.15;
    }
    else if((hum>=81)&&(hum<83))
    {
      emc=14.525;
    }
    else if((hum>=83)&&(hum<85))
    {
      emc=14.95;
    }
    else if((hum>=85)&&(hum<87))
    {
      emc=15.35;
    }
    else if((hum>=87)&&(hum<89))
    {
      emc=15.85;
    }
    else if((hum>=89)&&(hum<91))
    {
      emc=16.45;
    }
    else
    {
      emc=17.15;
    }
  }
//--------------------------------------------------------------
    else if(temp==36)
  {
    if((hum>=50)&&(hum<55))
    {
      emc=10.2;
    }
    else if((hum>=55)&&(hum<60))
    {
      emc=10.8;
    }
    else if((hum>=60)&&(hum<65))
    {
      emc=11.4;
    }
    else if((hum>=65)&&(hum<70))
    {
      emc=12.0;
    }
    else if((hum>=70)&&(hum<75))
    {
      emc=12.6;
    }
    else if((hum>=75)&&(hum<77))
    {
      emc=13.4;
    }
    else if((hum>=77)&&(hum<79))
    {
      emc=13.7;
    }
    else if((hum>=79)&&(hum<81))
    {
      emc=14.1;
    }
    else if((hum>=81)&&(hum<83))
    {
      emc=14.5;
    }
    else if((hum>=83)&&(hum<85))
    {
      emc=14.9;
    }
    else if((hum>=85)&&(hum<87))
    {
      emc=15.3;
    }
    else if((hum>=87)&&(hum<89))
    {
      emc=15.8;
    }
    else if((hum>=89)&&(hum<91))
    {
      emc=16.4;
    }
    else
    {
      emc=17.1;
    }
  }
//--------------------------------------------------------------    
    else if(temp==37)
  {
    if((hum>=50)&&(hum<55))
    {
      emc=10.15;
    }
    else if((hum>=55)&&(hum<60))
    {
      emc=10.75;
    }
    else if((hum>=60)&&(hum<65))
    {
      emc=11.45;
    }
    else if((hum>=65)&&(hum<70))
    {
      emc=11.95;
    }
    else if((hum>=70)&&(hum<75))
    {
      emc=12.575;
    }
    else if((hum>=75)&&(hum<77))
    {
      emc=13.35;
    }
    else if((hum>=77)&&(hum<79))
    {
      emc=13.65;
    }
    else if((hum>=79)&&(hum<81))
    {
      emc=14.05;
    }
    else if((hum>=81)&&(hum<83))
    {
      emc=14.45;
    }
    else if((hum>=83)&&(hum<85))
    {
      emc=14.85;
    }
    else if((hum>=85)&&(hum<87))
    {
      emc=15.25;
    }
    else if((hum>=87)&&(hum<89))
    {
      emc=15.75;
    }
    else if((hum>=89)&&(hum<91))
    {
      emc=16.35;
    }
    else
    {
      emc=17.05;
    }
  }
  }
  else
  {
    hum = 0;
    lcd.clear();
  }
  
  String rowOne="Temp: " + String(temp) + String(char(223)) +String("C");
  String rowTwo="Moisture: " + String(emc)+ String("%");
  
  lcd.setCursor(0,0);
  lcd.print(rowOne);
  lcd.setCursor(0,1);
  lcd.print(rowTwo);
  

  Serial.println(String(emc) + String(",") + String(temp));
  //Serial.println(String("H:")+String(hum));
  saveData();
  
  delay(2000);
}

void initSDCard()
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
    dataFile.print("Moisture: "); dataFile.print(emc); dataFile.println(" % ");
    dataFile.close();
  }
  else
  { // if the file isn't open, pop up an error
    
    lcd.clear();
    lcd.setCursor(0,0); lcd.print("Error Saving Data.");
    lcd.setCursor(0,1); lcd.print("File not found");

  }
}
