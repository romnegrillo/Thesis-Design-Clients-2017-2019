#include <LiquidCrystal_I2C.h>
#include <Keypad.h>
#include <Servo.h>

LiquidCrystal_I2C lcd(0x3F,2,1,0,4,5,6,7,3, POSITIVE);

const byte ROWS = 4; //four rows
const byte COLS = 4; //four columns
//define the cymbols on the buttons of the keypads
char hexaKeys[ROWS][COLS] = {
  {'1','4','7','*'},
  {'2','5','8','0'},
  {'3','6','9','#'},
  {'A','B','C','D'}
};

byte rowPins[ROWS] = {5, 4, 3, 2}; //connect to the row pinouts of the keypad
byte colPins[COLS] = {9, 8, 7, 6}; //connect to the column pinouts of the keypad

//initialize an instance of class NewKeypad
Keypad customKeypad = Keypad( makeKeymap(hexaKeys), rowPins, colPins, ROWS, COLS); 

String passTarget="3A6B";
String passInput="";

Servo myServo;

const int signalPin=10;
const int servoPin=11;

void setup() 
{
  pinMode(signalPin,OUTPUT);
  
  Serial.begin(9600);
  lcd.begin(16,2);
  lcd.print("Loading...");
  delay(2000);

  myServo.attach(servoPin);
  myServo.write(0);
  resetState();
}

void loop() 
{
  char customKey = customKeypad.getKey();
  
  if (customKey)
  {
    // Clear
    if(customKey=='*')
    {
      resetState();
    }
    // Confirm
    else if(customKey=='#')
    {
      if(passInput==passTarget)
      {
        lcd.clear();
        lcd.setCursor(0,0);
        lcd.print("Correct!");
        lcd.setCursor(0,1);
        lcd.print("# to reset");

        digitalWrite(signalPin,HIGH);
        myServo.write(90);
         
        while(customKeypad.getKey() != '#'){}
        
        resetState();
      }
      else
      {
        lcd.clear();
        lcd.setCursor(0,0);
        lcd.print("Wrong pass!");
        lcd.setCursor(0,1);
        lcd.print("# to reset");
        
        digitalWrite(signalPin,LOW);
        myServo.write(0);
        
        while(customKeypad.getKey() != '#'){}

        resetState();
      }
    }
    // Enter
    else
    {
      passInput+=customKey;
      lcd.setCursor(0,1);
      lcd.print(passInput);
    }    
  }
}

void resetState()
{
  digitalWrite(signalPin,LOW);
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("Enter password:");
  lcd.setCursor(0,1);
  passInput="";
  myServo.write(0);
  
}






