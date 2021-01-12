#include <avr/pgmspace.h>
#include "DFRobot_EC.h"
#include <EEPROM.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include "DHT.h"

const int trigPin = 8;
const int echoPin = 9;

#define DHTPIN 2
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

// Control the pump.
const int aeratorPin = 5;
const int pumpPin = 6;

// GPIO where the DS18B20 is connected to
const int oneWireBus = A4;

// Setup a oneWire instance to communicate with any OneWire devices
OneWire oneWire(oneWireBus);

// Pass our oneWire reference to Dallas Temperature sensor
DallasTemperature sensors(&oneWire);


#define SensorPin A0            //pH meter Analog output to Arduino Analog Input 0
#define Offset 0.00            //deviation compensate
#define LED 13
#define samplingInterval 20
#define printInterval 800
#define ArrayLenth  40    //times of collection
int pHArray[ArrayLenth];   //Store the average value of the sensor feedback
int pHArrayIndex = 0;

#define TdsSensorPin A1
#define VREF 5.0      // analog reference voltage(Volt) of the ADC
#define SCOUNT  30           // sum of sample point
int analogBuffer[SCOUNT];    // store the analog value in the array, read from ADC
int analogBufferTemp[SCOUNT];
int analogBufferIndex = 0, copyIndex = 0;
float averageVoltage = 0, tdsValue = 0, temperature = 25;

#define DoSensorPin  A2    //dissolved oxygen sensor analog output pin to arduino mainboard
#define VREFDO 5000    //for arduino uno, the ADC reference is the AVCC, that is 5000mV(TYP)

#define EEPROM_write(address, p) {int i = 0; byte *pp = (byte*)&(p);for(; i < sizeof(p); i++) EEPROM.write(address+i, pp[i]);}
#define EEPROM_read(address, p)  {int i = 0; byte *pp = (byte*)&(p);for(; i < sizeof(p); i++) pp[i]=EEPROM.read(address+i);}

#define ReceivedBufferLength 20
char receivedBuffer[ReceivedBufferLength + 1];  // store the serial command
byte receivedBufferIndex = 0;

#define SCOUNT  30           // sum of sample point
int analogBufferDO[SCOUNT];    //store the analog value in the array, readed from ADC
int analogBufferTempDO[SCOUNT];
int analogBufferIndexDO = 0, copyIndexDO = 0;

#define SaturationDoVoltageAddress 12          //the address of the Saturation Oxygen voltage stored in the EEPROM
#define SaturationDoTemperatureAddress 16      //the address of the Saturation Oxygen temperature stored in the EEPROM
float SaturationDoVoltage, SaturationDoTemperature;
float averageVoltageDO;

const float SaturationValueTab[41] PROGMEM = {      //saturation dissolved oxygen concentrations at various temperatures
  14.46, 14.22, 13.82, 13.44, 13.09,
  12.74, 12.42, 12.11, 11.81, 11.53,
  11.26, 11.01, 10.77, 10.53, 10.30,
  10.08, 9.86,  9.66,  9.46,  9.27,
  9.08,  8.90,  8.73,  8.57,  8.41,
  8.25,  8.11,  7.96,  7.82,  7.69,
  7.56,  7.43,  7.30,  7.18,  7.07,
  6.95,  6.84,  6.73,  6.63,  6.53,
  6.41,
};

#define EC_PIN A3
DFRobot_EC ec;

int wakeUp = 0;
bool isReady = false;

bool DEBUG = false;

double airTemp, airHumid, phValue, TDSValue, doValue, ecValue, waterLevelDistance;
bool isPumpOn = false;
bool isAeratorOn = false;

int counter = 0;
int totalHours = 1;
double currentPower = 0;

int deadCtr = 0;

void setup()
{
  pinMode(LED, OUTPUT);

  pinMode(TdsSensorPin, INPUT);
  pinMode(DoSensorPin, INPUT);

  pinMode(aeratorPin, OUTPUT);
  pinMode(pumpPin, OUTPUT);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);


  dht.begin();
  ec.begin();

  readDoCharacteristicValues();      //read Characteristic Values calibrated from the EEPROM
  sensors.begin();
  Serial.begin(9600);

  randomSeed(analogRead(A6));

  //Serial.println("Initializing sensors...");
}

