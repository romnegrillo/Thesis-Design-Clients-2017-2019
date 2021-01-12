import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT)

try:
    while 1:
        GPIO.output(2, GPIO.LOW)
except:
    GPIO.output(2, GPIO.HIGH)

GPIO.cleanup()
