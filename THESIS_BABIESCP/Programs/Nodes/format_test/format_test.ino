void setup() 
{
  Serial.begin(9600);
}

void loop() 
{
  String format="NODE1,1,2,3,NODE2,4,5,6,NODE3,7,8,9,NODE4,10,11,12";
  Serial.println(format);

    delay(1000);
}
