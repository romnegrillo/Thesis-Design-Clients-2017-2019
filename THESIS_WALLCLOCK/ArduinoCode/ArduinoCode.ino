#if 1

#include <Adafruit_GFX.h>
#include <MCUFRIEND_kbv.h>
#include <Wire.h>
#include <GPRS_Shield_Arduino.h>
MCUFRIEND_kbv tft;
#include <TouchScreen.h>
#include <virtuabotixRTC.h>
#define MINPRESSURE 200
#define MAXPRESSURE 1000
#include <SoftwareSerial.h>
#include <TinyGPS.h>

#include <Fonts/FreeSans9pt7b.h>
#include <Fonts/FreeSans12pt7b.h>
#include <Fonts/FreeSerif12pt7b.h>

#include <FreeDefaultFonts.h>

virtuabotixRTC myRTC(22, 23, 24);
String myTime, myDate;

unsigned long previousMillis = 0;

const long interval = 30000;

#define PIN_TX    53
#define PIN_RX    52
#define BAUDRATE  9600
#define PHONE_NUMBER_2 "+639171709038"
#define PHONE_NUMBER "+639177760112"
String googleLinkFormat = "https://www.google.com/maps/search/?api=1&query=<lat>,<lon>";

GPRS gprs(PIN_TX, PIN_RX, BAUDRATE); //RX,TX,BaudRate

TinyGPS gps;
SoftwareSerial gpsSS(51, 50);
String lat = "14.626660", lon = "121.061157";
bool gpsConnected = false;

const int buttonPin = 49;
const int buzzerPin = 48;

// ALL Touch panels and wiring is DIFFERENT
// copy-paste results from Touc2hScreen_Calibr_native.ino
const int XP = 6, XM = A2, YP = A1, YM = 7; //ID=0x9341
const int TS_LEFT = 922, TS_RT = 172, TS_TOP = 174, TS_BOT = 918;

TouchScreen ts = TouchScreen(XP, YP, XM, YM, 300);
Adafruit_GFX_Button oneButton, twoButton, threeButton, fourButton, fiveButton, sixButton, sevenButton, eightButton, nineButton;
Adafruit_GFX_Button clearButton, addButton, subtractButton, divideButton, multiplyButton, equalsButton;

int pixel_x, pixel_y;     //Touch_getXY() updates global vars
bool Touch_getXY(void)
{
  TSPoint p = ts.getPoint();
  pinMode(YP, OUTPUT);      //restore shared pins
  pinMode(XM, OUTPUT);
  digitalWrite(YP, HIGH);   //because TFT control pins
  digitalWrite(XM, HIGH);
  bool pressed = (p.z > MINPRESSURE && p.z < MAXPRESSURE);
  if (pressed) {
    pixel_x = map(p.x, TS_LEFT, TS_RT, 0, tft.width()); //.kbv makes sense to me
    pixel_y = map(p.y, TS_TOP, TS_BOT, 0, tft.height());
  }
  return pressed;
}

#define BLACK   0x0000
#define BLUE    0x001F
#define RED     0xF800
#define GREEN   0x07E0
#define CYAN    0x07FF
#define MAGENTA 0xF81F
#define YELLOW  0xFFE0
#define WHITE   0xFFFF

String currDisplayString = "";
float currDisplay = 0;
float ans = 0;
int prevOper = 0;