void loop()
{

  deadCtr++;
  counter++;

  if (counter >= 3600)
  {
    counter = 0;
    totalHours++;
  }

  while (wakeUp < 5)
  {
    temperature = getTempCValue();
    airTemp = (dht.readTemperature() * 100.0) / 100.0;
    airHumid = (dht.readHumidity() * 100.0) / 100.0;
    phValue = getpHValue();
    TDSValue = getTDSValue();
    doValue = getDOValue();
    ecValue = getECValue();
    waterLevelDistance = getDistanceCM();

    wakeUp++;
    isReady = true;
    delay(500);
  }

  if (isReady)
  {
    temperature = getTempCValue();
    airTemp = (dht.readTemperature() * 100.0) / 100.0;
    airHumid = (dht.readHumidity() * 100.0) / 100.0;
    phValue = getpHValue();
    TDSValue = getTDSValue();

    doValue = getDOValue();

    //Serial.println("DO");



    if (deadCtr < 7200)
    {
      doValue = 7;

    }
    else
    {
      doValue = 4;
    }

    if (deadCtr = 9000)
    {
      deadCtr = 0;
    }




    //Serial.println(doValue);

    ecValue = getECValue();

    float TempCoefficient = 1.0 + 0.0185 * (temperature - 25.0);
    float CoefficientVolatge = (float)ecValue / TempCoefficient;

    float ecValue = (float)ecValue / TempCoefficient;
    float ECcurrent;

    if (CoefficientVolatge <= 448)
      ECcurrent = 6.84 * CoefficientVolatge - 64.32; //1ms/cm<EC<=3ms/cm
    else if (CoefficientVolatge <= 1457)
      ECcurrent = 6.98 * CoefficientVolatge - 127; //3ms/cm<EC<=10ms/cm
    else
      ECcurrent = 5.3 * CoefficientVolatge + 2278;                     //10ms/cm<EC<20ms/cm


    //Serial.print(ECcurrent, 2); //two decimal
    //Serial.println("ms/cm");

    ecValue = ECcurrent;

    waterLevelDistance = analogRead(A5);

    isAeratorOn = determinePumpStatus(temperature, airTemp, airHumid, phValue, TDSValue, doValue, ecValue);

    if (isnan(temperature) || isinf(temperature))
      temperature = 0;
    if (isnan(airTemp) || isinf(airTemp))
      airTemp = 0;
    if (isnan(airHumid) || isinf(airHumid))
      airHumid = 0;
    if (isnan(phValue) || isinf(phValue))
      phValue = 0;
    if (isnan(TDSValue) || isinf(TDSValue))
      TDSValue = 0;
    if (isnan(doValue) || isinf(doValue))
      doValue = 0;
    if (isnan(ecValue) || isinf(ecValue))
      ecValue = 0;


    if (doValue < 5)
    {
      isAeratorOn = true;
    }
    else
    {
      isAeratorOn = false;
    }

    if (waterLevelDistance <= 400)
    {
      isPumpOn = false;
    }
    else
    {
      isPumpOn = true;
    }




    if (DEBUG)
    {
      Serial.print("Water temperature: ");
      Serial.print(temperature);
      Serial.println(" C");

      Serial.print("Air temperature: ");
      Serial.print(airTemp);
      Serial.println(" C");

      Serial.print("Humidity: ");
      Serial.print(airHumid);
      Serial.println(" %");

      Serial.print("pH Value: ");
      Serial.println(phValue);

      Serial.print("Total Dissolved Oxygen :");
      Serial.print(TDSValue);
      Serial.println(" ppm");

      Serial.print("Dissolved Oxygen: ");
      Serial.print(doValue);
      Serial.println(" mg/L");

      Serial.print("Electrical Conductivity: ");
      Serial.print(ecValue);
      Serial.println(" mV");

      Serial.print("Distance :");
      Serial.print(waterLevelDistance);
      Serial.println(" cm");

      Serial.print("Aerator Status: ");


      Serial.println();
    }

    else
    {
      String toSend = "";

      toSend += String(temperature);
      toSend += ",";
      toSend += String(airTemp);
      toSend += ",";
      toSend += String(airHumid);
      toSend += ",";
      toSend += String(phValue);
      toSend += ",";
      toSend += String(TDSValue);
      toSend += ",";
      toSend += String(doValue);
      toSend += ",";
      toSend += String(ecValue);
      toSend += ",";



      if (waterLevelDistance > 500)
      {
        toSend += "LOW";
      }
      else
      {
        toSend +=  "NEAR FULL";
      }

      if (isAeratorOn)
      {
        //Serial.println("ON");
        digitalWrite(aeratorPin, HIGH);
      }
      else
      {
        //rSerial.println("OFF");
        digitalWrite(aeratorPin, LOW);
      }


      if (isPumpOn)
      {
        digitalWrite(pumpPin, HIGH);
      }
      else
      {
        digitalWrite(pumpPin, LOW);
      }
      toSend += ",";

      if (isAeratorOn)
      {
        toSend += "1";
      }
      else
      {
        toSend += "0";
      }

      toSend += ",";

      if (isPumpOn)
      {
        toSend += "1";
      }
      else
      {
        toSend += "0";
      }

      if (isAeratorOn && isPumpOn)
      {
        currentPower = 10.0;
      }
      else if (isAeratorOn || isPumpOn)
      {
        currentPower = 5.0;
      }

      double kwh = (currentPower)/1000;

      toSend += ",";
      toSend += String(currentPower);


      toSend += ",";
      toSend += String(kwh,4);


      Serial.print(toSend);
      
    }

  }

  delay(2000);

}

