import cv2
import numpy as np
#from picamera import PiCamera
#from picamera.array import PiRGBArray
import time
from skimage.feature import peak_local_max
from skimage.morphology import watershed
from scipy import ndimage


class ImageProcessing(object):

    def __init__(self,usbcamera=0,rpicamera=None):

        self.usbcamera=usbcamera
        self.rpicamera=rpicamera
        
        if self.rpicamera is None:
            self.cap=cv2.VideoCapture(self.usbcamera)
            print("USB Camera Detected")
        else:
            self.camera = PiCamera()
            self.rawCapture = PiRGBArray(self.camera)
            print("RPi Camera Detected")
            time.sleep(0.1)
            
    def getImage(self):

        if self.rpicamera is None:
            ret,image=self.cap.read()
            #frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        else:
            self.camera.capture(self.rawCapture, format="bgr", use_video_port=True)
            image=self.rawCapture.array
            image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
            self.rawCapture.truncate(0)

        # Load the sample image.
        image=cv2.imread("./images/sample2.jpg")
        
        # Create a circle mask.
        mask=np.zeros((image.shape[:2]),np.uint8)
        (x,y)=mask.shape[1]//2,mask.shape[0]//2
        # Sample 1 radius = 275
        # Sample 2 radius = 286
        # Sample 3 radius = 90
        # Sample 4 radius = 180
        rad=286
        cv2.circle(mask,(x,y),rad,(255),-1)

        # Get ROI and set its background to white.
        # Note that this method works only if the background is
        # lighter than the colonies.
        # If the colonies are darker than the background, we
        # will repeat this code in the section below but
        # we set the background to black in the other case.
        imageROI=cv2.bitwise_and(image,image,mask=mask)
        imageROI[imageROI==0]=255
        #cv2.imshow("Input", imageROI)

        # Convert to grayscale, blur it
        # then apply Otsu's thresholding
        gray = cv2.cvtColor(imageROI, cv2.COLOR_BGR2GRAY)
        blurred=cv2.GaussianBlur(gray,(3,3),0)
        thresh = cv2.threshold(blurred, 0, 255,
                cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        # Bit AND the threshold with the circle mask
        # and count the number of non-zero pixels.
        threshMasked=cv2.bitwise_and(thresh,mask)
        countNonZeroInsideDish=cv2.countNonZero(threshMasked)
        #print(countNonZeroInsideDish)
        #cv2.imshow("Debug",threshMasked)
        targetPixels=200

# Uncomment the comment block below if the background of the petridish
# is lighter than the colonies.

##        # If there are at least targetPixels pixels, it means that
##        # the background is darker than the colonies, else
##        # vice-versa
##        if countNonZeroInsideDish>targetPixels:
##                pass
##        else:
##                # We repeat the same code above but we set the background
##                # to black.
##                imageROI=cv2.bitwise_and(image,image,mask=mask)
##                #cv2.imshow("Input", imageROI)
##
##                # Convert to grayscale, blur it
##                # then apply Otsu's thresholding
##                gray = cv2.cvtColor(imageROI, cv2.COLOR_BGR2GRAY)
##                blurred=cv2.GaussianBlur(gray,(3,3),0)
##                thresh = cv2.threshold(blurred, 0, 255,
##                        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]                       

        #cv2.imshow("Thresh", thresh)

        # Compute the exact Euclidean distance from every binary
        # Pixel to the nearest zero pixel, then find peaks in this
        # distance map
        D = ndimage.distance_transform_edt(thresh)
        localMax = peak_local_max(D, indices=False, min_distance=5,
                labels=thresh)

        # Perform a connected component analysis on the local peaks,
        # Using 8-connectivity, then appy the Watershed algorithm
        markers = ndimage.label(localMax, structure=np.ones((3, 3)))[0]
        labels = watershed(-D, markers, mask=thresh)
        self.colonyCount=len(np.unique(labels) - 1)

        # Loop over the unique labels returned by the Watershed
        # algorithm
        for label in np.unique(labels):
                # If the label is zero, we are examining the 'background'
                # so simply ignore it
                if label == 0:
                        continue

                # Otherwise, allocate memory for the label region and draw
                # it on the mask
                mask = np.zeros(gray.shape, dtype="uint8")
                mask[labels == label] = 255

                # Detect contours in the mask and grab the largest one
                cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)[-2]
                c = max(cnts, key=cv2.contourArea)

                # Draw a circle enclosing the object
                ((x, y), r) = cv2.minEnclosingCircle(c)
                cv2.circle(image, (int(x), int(y)), int(r), (0, 255, 0), 2)
                #cv2.putText(image, "#{}".format(label), (int(x) - 10, int(y)),
                #        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        # Show the output image
        #cv2.imshow("Output", image)

        image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        return image

    def getColonyCount(self):
        return self.colonyCount
        
    def closeCamera(self):

        if self.rpicamera is None:
            self.cap.release()

    def isCameraOpen(self):

        if self.rpicamera is None:
            return self.cap.isOpened()

    
