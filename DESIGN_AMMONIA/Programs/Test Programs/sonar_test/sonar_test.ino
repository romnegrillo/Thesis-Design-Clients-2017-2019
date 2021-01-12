const int trigger=A4;
const int echo=A5;

void setup() 
{
  pinMode(trigger, OUTPUT);
  pinMode(echo, INPUT);

  Serial.begin(9600);
}

void loop() 
{
   int distance=getDistance();
   Serial.println(distance);
   //Serial.println(" cm");

   delay(1000);

}

int getDistance()
{
  digitalWrite(trigger, LOW);
  delayMicroseconds(2);

  digitalWrite(trigger, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigger, LOW);

  int distance = pulseIn(echo, HIGH);
  distance = distance * 0.034 / 2;

  return distance;
}

