
import time
import servo_control
import dcmotor_control
import Adafruit_ADS1x15
import pygame
import image_processing
import depth_calib

motorObj=dcmotor_control.DCMotorControl()
servoObj=servo_control.ServoControl()

adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1

pygame.init()
my_sound=pygame.mixer.Sound("./audio_files/vibration_final.ogg")

imgObj=image_processing.ImageProcessing(3)
depthCalibObj=depth_calib.DepthCalib()


try:
    for i in range(depthCalibObj.getLen()):
        servoObj.goUp()
        motorObj.forward()
        time.sleep(0.1)
        motorObj.stop()
        time.sleep(1)
        servoObj.goDown()
        pygame.mixer.unpause()
        my_sound.play()
        time.sleep(1)
        channelOne=adc.read_adc(0, gain=GAIN)
        depthCalibObj.addDepth(channelOne)
        time.sleep(5)
        pygame.mixer.pause()
        servoObj.goUp()
        time.sleep(1)
except:
    servoObj.goUp()
    motorObj.stop()
    pygame.mixer.pause()

depthCalibObj.plotResult()
        

