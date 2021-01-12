import time
from adafruit_servokit import ServoKit

class ServoControl:

    def __init__(self):
        self.kit=ServoKit(channels=16)

    def goDown(self):
        self.kit.servo[0].angle=10
        self.kit.servo[2].angle=10

    def goUp(self):
        self.kit.servo[0].angle=180
        self.kit.servo[2].angle=180

    

if __name__=="__main__":
    test=ServoControl()
    test.goUp()
    time.sleep(1)
    test.goDown()
    time.sleep(5)
    test.goUp()
    
