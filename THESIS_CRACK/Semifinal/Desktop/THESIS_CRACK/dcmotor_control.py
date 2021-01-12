import board
import busio
import adafruit_pca9685
import time
import servo_control


class DCMotorControl:

    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.hat = adafruit_pca9685.PCA9685(self.i2c)
        #self.hat.frequency=2000

        self.left_motor = self.hat.channels[15]
        self.right_motor = self.hat.channels[14]


    def forward(self):
        self.left_motor.duty_cycle = 26000
        self.right_motor.duty_cycle = 26000

    def left(self):
        self.left_motor.duty_cycle = 0
        self.right_motor.duty_cycle = 26000

    def right(self):
        self.left_motor.duty_cycle = 26000
        self.right_motor.duty_cycle = 0

    def stop(self):
        self.left_motor.duty_cycle = 0
        self.right_motor.duty_cycle = 0

if __name__=="__main__":
    motorObj=DCMotorControl()
    servoObj=servo_control.ServoControl()
    servoObj.goUp()
    motorObj.forward()
    time.sleep(0.2)
    motorObj.stop()
