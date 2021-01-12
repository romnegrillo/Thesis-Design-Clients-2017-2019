import time

import board
import busio
import adafruit_pca9685
i2c = busio.I2C(board.SCL, board.SDA)
hat = adafruit_pca9685.PCA9685(i2c)

hat.frequency=2000

left_motor = hat.channels[15]
right_motor = hat.channels[14]

left_motor.duty_cycle = 0
right_motor.duty_cycle =  0
