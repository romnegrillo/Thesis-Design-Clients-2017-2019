/* Comment this out to disable prints and save space */
#define BLYNK_PRINT Serial
#include <ESP8266WiFi.h>
#include <BlynkSimpleEsp8266.h>


const int trigPin = D2;
const int echoPin = D1;
const int relayPin = D3;

// You should get Auth Token in the Blynk App.
// Go to the Project Settings (nut icon).
char auth[] = "CmlloYCeDNoKCipk4oAcuWTCqjoHrxty";

// Your WiFi credentials.
// Set password to "" for open networks.
char ssid[] = "PLDTHOMEFIBR36684";
char pass[] = "princessBaby12301";

// Parametes to change depending on tank height and water level threshold.
const float distanceThresholdCM = 40;
const float maxTankLevelCM = 170;

int autoOrManual = 0;
int manualStatus = 0;

void setup()
{
  Serial.begin(9600);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  pinMode(relayPin, OUTPUT);
  digitalWrite(relayPin, LOW);  // Relay is active low.

  Blynk.begin(auth, ssid, pass);
  Blynk.run();

}

void loop()
{

  int waterLevelDistance = getDistanceCM();
  float waterLevelPercentage = (waterLevelDistance / maxTankLevelCM) * 100.0;
  String solenoidStatus = "OFF"; // off

  if (autoOrManual == 0)
  {

    if (waterLevelDistance > distanceThresholdCM)
    {
      digitalWrite(relayPin, HIGH); // Relay is active low.
      solenoidStatus = "ON";
    }
    else
    {
      digitalWrite(relayPin, LOW); // Relay is active low.
      solenoidStatus = "OFF";
    }
  }
  else
  {
    if (manualStatus == 0)
    {
      digitalWrite(relayPin, LOW); // Relay is active low.
      solenoidStatus = "OFF";
    }
    else
    {

      digitalWrite(relayPin, HIGH); // Relay is active low.
      solenoidStatus = "ON";
    }
  }

  Serial.print("Distance: ");
  Serial.println(waterLevelDistance);

  Serial.print("Percentage full: ");
  Serial.println(waterLevelPercentage);

  Blynk.virtualWrite(V1, String(waterLevelDistance) + " cm");
  Blynk.virtualWrite(V2, String(maxTankLevelCM) + " cm");
  Blynk.virtualWrite(V3, String(distanceThresholdCM) + " cm");
  Blynk.virtualWrite(V4, waterLevelPercentage);
  Blynk.virtualWrite(V5, solenoidStatus);


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
  distance=distance*5;
  
  if (distance > 400 || distance < 0)
  {
    distance = 0;
  }

  return distance;
}


BLYNK_WRITE(V6)
{
  autoOrManual = param.asInt();

  if (autoOrManual == 0)
  {
    Serial.println("Automatic Mode");
  }
  else
  {
    Serial.println("Manual Mode");
  }
}

BLYNK_WRITE(V7)
{
  manualStatus = param.asInt();

  if (manualStatus == 0)
  {
    Serial.println("OFF - Auto Mode");
  }
  else
  {
    Serial.println("ON - Auto Mode");
  }
}