void setup(void)
{
  pinMode(buttonPin, INPUT_PULLUP);
  pinMode(buzzerPin, OUTPUT);

  Serial.begin(9600);

  //myRTC.setDS1302Time(00, 10, 11, 7, 28, 9, 2019);

  uint16_t ID = tft.readID();
  Serial.print("TFT ID = 0x");
  Serial.println(ID, HEX);
  Serial.println("Calibrate for your Touch Panel");
  if (ID == 0xD3D3) ID = 0x9486; // write-only shield
  tft.begin(ID);
  tft.setRotation(0);            //PORTRAIT
  tft.fillScreen(BLACK);

  tft.setTextColor(RED, BLACK);
  //showmsgXY(20, 10, 2, NULL, "12:00 PM   G S");
  //showmsgXY(20, 36, 2, NULL, "WED, 08/12/2019");
  updateDateTime();

  tft.fillRect(10, 65, 220, 50, RED);

  oneButton.initButton(&tft,  35, 150, 50, 40, WHITE, CYAN, BLACK, "1", 3);
  twoButton.initButton(&tft, 90, 150, 50, 40, WHITE, CYAN, BLACK, "2", 3);
  threeButton.initButton(&tft,  145, 150, 50, 40, WHITE, CYAN, BLACK, "3", 3);
  clearButton.initButton(&tft,  200, 150, 50, 40, WHITE, CYAN, BLACK, "C", 3);

  fourButton.initButton(&tft,  35, 200, 50, 40, WHITE, CYAN, BLACK, "4", 3);
  fiveButton.initButton(&tft, 90, 200, 50, 40, WHITE, CYAN, BLACK, "5", 3);
  sixButton.initButton(&tft,  145, 200, 50, 40, WHITE, CYAN, BLACK, "6", 3);
  equalsButton.initButton(&tft,  200, 225, 50, 90, WHITE, CYAN, BLACK, "=", 3);


  sevenButton.initButton(&tft,  35, 250, 50, 40, WHITE, CYAN, BLACK, "7", 3);
  eightButton.initButton(&tft, 90, 250, 50, 40, WHITE, CYAN, BLACK, "8", 3);
  nineButton.initButton(&tft,  145, 250, 50, 40, WHITE, CYAN, BLACK, "9", 3);

  divideButton.initButton(&tft,  35, 300, 50, 40, WHITE, CYAN, BLACK, "/", 3);
  multiplyButton.initButton(&tft, 90, 300, 50, 40, WHITE, CYAN, BLACK, "*", 3);
  subtractButton.initButton(&tft,  145, 300, 50, 40, WHITE, CYAN, BLACK, "-", 3);
  addButton.initButton(&tft,  200, 300, 50, 40, WHITE, CYAN, BLACK, "+", 3);


  oneButton.drawButton(false);
  twoButton.drawButton(false);
  threeButton.drawButton(false);
  fourButton.drawButton(false);
  fiveButton.drawButton(false);
  sixButton.drawButton(false);
  sevenButton.drawButton(false);
  eightButton.drawButton(false);
  nineButton.drawButton(false);
  clearButton.drawButton(false);
  addButton.drawButton(false);
  subtractButton.drawButton(false);
  divideButton.drawButton(false);
  multiplyButton.drawButton(false);
  equalsButton.drawButton(false);


   
  gprs.checkPowerUp();
  gprs.init();
}


void loop(void)
{

  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= interval) {
    // save the last time you blinked the LED
    previousMillis = currentMillis;
    updateDateTime();
    getLatLon();
    gprs.init();
  }

  checkButtonPressed();
  checkAlarmButton();
}

void checkAlarmButton()
{
  int alarmButtonStatus = !digitalRead(buttonPin);

  if (alarmButtonStatus)
  {
    digitalWrite(buzzerPin, HIGH);
    sendAlarmSMS();
  }
  else
  {
    digitalWrite(buzzerPin, LOW);
  }
}

void drawEval(String command)
{

  tft.fillRect(10, 65, 220, 50, RED);

  if (command != "+" && command != "-" && command != "/" && command != "*" && command != "C" && command != "=")
  {
    currDisplayString += command;

    char buff[12];
    currDisplayString.toCharArray(buff, 12);
    showmsgXY(10, 70, 3, NULL, buff);
  }
  else if (command == "C")
  {
    currDisplayString = "";
    currDisplay = 0;
    ans = 0;
    prevOper = 0;

    showmsgXY(10, 70, 3, NULL, 0);
  }
  else if (command == "+")
  {
    ans = currDisplayString.toFloat();

    showmsgXY(10, 70, 3, NULL, 0);
    currDisplayString = "";
    prevOper = 1;

    char buff[12];
    showmsgXY(10, 70, 3, NULL, 0);
  }
  else if (command == "-")
  {
    ans = currDisplayString.toFloat();

    showmsgXY(10, 70, 3, NULL, 0);
    currDisplayString = "";
    prevOper = 2;


    char buff[12];
    showmsgXY(10, 70, 3, NULL, 0);
  }
  else if (command == "*")
  {
    ans = currDisplayString.toFloat();

    Serial.println(ans);

    showmsgXY(10, 70, 3, NULL, 0);
    currDisplayString = "";

    prevOper = 3;


    char buff[12];
    showmsgXY(10, 70, 3, NULL, 0);
  }
  else if (command == "/")
  {
    ans = currDisplayString.toFloat();

    showmsgXY(10, 70, 3, NULL, 0);
    currDisplayString = "";
    prevOper = 4;


    char buff[12];
    showmsgXY(10, 70, 3, NULL, 0);
  }
  else if (command == "=")
  {
    if (prevOper == 1)
    {
      Serial.println("Add: ");
      ans += currDisplayString.toFloat();
    }
    else if (prevOper == 2)
    {
      Serial.println("Subtract: ");
      ans -= currDisplayString.toFloat();
    }
    else if (prevOper == 3)
    {
      Serial.println("Multiply: ");
      ans *= currDisplayString.toFloat();
    }
    else if (prevOper == 4)
    {
      Serial.println("Divide: ");
      ans /= currDisplayString.toFloat();
    }


    Serial.println(ans);


    String toDisp = String(ans);
    currDisplayString = toDisp;

    char buff[12];
    toDisp.toCharArray(buff, 12);

    showmsgXY(10, 70, 3, NULL, buff);

  }

}

