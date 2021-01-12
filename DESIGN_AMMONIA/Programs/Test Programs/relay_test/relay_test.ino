int relay1Pin=A1;
int relay2Pin=A2;

void setup() 
{
   pinMode(relay1Pin,OUTPUT);
   pinMode(relay2Pin,OUTPUT);
}

void loop() 
{
  digitalWrite(relay1Pin,HIGH);
  digitalWrite(relay2Pin,HIGH);
  delay(3000);
  digitalWrite(relay1Pin,LOW);
  digitalWrite(relay2Pin,LOW);
  delay(3000);
}
