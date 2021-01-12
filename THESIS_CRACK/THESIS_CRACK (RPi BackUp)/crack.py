import time
import servo_control
import dcmotor_control
import Adafruit_ADS1x15
import crack_calibration

motorObj=dcmotor_control.DCMotorControl()
servoObj=servo_control.ServoControl()
adc = Adafruit_ADS1x15.ADS1015(address=0x48, busnum=1)
GAIN = 1
crackObj=crack_calibration.CrackCalib()


for i in range(3):
    servoObj.goUp()
    motorObj.forward()
    time.sleep(0.2)
    motorObj.stop()
    time.sleep(1)
    servoObj.goDown()
    time.sleep(5)
    servoObj.goUp()
    time.sleep(1)

    channelOne=adc.read_adc(0, gain=GAIN)
    depth=crackObj.getDepth(channelOne)
    print(depth)
