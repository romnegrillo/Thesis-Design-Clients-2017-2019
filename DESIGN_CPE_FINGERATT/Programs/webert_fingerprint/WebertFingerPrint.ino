#include <Adafruit_Fingerprint.h>

#include <SoftwareSerial.h>
SoftwareSerial mySerial(2, 3);

Adafruit_Fingerprint finger = Adafruit_Fingerprint(&mySerial);
int fingerList[4];
int fingerListToDelete[4];
int currentRegistering=0;
uint8_t id;
int readModeLed=13;
int deleteModeLed=9;

void setup()  
{
  Serial.begin(9600);
  
  //while (!Serial); 

  //delay(100);
  //Serial.println("Adafruit Fingerprint sensor enrollment");
  
  finger.begin(57600);
  
  if (finger.verifyPassword()) 
  {
    //Serial.println("Found fingerprint sensor!");
  } else 
  {
    Serial.println("Did not find fingerprint sensor :(");
    while (1) { delay(1); }
  }

  Serial.flush();

  pinMode(readModeLed, OUTPUT);
  pinMode(deleteModeLed, OUTPUT);
}
void(* resetFunc)(void) = 0;

void loop()                     
{
  getFingerprintIDez();
  digitalWrite(readModeLed, HIGH);
  
  if(Serial.available())
  {
    digitalWrite(readModeLed, LOW);
  
    String inData=Serial.readStringUntil(',');
    Serial.println(inData);
    
    if(inData.indexOf("ENROLLMODE")>-1)
    {
      for(int i=0; i<4; i++)
      {
        fingerList[i]=Serial.parseInt();
      }

      //Serial.println("Finger 1: " + String(fingerList[0]));
      //Serial.println("Finger 2: " + String(fingerList[1]));
      //Serial.println("Finger 3: " + String(fingerList[2]));
      //Serial.println("Finger 4: " + String(fingerList[3]));

      enrollMode(fingerList);

      Serial.println("ENROLL MODE DONE");
  
    }
    else if(inData.indexOf("DELETEMODE")>-1)
    {
      for(int i=0; i<4; i++)
      {
        fingerListToDelete[i]=Serial.parseInt();
      }

      //Serial.println("Finger 1: " + String(fingerListToDelete[0]));
      //Serial.println("Finger 2: " + String(fingerListToDelete[1]));
      //Serial.println("Finger 3: " + String(fingerListToDelete[2]));
      //Serial.println("Finger 4: " + String(fingerListToDelete[3]));

      deleteMode(fingerListToDelete);
       Serial.flush();
    }
    else if(inData.indexOf("RESET")>-1)
    {
      digitalWrite(deleteModeLed, HIGH);
      digitalWrite(readModeLed, LOW);
      finger.emptyDatabase();
      Serial.println("All finger prints deleted!");
      digitalWrite(deleteModeLed, LOW);
       Serial.flush();
    }
  }
 Serial.flush();
  delay(1000);
}

void enrollMode(int fingerIDs[])
{   
  while(true)
  {
    if(currentRegistering==4)
    {
      currentRegistering=0;
      break;
    }

    id=fingerIDs[currentRegistering];

    if(id==0)
    {
      currentRegistering=0;
      break;
    }
    
    deleteFingerprint(id);
    getFingerprintEnroll(); 

    delay(1000);
  }
}

void deleteMode(int fingerIDs[])
{
  for(int i=0; i<4; i++)
  {
    if(fingerIDs[i]==0)
    {
      break;
    }
    
    deleteFingerprint(fingerIDs[i]);
  }

  Serial.println("DELETE MODE DONE");
}

