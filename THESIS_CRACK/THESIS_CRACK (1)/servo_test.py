import servo_control
import time

servoObj = servo_control.ServoControl()
servoObj.goUp()
time.sleep(5)
servoObj.goDown()
time.sleep(5)
servoObj.goUp()
