const int triggerPin1 = 2;
const int echoPin1 = 3;

const int triggerPin2 = 4;
const int echoPin2 = 5;

const int triggerPin3 = 6;
const int echoPin3 = 7;

const int pump1Pin = 8;
const int pump2Pin = 9;
const int pump3Pin = 10;

const int setPointDistance = 10;

void setup()
{
  pinMode(triggerPin1, OUTPUT);
  pinMode(triggerPin2, OUTPUT);
  pinMode(triggerPin3, OUTPUT);

  pinMode(echoPin1, INPUT);
  pinMode(echoPin2, INPUT);
  pinMode(echoPin3, INPUT);

  pinMode(pump1Pin, OUTPUT);
  pinMode(pump2Pin, OUTPUT);
  pinMode(pump3Pin, OUTPUT);

  Serial.begin(9600);
}

void loop()
{
  String motor1Status, motor2Status, motor3Status;

  int container1Distance = getSonarDistance1();
  int container2Distance = getSonarDistance2();
  int container3Distance = getSonarDistance3();

  if (container1Distance > setPointDistance)
  {
    digitalWrite(pump1Pin, HIGH);
    motor1Status = "ON";
  }
  else
  {
    digitalWrite(pump1Pin, LOW);
    motor1Status = "OFF";
  }

  if (container2Distance > setPointDistance)
  {
    digitalWrite(pump2Pin, HIGH);
    motor2Status = "ON";
  }
  else
  {
    digitalWrite(pump2Pin, LOW);
    motor2Status = "OFF";
  }

  if (container3Distance > setPointDistance)
  {
    digitalWrite(pump3Pin, HIGH);
    motor3Status = "ON";
  }
  else
  {
    digitalWrite(pump3Pin, LOW);
    motor3Status = "OFF";
  }

  String toMATLAB = "";
  toMATLAB += String(container1Distance);
  toMATLAB += ",";
  toMATLAB += String(container2Distance);
  toMATLAB += ",";
  toMATLAB += String(container3Distance);
  toMATLAB += ",";
  toMATLAB += String(motor1Status);
  toMATLAB += ",";
  toMATLAB += String(motor2Status);
  toMATLAB += ",";
  toMATLAB += String(motor3Status);

  Serial.println(toMATLAB);

  delay(1000);
}

int getSonarDistance1()
{
  digitalWrite(triggerPin1, LOW);
  delayMicroseconds(2);

  digitalWrite(triggerPin1, HIGH);
  delayMicroseconds(10);
  digitalWrite(triggerPin1, LOW);

  int distance = pulseIn(echoPin1, HIGH);
  distance = distance * 0.034 / 2;

  // Check sensor distance ranger.
  if (!(distance >= 2 && distance <= 400))
  {
    return 0;
  }

  return distance;
}

int getSonarDistance2()
{
  digitalWrite(triggerPin2, LOW);
  delayMicroseconds(2);

  digitalWrite(triggerPin2, HIGH);
  delayMicroseconds(10);
  digitalWrite(triggerPin2, LOW);

  int distance = pulseIn(echoPin2, HIGH);
  distance = distance * 0.034 / 2;

  // Check sensor distance ranger.
  if (!(distance >= 2 && distance <= 400))
  {
    return 0;
  }

  return distance;
}

int getSonarDistance3()
{
  digitalWrite(triggerPin3, LOW);
  delayMicroseconds(2);

  digitalWrite(triggerPin3, HIGH);
  delayMicroseconds(10);
  digitalWrite(triggerPin3, LOW);

  int distance = pulseIn(echoPin3, HIGH);
  distance = distance * 0.034 / 2;

  // Check sensor distance ranger.
  if (!(distance >= 2 && distance <= 400))
  {
    return 0;
  }

  return distance;
}
