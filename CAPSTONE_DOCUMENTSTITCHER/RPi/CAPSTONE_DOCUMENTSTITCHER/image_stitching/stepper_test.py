import RPi.GPIO as GPIO
import time

M1CoilA1Pin=14
M1CoilA2Pin=15
M1CoilB1Pin=18
M1CoilB2Pin=23

M2CoilA1Pin=24
M2CoilA2Pin=25
M2CoilB1Pin=8
M2CoilB2Pin=7

GPIO.setmode(GPIO.BCM)

GPIO.setup(M1CoilA1Pin, GPIO.OUT)
GPIO.setup(M1CoilA2Pin, GPIO.OUT)
GPIO.setup(M1CoilB1Pin, GPIO.OUT)
GPIO.setup(M1CoilB2Pin, GPIO.OUT)

GPIO.setup(M2CoilA1Pin, GPIO.OUT)
GPIO.setup(M2CoilA2Pin, GPIO.OUT)
GPIO.setup(M2CoilB1Pin, GPIO.OUT)
GPIO.setup(M2CoilB2Pin, GPIO.OUT)

forwardSeq = ['1000', '1100', '0100', '0110', '0010','0011','0001','1001']
backwardSeq = forwardSeq.copy()
backwardSeq.reverse()

def setStep(step):
    GPIO.output(M1CoilA1Pin, step[0]=='1')
    GPIO.output(M1CoilA2Pin, step[1]=='1')
    GPIO.output(M1CoilB1Pin, step[2]=='1')
    GPIO.output(M1CoilB2Pin, step[3]=='1')

    GPIO.output(M2CoilA1Pin, step[0]=='1')
    GPIO.output(M2CoilA2Pin, step[1]=='1')
    GPIO.output(M2CoilB1Pin, step[2]=='1')
    GPIO.output(M2CoilB2Pin, step[3]=='1')

def turnOff():
    GPIO.output(M1CoilA1Pin, GPIO.LOW)
    GPIO.output(M1CoilA2Pin, GPIO.LOW)
    GPIO.output(M1CoilB1Pin, GPIO.LOW)
    GPIO.output(M1CoilB2Pin, GPIO.LOW)

    GPIO.output(M2CoilA1Pin, GPIO.LOW)
    GPIO.output(M2CoilA2Pin, GPIO.LOW)
    GPIO.output(M2CoilB1Pin, GPIO.LOW)
    GPIO.output(M2CoilB2Pin, GPIO.LOW)

def forward(steps):
    try:
        for i in range(steps):
            for step in forwardSeq:
                setStep(step)
                time.sleep(0.001)
    except:
        pass

def backward(steps):
    try:
        for i in range(steps):
            for step in backwardSeq:
                setStep(step)
                time.sleep(0.001)
    except:
        pass

backward(1000)
GPIO.cleanup()
