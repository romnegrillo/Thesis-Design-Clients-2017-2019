import cv2
import numpy as np

# Get image, filter it and get threshold.
img=cv2.imread("./images/pig2.jpg")
gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
blurred=cv2.GaussianBlur(gray,(5,5),0)
t,thresh=cv2.threshold(blurred,240,255,
                       cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)


cv2.imshow("test",thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()

### Final image that containes the ROI.
##ROIFinal=cv2.bitwise_and(img,img,mask=thresh)
##cv2.imshow("wew",ROIFinal)
### Get the contours from the ROIMask.
##_,cnts,_=cv2.findContours(thresh.copy(),
##                          cv2.RETR_EXTERNAL,
##                          cv2.CHAIN_APPROX_SIMPLE)
##
### Draw contours around it with green color.
##cv2.drawContours(img,cnts,-1,(0,255,0),2)
##
### Create a list of which will contain the
### length of points of the countours detected.
##indC=[]
##
### Get all the length of contours.
##for (i,c) in enumerate(cnts):
##    indC.append(len(c))
##
### Find the index of the highest number of contours.
##indexLargestC=indC.index(max(indC))
##
### Get the rectangle around the contours.
##x,y,w,h=cv2.boundingRect(cnts[indexLargestC])
##
### Draw a rectangle around swine ROI mask.
##cv2.rectangle(ROIMask,(x,y),(x+w,y+h),(255),2)
##
### We will now get the center of the swine as a whole.
### The center of the swine will always be between its two
### pair of legs. We will use this information to
### find the Abdominal Circumference.
##
### The center of the swine, not needed to draw
### so it is commented.
###cv2.line(ROIMask,((x+w)//2,y),((x+w)//2,y+h),(0),2)
##
### Center of right rectangle.
##xNew=(x+w)//2
##yNew=y
##wNew=w
##hNew=h
###cv2.line(ROIMask,((xNew+wNew)//2,yNew),((xNew+wNew)//2,yNew+hNew),(0),2)
##
### Center of the left of right rectangle.
##xNew=xNew
##yNew=y
##wNew=(xNew+wNew)//2
##hNew=h
##cv2.line(ROIMask,((xNew+wNew)//2,yNew),((xNew+wNew)//2,yNew+hNew),(0),2)
##
##### Center of the left rectangle.
####xNew=x
####yNew=y
####wNew=(x+w)//2
####hNew=h
#####cv2.line(ROIMask,((xNew+wNew)//2,yNew),((xNew+wNew)//2,yNew+hNew),(0),2)
####
##### Center of the right rectangle of the left rectangle.
####xNew=(xNew+wNew)//2
####yNew=yNew
####wNew=(x+w)//2
####hNew=h
####cv2.line(ROIMask,((xNew+wNew)//2,yNew),((xNew+wNew)//2,yNew+hNew),(0),2)
##
### Horizontal center line.
##cv2.line(ROIMask,(x,(y+h)//2),(x+w,(y+h)//2),(0),2)
##
##percentDiff=[]
##found=False
##for j,i in enumerate(range(y+h-10,y,-2)):
##    origMaskCpy=origMask.copy()
##    cv2.line(origMaskCpy,(x,i),(x+w,i),(0),2)
##    inverse=cv2.bitwise_not(origMaskCpy)
##    origMaskCpy=cv2.bitwise_and(inverse,origMask)
##    percentDiff.append(cv2.countNonZero(origMaskCpy))
##
##    if i<(y+h):
##        diff=abs(((percentDiff[j]-percentDiff[j-1])/percentDiff[j-1])*100)
##        print(round(diff,2))
##        if diff > 20:
##            found=True
##        if found:
##            if diff<10:
##                break
##             
##
##
### Inverse of all the mask.
##inverseROI=cv2.bitwise_not(origMaskCpy)
##inverseROI=cv2.bitwise_and(inverseROI,origMask)
##
##wew=cv2.bitwise_not(origMaskCpy)
##wew=cv2.bitwise_and(wew,origMask)
##cv2.imshow("test",wew)
##                                    
##cv2.imshow("Contours",img)
##cv2.imshow("ROI Mask",ROIMask)
##    
##cv2.waitKey(0)
##cv2.destroyAllWindows()
##
