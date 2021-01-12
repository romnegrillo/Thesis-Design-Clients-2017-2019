int buttonCount=0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  //Serial.println("Waiting for LabView commands...");

  pinMode(13,OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()>0)
  {
    buttonCount++;
    Serial.println(buttonCount);
    
    
    byte x=Serial.read();

    if(x=='a')
    {
      digitalWrite(13,HIGH);
    }
    else
    {
      digitalWrite(13,LOW);
    }
  }

  //Serial.println("rom");
  delay(1000);
 
}
