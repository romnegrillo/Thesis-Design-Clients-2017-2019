void setup() 
{
  Serial.begin(9600);
  
}

void loop() 
{
 String format = "node1,1,2,3,";
 format+="node2,4,5,6,";
 format+="node3,7,8,9,";
 format+="node4,10,11,12";

 Serial.println(format);

 delay(1000);

}
