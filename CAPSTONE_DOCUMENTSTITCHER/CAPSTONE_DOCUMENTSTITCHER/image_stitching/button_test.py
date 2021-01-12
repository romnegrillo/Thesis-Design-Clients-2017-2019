import RPi.GPIO as GPIO  
import time

buttonPin=2

GPIO.setmode(GPIO.BCM) 
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while 1:
        if  not (GPIO.input(buttonPin) == GPIO.HIGH):
            print("Pressed.")
        else:
            print("Not pressed.")

        time.sleep(1)
            
except Exception as exp:
    print(str(exp))
    
finally:
    GPIO.cleanup()
        