void checkButtonPressed()
{
  bool down = Touch_getXY();

  oneButton.press(down && oneButton.contains(pixel_x, pixel_y));
  twoButton.press(down && twoButton.contains(pixel_x, pixel_y));
  threeButton.press(down && threeButton.contains(pixel_x, pixel_y));
  fourButton.press(down && fourButton.contains(pixel_x, pixel_y));
  fiveButton.press(down && fiveButton.contains(pixel_x, pixel_y));
  sixButton.press(down && sixButton.contains(pixel_x, pixel_y));
  sevenButton.press(down && sevenButton.contains(pixel_x, pixel_y));
  eightButton.press(down && eightButton.contains(pixel_x, pixel_y));
  nineButton.press(down && nineButton.contains(pixel_x, pixel_y));
  clearButton.press(down && clearButton.contains(pixel_x, pixel_y));
  addButton.press(down && addButton.contains(pixel_x, pixel_y));
  subtractButton.press(down && subtractButton.contains(pixel_x, pixel_y));
  divideButton.press(down && divideButton.contains(pixel_x, pixel_y));
  multiplyButton.press(down && multiplyButton.contains(pixel_x, pixel_y));
  equalsButton.press(down && equalsButton.contains(pixel_x, pixel_y));

  if (oneButton.justReleased())
  {
    oneButton.drawButton();
    drawEval("1");
  }
  if (twoButton.justReleased())
  {
    twoButton.drawButton();
    drawEval("2");
  }
  if (threeButton.justReleased())
  {
    threeButton.drawButton();
    drawEval("3");
  }
  if (fourButton.justReleased())
  {
    fourButton.drawButton();
    drawEval("4");
  }
  if (fiveButton.justReleased())
  {
    fiveButton.drawButton();
    drawEval("5");
  }
  if (sixButton.justReleased())
  {
    sixButton.drawButton();
    drawEval("6");
  }
  if (sevenButton.justReleased())
  {
    sevenButton.drawButton();
    drawEval("7");
  }
  if (eightButton.justReleased())
  {
    eightButton.drawButton();
    drawEval("8");
  }
  if (nineButton.justReleased())
  {
    nineButton.drawButton();
    drawEval("9");
  }
  if (clearButton.justReleased())
  {
    clearButton.drawButton();
    drawEval("C");
  }
  if (addButton.justReleased())
  {
    addButton.drawButton();
    drawEval("+");
  }
  if (subtractButton.justReleased())
  {
    subtractButton.drawButton();
    drawEval("-");
  }
  if (divideButton.justReleased())
  {
    divideButton.drawButton();
    drawEval("/");
  }
  if (multiplyButton.justReleased())
  {
    multiplyButton.drawButton();
    drawEval("*");
  }
  if (equalsButton.justReleased())
  {
    equalsButton.drawButton();
    drawEval("=");
  }

  if (oneButton.justPressed())
  {
    oneButton.drawButton(true);
  }

  if (twoButton.justPressed())
  {
    twoButton.drawButton(true);
  }

  if (threeButton.justPressed())
  {
    threeButton.drawButton(true);
  }

  if (fourButton.justPressed())
  {
    fourButton.drawButton(true);
  }

  if (fiveButton.justPressed())
  {
    fiveButton.drawButton(true);
  }

  if (sixButton.justPressed())
  {
    sixButton.drawButton(true);
  }

  if (sevenButton.justPressed())
  {
    sevenButton.drawButton(true);

  }

  if (eightButton.justPressed())
  {
    eightButton.drawButton(true);

  }

  if (nineButton.justPressed())
  {
    nineButton.drawButton(true);;
  }

  if (addButton.justPressed())
  {
    addButton.drawButton(true);
  }

  if (subtractButton.justPressed())
  {
    subtractButton.drawButton(true);
  }

  if (divideButton.justPressed())
  {
    divideButton.drawButton(true);
  }

  if (multiplyButton.justPressed())
  {
    multiplyButton.drawButton(true);
  }

  if (equalsButton.justPressed())
  {
    equalsButton.drawButton(true);
  }

  if (clearButton.justPressed())
  {
    clearButton.drawButton(true);

  }
}

