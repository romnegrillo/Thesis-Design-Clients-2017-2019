import cv2
import time
import servo_control
import dcmotor_control
import Adafruit_ADS1x15
import pygame
import image_processing
import depth_calib
import matplotlib.pyplot as plt
import threading
from matplotlib import ticker
import time

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
        #plt.imshow(img,cmap=plt.cm.gray)
        #plt.show()
        cv2.imshow("test",img)
        cv2.waitKey(1)

        if(imgObj.getLineNumPixels()>imgObj.getOneLineNumPixels() and
           imgObj.getLineNumPixels()<80000):
            
            if imgObj.getMovement()=="left":
                motorObj.left()
                time.sleep(0.1)
            elif imgObj.getMovement()=="right":
                motorObj.right()
                time.sleep(0.1)
                
            motorObj.stop()
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
            channelOne=depthCalibObj.getTargetValue(channelOne)
            timeNow = time.time()
            
            while(channelOne<1000):
                pass

            timeAfter=time.time()
            # In seconds
            totalTime = timeAfter-timeNow
           
            depth=(((totalTime*3.43)**2)-((3)**2))
            
            
            depthCalibObj.addDepth(depth)
            time.sleep(5)
            pygame.mixer.pause()
            servoObj.goUp()
            time.sleep(1)
        else:
            cv2.destroyAllWindows()
            print("No crack line detected or detected more than two crack lines.")
            break
    cv2.destroyAllWindows()
except KeyboardInterrupt as exp:
    #print(str(exp))
    unknown=True
except Exception as exp:
    #print(str(exp))
    unknown=True
finally:
 
    servoObj.goUp()
    motorObj.stop()
    pygame.mixer.pause()
    cv2.destroyAllWindows()
    imgObj.closeEverything()
 
if unknown:
    print("An unknown surface has been detected. Robot stopped.")
 
print("End of one line crack.")


    
        

