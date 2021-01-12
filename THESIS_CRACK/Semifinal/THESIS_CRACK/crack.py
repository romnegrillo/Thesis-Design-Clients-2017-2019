import cv2
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

fordInterval=0.2
unknown=False

ctr=0

try:
    for i in range(depthCalibObj.getLen()):

        while ctr<5:
            img=imgObj.getImage()
            cv2.imshow("test",img)
            ctr=ctr+1
            cv2.waitKey(1)

        img=imgObj.getImage()
        cv2.imshow("test",img)
        cv2.waitKey(1)
            
        servoObj.goUp()
        motorObj.forward()
        time.sleep(fordInterval)
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
    unknown=True
     

if not unknown:
    depthCalibObj.plotResult()
else:
    print("An unknown surface has been detected. Robot stopped.")
    depthCalibObj.plotResult()

cv2.destroyAllWindows()
    
        