uint8_t getFingerprintEnroll() 
{

  int p = -1;
  Serial.println("Waiting for finger...");
  while (p != FINGERPRINT_OK) {
    p = finger.getImage();
    switch (p) {
    case FINGERPRINT_OK:
      Serial.println("Image taken");
      break;
    case FINGERPRINT_NOFINGER:
      //Serial.println(".");
      break;
    case FINGERPRINT_PACKETRECIEVEERR:
      Serial.println("Communication error");
      break;
    case FINGERPRINT_IMAGEFAIL:
      Serial.println("Imaging error");
      break;
    default:
      Serial.println("Unknown error");
      break;
    }
  }

  // OK success!

  p = finger.image2Tz(1);
  switch (p) {
    case FINGERPRINT_OK:
      //Serial.println("Image converted");
      break;
    case FINGERPRINT_IMAGEMESS:
      Serial.println("Image too messy");
      return p;
    case FINGERPRINT_PACKETRECIEVEERR:
      Serial.println("Communication error");
      return p;
    case FINGERPRINT_FEATUREFAIL:
      Serial.println("Could not find fingerprint features");
      return p;
    case FINGERPRINT_INVALIDIMAGE:
      Serial.println("Could not find fingerprint features");
      return p;
    default:
      Serial.println("Unknown error");
      return p;
  }
  
  Serial.println("Remove finger");
  delay(1000);
  p = 0;
  while (p != FINGERPRINT_NOFINGER) {
    p = finger.getImage();
  }
  //Serial.print("ID "); Serial.println(id);
  p = -1;
  Serial.println("Place same finger again");
  while (p != FINGERPRINT_OK) {
    p = finger.getImage();
    switch (p) {
    case FINGERPRINT_OK:
      //Serial.println("Image taken");
      break;
    case FINGERPRINT_NOFINGER:
      //Serial.print(".");
      break;
    case FINGERPRINT_PACKETRECIEVEERR:
      Serial.println("Communication error");
      break;
    case FINGERPRINT_IMAGEFAIL:
      Serial.println("Imaging error");
      break;
    default:
      Serial.println("Unknown error");
      break;
    }
  }

  // OK success!

  p = finger.image2Tz(2);
  switch (p) {
    case FINGERPRINT_OK:
      //Serial.println("Image converted");
      break;
    case FINGERPRINT_IMAGEMESS:
      Serial.println("Image too messy");
      return p;
    case FINGERPRINT_PACKETRECIEVEERR:
      Serial.println("Communication error");
      return p;
    case FINGERPRINT_FEATUREFAIL:
      Serial.println("Could not find fingerprint features");
      return p;
    case FINGERPRINT_INVALIDIMAGE:
      Serial.println("Could not find fingerprint features");
      return p;
    default:
      Serial.println("Unknown error");
      return p;
  }
  
  // OK converted!
 // Serial.print("Creating model for #");  Serial.println(id);
  
  p = finger.createModel();
  if (p == FINGERPRINT_OK) {
    Serial.println("Prints matched!");
  } else if (p == FINGERPRINT_PACKETRECIEVEERR) {
    Serial.println("Communication error");
    return p;
  } else if (p == FINGERPRINT_ENROLLMISMATCH) {
    Serial.println("Fingerprints did not match");
    return p;
  } else {
    Serial.println("Unknown error");
    return p;
  }   
  
  //Serial.print("ID "); Serial.println(id);
  p = finger.storeModel(id);
  if (p == FINGERPRINT_OK) {
    Serial.println("Stored!");
    currentRegistering++;
      p = 0;
  while (p != FINGERPRINT_NOFINGER) {
    p = finger.getImage();
  }

  } else if (p == FINGERPRINT_PACKETRECIEVEERR) {
    Serial.println("Communication error");
    return p;
  } else if (p == FINGERPRINT_BADLOCATION) {
    Serial.println("Could not store in that location");
    return p;
  } else if (p == FINGERPRINT_FLASHERR) {
    Serial.println("Error writing to flash");
    return p;
  } else {
    Serial.println("Unknown error");
    return p;
  }   
}

uint8_t deleteFingerprint(uint8_t id) {
  uint8_t p = -1;
  
  p = finger.deleteModel(id);

  if (p == FINGERPRINT_OK) {
    //Serial.println("Deleted!");
  } else if (p == FINGERPRINT_PACKETRECIEVEERR) {
    Serial.println("Communication error");
    return p;
  } else if (p == FINGERPRINT_BADLOCATION) {
    Serial.println("Could not delete in that location");
    return p;
  } else if (p == FINGERPRINT_FLASHERR) {
    Serial.println("Error writing to flash");
    return p;
  } else {
    Serial.print("Unknown error: 0x"); Serial.println(p, HEX);
    return p;
  }   
}

int getFingerprintIDez() {
  uint8_t p = finger.getImage();
  if (p != FINGERPRINT_OK)  return -1;

  p = finger.image2Tz();
  if (p != FINGERPRINT_OK)  return -1;

  p = finger.fingerFastSearch();
  if (p != FINGERPRINT_OK)  {
    Serial.println("Finger print not recognized.");
    return -1;
  }
  
  // found a match!
  Serial.println("INCOMINGFINGER:" + String(finger.fingerID)); //Serial.print(finger.fingerID); 
  //Serial.print(" with confidence of "); Serial.println(finger.confidence);

  while (p != FINGERPRINT_NOFINGER) {
    p = finger.getImage();
  }
  return finger.fingerID; 
}
