/*
   Assembly
   Connect panel to solar charger.
   Connect battery to solar charger.
   Connect output of solar charger to inverter.
   Measure resistance of the input in inverter.
*/

const int voltageSensorPin = A0;
const int panelRelay = A1;
const int powerSwitchRelay01 = A2;
const int powerSwitchRelay02 = A3;
const int dummyLoadPin = A4;

const int voltageThreshold = 12.2;
const int voltageExcess = 12.7;

void setup()
{
  Serial.begin(9600);

  pinMode(voltageSensorPin, INPUT);

  pinMode(panelRelay, OUTPUT);
  pinMode(powerSwitchRelay01, OUTPUT);
  pinMode(powerSwitchRelay02, OUTPUT);
  pinMode(dummyLoadPin, OUTPUT);
}


void loop()
{
  float voltage = getVoltage();
  String toSend = "";


  if (voltage <= voltageThreshold )
  {
    // Use house power, charge battery.
    digitalWrite(powerSwitchRelay01, LOW);
    digitalWrite(powerSwitchRelay02, LOW);
    digitalWrite(panelRelay, HIGH);

    toSend += "House Outlet,LOW";
  }
  else
  {
    // Use battery, don't charge panel.
    digitalWrite(powerSwitchRelay01, HIGH);
    digitalWrite(powerSwitchRelay02, HIGH);
    digitalWrite(panelRelay, LOW);

    if (voltage >= voltageExcess)
    {
      digitalWrite(dummyLoadPin, LOW);
    }
    else
    {
      digitalWrite(dummyLoadPin, HIGH);
    }

    toSend += "Battery, HIGH";
  }

  toSend += ",";
  toSend += String(voltage);  // From sensor.
  //toSend += ",";
  //  toSend += String(power);  // Add aerator and pump power.
  //  toSend += ",";
  //  toSend += String(kWh);  // Compute based from hours this is open.

  // Tosend: Power Source, Battery Status, Voltage, Power, Kilowathour
  // Update: Power Source, Battery Status, Voltage,
  toSend += ",";

  int excess = voltage - 12;

  if (excess > 0)
  {
    toSend += String(excess*1000);
  }
  else
  {
    toSend += String("0");
  }

  Serial.print(toSend);

  delay(1000);
}


float getVoltage()
{
  // Sensor is just a voltage divider.

  float reading = analogRead(voltageSensorPin);
  float R1 = 30000;
  float R2 = 7500;

  float voltage = reading * (5.0 / 1023.0) * ((R1 + R2) / R2);

  return voltage;


}
