int ctr=0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.print("String1,String2,String3,String4,String5,String6,String7,String8,"+String(ctr)+","+String(ctr)+",4");
  ctr=ctr+1;
  delay(5000);
}