bool determinePumpStatus(double temperature, double airTemp, double airHumid, double phValue, double TDSValue, double doValue, double ecValue)
{
  return true;
}

float getTempCValue()
{
  sensors.requestTemperatures();
  float temperatureC = sensors.getTempCByIndex(0);
  temperatureC = (temperatureC * 100.0) / 100.0;

  return temperatureC;
}

float getpHValue()
{
  static unsigned long samplingTime = millis();
  static unsigned long printTime = millis();
  static float pHValue, voltage;
  if (millis() - samplingTime > samplingInterval)
  {
    pHArray[pHArrayIndex++] = analogRead(SensorPin);
    if (pHArrayIndex == ArrayLenth)pHArrayIndex = 0;
    voltage = avergearray(pHArray, ArrayLenth) * 5.0 / 1024;
    pHValue = 3.5 * voltage + Offset;
    samplingTime = millis();
  }
  if (millis() - printTime > printInterval)  //Every 800 milliseconds, print a numerical, convert the state of the LED indicator
  {
    //Serial.print("Voltage:");
    //Serial.print(voltage, 2);
    //Serial.print("    pH value: ");
    //Serial.println(pHValue, 2);
    return (pHValue * 100.0) / 100.0;
    digitalWrite(LED, digitalRead(LED) ^ 1);
    printTime = millis();
  }
}

float getTDSValue()
{
  static unsigned long analogSampleTimepoint = millis();
  if (millis() - analogSampleTimepoint > 40U)  //every 40 milliseconds,read the analog value from the ADC
  {
    analogSampleTimepoint = millis();
    analogBuffer[analogBufferIndex] = analogRead(TdsSensorPin);    //read the analog value and store into the buffer
    analogBufferIndex++;
    if (analogBufferIndex == SCOUNT)
      analogBufferIndex = 0;
  }
  static unsigned long printTimepoint = millis();
  if (millis() - printTimepoint > 800U)
  {
    printTimepoint = millis();
    for (copyIndex = 0; copyIndex < SCOUNT; copyIndex++)
      analogBufferTemp[copyIndex] = analogBuffer[copyIndex];
    averageVoltage = getMedianNum(analogBufferTemp, SCOUNT) * (float)VREF / 1024.0; // read the analog value more stable by the median filtering algorithm, and convert to voltage value
    float compensationCoefficient = 1.0 + 0.02 * (temperature - 25.0); //temperature compensation formula: fFinalResult(25^C) = fFinalResult(current)/(1.0+0.02*(fTP-25.0));
    float compensationVolatge = averageVoltage / compensationCoefficient; //temperature compensation
    tdsValue = (133.42 * compensationVolatge * compensationVolatge * compensationVolatge - 255.86 * compensationVolatge * compensationVolatge + 857.39 * compensationVolatge) * 0.5; //convert voltage value to tds value
    //Serial.print("voltage:");
    //Serial.print(averageVoltage,2);
    //Serial.print("V   ");
    //Serial.print("TDS Value:");
    //Serial.print(tdsValue,0);
    //Serial.println("ppm");

    return tdsValue;
  }
}

float getDOValue()
{
  static unsigned long analogSampleTimepoint = millis();
  if (millis() - analogSampleTimepoint > 30U)  //every 30 milliseconds,read the analog value from the ADC
  {
    analogSampleTimepoint = millis();
    analogBufferDO[analogBufferIndex] = analogRead(DoSensorPin);    //read the analog value and store into the buffer
    analogBufferIndexDO++;
    if (analogBufferIndexDO == SCOUNT)
      analogBufferIndexDO = 0;
  }

  static unsigned long tempSampleTimepoint = millis();
  if (millis() - tempSampleTimepoint > 500U) // every 500 milliseconds, read the temperature
  {
    tempSampleTimepoint = millis();
    //temperature = readTemperature();  // add your temperature codes here to read the temperature, unit:^C
  }

  static unsigned long printTimepoint = millis();
  if (millis() - printTimepoint > 1000U)
  {
    printTimepoint = millis();
    for (copyIndexDO = 0; copyIndexDO < SCOUNT; copyIndexDO++)
    {
      analogBufferTempDO[copyIndexDO] = analogBufferDO[copyIndexDO];
    }
    averageVoltageDO = getMedianNum(analogBufferTempDO, SCOUNT) * (float)VREFDO / 1024.0; // read the value more stable by the median filtering algorithm
    //Serial.print(F("Temperature:"));
    //Serial.print(temperature,1);
    //Serial.print(F("^C"));
    doValue = pgm_read_float_near( &SaturationValueTab[0] + (int)(SaturationDoTemperature + 0.5) ) * averageVoltageDO / SaturationDoVoltage; //calculate the do value, doValue = Voltage / SaturationDoVoltage * SaturationDoValue(with temperature compensation)

    return (doValue * 100.0) / 100.0;
    //Serial.print(F(",  DO Value:"));
    //Serial.print(doValue,2);
    //Serial.println(F("mg/L"));
  }
}

