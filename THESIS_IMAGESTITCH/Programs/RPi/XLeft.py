import RPi.GPIO as GPIO
import time

coilA1Pin=3
coilA2Pin=18
coilB1Pin=27
coilB2Pin=22

GPIO.setmode(GPIO.BCM)
GPIO.setup(coilA1Pin, GPIO.OUT)
GPIO.setup(coilA2Pin, GPIO.OUT)
GPIO.setup(coilB1Pin, GPIO.OUT)
GPIO.setup(coilB2Pin, GPIO.OUT)

forwardSeq = ['1010', '0110', '0101', '1001']

def setStep(step):
    GPIO.output(coilA1Pin, step[0]=='1')
    GPIO.output(coilA2Pin, step[1]=='1')
    GPIO.output(coilB1Pin, step[2]=='1')
    GPIO.output(coilB2Pin, step[3]=='1')

def turnOff():
    GPIO.output(coilA1Pin, GPIO.LOW)
    GPIO.output(coilA2Pin, GPIO.LOW)
    GPIO.output(coilB1Pin, GPIO.LOW)
    GPIO.output(coilB2Pin, GPIO.LOW)

try:
    for i in range(35):
        for step in forwardSeq:
            setStep(step)
            time.sleep(0.01)
except:
    pass
finally:
    turnOff()
    GPIO.cleanup()


