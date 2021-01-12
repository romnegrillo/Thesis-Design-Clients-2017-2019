const int ledPin=13;
const int pirPin=4;
const int trigger=2;
const int echo=3;
const int buzzPin=A0;

void setup()
{
  pinMode(ledPin, OUTPUT);
  pinMode(pirPin,INPUT);  
  pinMode(trigger, OUTPUT);
  pinMode(echo, INPUT);
  pinMode(buzzPin,OUTPUT);
  
  Serial.begin(9600);
}

void loop() 
{
  int distance=getDistance();
  //Serial.println(distance);

  if(!(distance>=2 && distance<=400))
  {
    distance=0;
  }

  if(distance<10)
  {
    analogWrite(buzzPin,255);
  }
  else
  {
    analogWrite(buzzPin,0);
  }
  
  if(digitalRead(pirPin))
  {
    digitalWrite(ledPin,HIGH);   
    Serial.println("motion,"+String(distance));
    analogWrite(buzzPin,255);
  }
  else
  {
    digitalWrite(ledPin,LOW);
    Serial.println("no motion,"+String(distance));

    if(!(distance<10))
    {
      analogWrite(buzzPin,0);
    }
  }

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

