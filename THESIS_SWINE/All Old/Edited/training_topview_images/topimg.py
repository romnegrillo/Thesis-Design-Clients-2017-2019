import cv2
import numpy as np
import os

fileList=os.listdir() 


for index,file in enumerate(fileList):
    
    if file.endswith(".jpg"):   

        img=cv2.imread(file)
        #cv2.imshow("img",img)
        
        hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        #cv2.imshow("hsv",hsv)

        upper=(0,40,90)
        lower=(40,255,255)

        binary=cv2.inRange(hsv,upper,lower)
        k=np.ones((3,3),dtype="uint8")
        binary=cv2.erode(binary,k,iterations=10)
        binary=cv2.dilate(binary,k,iterations=10)
        #cv2.imshow("binary",binary)

        _,cnts,_=cv2.findContours(binary,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        cntsLen=[]
        
        for i,c in enumerate(cnts):
            cntsLen.append(len(c))


        if cntsLen!=0:

            indexLargest=cntsLen.index(max(cntsLen))
            
            cntsLen.sort(reverse=True)
            
            cntsMask=np.zeros(img.shape[:2],dtype="uint8")
            cv2.drawContours(cntsMask,cnts,indexLargest,(255),3)

            binaryMask=np.zeros(img.shape[:2],dtype="uint8")
            cv2.drawContours(binaryMask,cnts,indexLargest,(255),-1)
            
            #cv2.imshow(file.replace("rgb","cnts"),cntsMask)
            #cv2.imshow(file.replace("rgb","binary"),binaryMask)
             
            cv2.imwrite(file.replace("rgb","cnts"),cntsMask)
            cv2.imwrite(file.replace("rgb","binary"),binaryMask)

cv2.waitKey(0)
cv2.destroyAllWindows()
