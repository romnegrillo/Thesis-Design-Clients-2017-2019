// Just some variables.

// Variable to store what data is being sent.
String dataIn;

// Variable indicate pin number 13 on the board.
int led = 3;

void setup()
{
  // Begin serial communication at 9600 baud rate.
  // Directly connected to dun sa USB port ng Arduino niyo
  // ot sa USB to TTL converted niyo sa Pro Mini, parehas lang yun.
  Serial.begin(9600);

  // Set the led pin as output.
  pinMode(led, OUTPUT);

  // Flush any waiting data in the serial port.
  Serial.flush();
}

void loop()
{
  // If statement to check if there is an
  // available data from the serial port.
  if (Serial.available())
  {
    // Read that data until \n.
    // the \n is used as a terminator to indicate
    // where to end the reading of data.
    // Remember in the Python program, we send
    // data that has \n in the end of the string.
    dataIn = Serial.readStringUntil("\n");

    // Compare that data if it is equal to Jezzamae\n
    if (dataIn == "Jezzamae\n")
    {
      // Do something if the data sent is 
      // equal to Jezzamae\n

      digitalWrite(led,HIGH);
      delay(500);
      digitalWrite(led, LOW);
      delay(500);
    }

    // Flush any waiting data in the serial port.
    Serial.flush();

    // Empty the dataIn variable
    dataIn = "";
  }

  // End of checking the serial port, it will loop
  // again to check for the available data and 
  // read it again.
}