void showmsgXY(int x, int y, int sz, const GFXfont *f, const char *msg)
{
  int16_t x1, y1;
  uint16_t wid, ht;
  //tft.drawFastHLine(0, y, tft.width(), WHITE);
  tft.setFont(f);
  tft.setCursor(x, y);
  tft.setTextColor(GREEN);
  tft.setTextSize(sz);
  tft.println(msg);
  delay(1000);
}

void updateDateTime()
{
  myRTC.updateTime();

  String formatTime = "";
  String prefix;

  myTime = "";
  myDate = "";

  myTime += String(myRTC.hours);

  if (myTime.toInt() >= 0 && myTime.toInt() <= 11)
  {
    prefix = " AM";
  }
  else
  {
    prefix = " PM";
  }


  if (myTime == "0")
  {
    myTime = "12";
  }
  else if (myTime == "1")
  {
    myTime = "01";
  }

  else if (myTime == "2")
  {
    myTime = "02";
  }

  else if (myTime == "3")
  {
    myTime = "03";
  }

  else if (myTime == "4")
  {
    myTime = "04";
  }

  else if (myTime == "5")
  {
    myTime = "05";
  }

  else if (myTime == "6")
  {
    myTime = "06";
  }

  else if (myTime == "7")
  {
    myTime = "07";
  }

  else if (myTime == "8")
  {
    myTime = "08";
  }

  else if (myTime == "9")
  {
    myTime = "09";
  }


  if (myTime.toInt() > 12)
  {
    myTime = String(myTime.toInt() - 12);
  }


  Serial.print("Day of the month: ");
  Serial.println(myRTC.dayofmonth);

  myTime += ":";
  myTime += String(myRTC.minutes);
  myTime += prefix;

  if (myRTC.dayofweek == 1)
  {
    myDate += "SUN, ";
  }
  else if (myRTC.dayofweek == 2)
  {
    myDate += "MON, ";
  }
  else if (myRTC.dayofweek == 3)
  {
    myDate += "TUE, ";
  }
  else if (myRTC.dayofweek == 4)
  {
    myDate += "WED, ";
  }
  else if (myRTC.dayofweek == 5)
  {
    myDate += "THU, ";
  }
  else if (myRTC.dayofweek == 6)
  {
    myDate += "FRI, ";
  }
  else if (myRTC.dayofweek == 7)
  {
    myDate += "SAT, ";
  }

  myDate += String(myRTC.month);
  myDate += "/";
  myDate += String(myRTC.dayofmonth);
  myDate += "/";
  myDate += String(myRTC.year);

  if (true)
  {
    myTime += " G S";
  }

  char buff1[30];
  char buff2[30];

  myTime.toCharArray(buff1, 15);
  myDate.toCharArray(buff2, 15);

  tft.fillRect(20, 10, 220, 50, BLACK);

  showmsgXY(20, 10, 2, NULL, buff1);
  showmsgXY(20, 36, 2, NULL, buff2);

  Serial.println(myTime);
  Serial.println(myDate);
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

  //Serial.print("Latitude: ");
  //Serial.println(lat);
  //Serial.print("Longitude: ");
  //Serial.println(lon);
}

void sendAlarmSMS()
{
  gprs.listen();

  String toSend = "Help I'm at ";
  toSend += googleLinkFormat;
  toSend.replace("<lat>", String(lat));
  toSend.replace("<lon>", String(lon));

  Serial.println(toSend);



  char buff[100];
  toSend.toCharArray(buff, 100);

  gprs.sendSMS(PHONE_NUMBER, buff);
  delay(1000);
  gprs.sendSMS(PHONE_NUMBER_2, buff);
   

}


#endif