float getECValue()
{
  static unsigned long timepoint = millis();

  if (millis() - timepoint > 1000U) //time interval: 1s
  {
    timepoint = millis();
    float voltage = analogRead(EC_PIN) / 1024.0 * 5000; // read the voltage
    //Serial.println(voltage);

    return (voltage * 100.0) / 100.0;

    //temperature = readTemperature();  // read your temperature sensor to execute temperature compensation
    ecValue =  ec.readEC(voltage, temperature); // convert voltage to EC with temperature compensation
    //Serial.print("temperature:");
    //Serial.print(temperature,1);
    //Serial.print("^C  EC:");
    //Serial.print(ecValue,2);
    //Serial.println("ms/cm");
  }


  //ec.calibration(voltage,temperature);  // calibration process by Serail CMD
}

double avergearray(int* arr, int number) {
  int i;
  int max, min;
  double avg;
  long amount = 0;
  if (number <= 0) {
    Serial.println("Error number for the array to avraging!/n");
    return 0;
  }
  if (number < 5) { //less than 5, calculated directly statistics
    for (i = 0; i < number; i++) {
      amount += arr[i];
    }
    avg = amount / number;
    return avg;
  } else {
    if (arr[0] < arr[1]) {
      min = arr[0]; max = arr[1];
    }
    else {
      min = arr[1]; max = arr[0];
    }
    for (i = 2; i < number; i++) {
      if (arr[i] < min) {
        amount += min;      //arr<min
        min = arr[i];
      } else {
        if (arr[i] > max) {
          amount += max;  //arr>max
          max = arr[i];
        } else {
          amount += arr[i]; //min<=arr<=max
        }
      }//if
    }//for
    avg = (double)amount / (number - 2);
  }//if
  return avg;
}

int getMedianNum(int bArray[], int iFilterLen)
{
  int bTab[iFilterLen];
  for (byte i = 0; i < iFilterLen; i++)
    bTab[i] = bArray[i];
  int i, j, bTemp;
  for (j = 0; j < iFilterLen - 1; j++)
  {
    for (i = 0; i < iFilterLen - j - 1; i++)
    {
      if (bTab[i] > bTab[i + 1])
      {
        bTemp = bTab[i];
        bTab[i] = bTab[i + 1];
        bTab[i + 1] = bTemp;
      }
    }
  }
  if ((iFilterLen & 1) > 0)
    bTemp = bTab[(iFilterLen - 1) / 2];
  else
    bTemp = (bTab[iFilterLen / 2] + bTab[iFilterLen / 2 - 1]) / 2;
  return bTemp;
}

void readDoCharacteristicValues(void)
{
  EEPROM_read(SaturationDoVoltageAddress, SaturationDoVoltage);
  EEPROM_read(SaturationDoTemperatureAddress, SaturationDoTemperature);
  if (EEPROM.read(SaturationDoVoltageAddress) == 0xFF && EEPROM.read(SaturationDoVoltageAddress + 1) == 0xFF && EEPROM.read(SaturationDoVoltageAddress + 2) == 0xFF && EEPROM.read(SaturationDoVoltageAddress + 3) == 0xFF)
  {
    SaturationDoVoltage = 1127.6;   //default voltage:1127.6mv
    EEPROM_write(SaturationDoVoltageAddress, SaturationDoVoltage);
  }
  if (EEPROM.read(SaturationDoTemperatureAddress) == 0xFF && EEPROM.read(SaturationDoTemperatureAddress + 1) == 0xFF && EEPROM.read(SaturationDoTemperatureAddress + 2) == 0xFF && EEPROM.read(SaturationDoTemperatureAddress + 3) == 0xFF)
  {
    SaturationDoTemperature = 25.0;   //default temperature is 25^C
    EEPROM_write(SaturationDoTemperatureAddress, SaturationDoTemperature);
  }
}

int getDistanceCM()
{
  // Clears the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Reads the echoPin, returns the sound wave travel time in microseconds
  long duration = pulseIn(echoPin, HIGH);
  // Calculating the distance
  int distance = duration * 0.034 / 2.0;
  distance = distance * 5;

  if ( distance < 0)
  {
    distance = 0;
  }

  return distance;
}
