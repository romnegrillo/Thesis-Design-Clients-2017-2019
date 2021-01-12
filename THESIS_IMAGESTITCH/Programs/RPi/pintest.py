IN1=3
IN2=18
IN3=27
IN4=22

IN5=23
IN6=10
IN7=9
IN8=25

L1=11
L2=8
L3=7

import RPi.GPIO as GPIO
import time

pinTest=IN8

GPIO.setmode(GPIO.BCM)
GPIO.setup(pinTest, GPIO.OUT)
GPIO.setup(L1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(L2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(L3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

try:
    for i in range(0,25):
        print("Blinking")
        GPIO.output(IN8,1)
        time.sleep(1)
        print("L1: {}".format(GPIO.input(L1)))
        print("L2: {}".format(GPIO.input(L2)))
        print("L3: {}".format(GPIO.input(L3)))
except:
    pass

GPIO.output(pinTest, GPIO.LOW)
GPIO.cleanup()
print("Done Testing")



