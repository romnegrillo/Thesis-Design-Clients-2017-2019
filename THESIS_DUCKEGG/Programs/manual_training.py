import cv2
import os
import numpy as np

ctr=0
def train(path,name,textfile):
    global ctr
    
    imageList=os.listdir(path)
    
    #print(imageList)


    for (i,image) in enumerate(imageList):

        if "rgb" in image:
            frame=cv2.imread(path+image)

            
            bgr=frame

            # Grayscale
            gray=cv2.cvtColor(bgr,cv2.COLOR_BGR2GRAY)

            # Filter
            blur=cv2.medianBlur(gray,3)
            
            # CLAHE
            #clahe = cv2.createCLAHE(clipLimit=40.0, tileGridSize=(8,8))
            #claheImg = clahe.apply(gray)
            claheImg=blur

            y,x=frame.shape[:2]
            
            # Create mask 01/20/2019
            mask=np.zeros((y,x),np.uint8)
            cv2.ellipse(mask,(x//2,(y//2)+70),(135,200),0,0,360,255,-1)
            maskedClahe=cv2.bitwise_and(claheImg,claheImg,mask=mask)
            ########################
            
            t,thresh=cv2.threshold(maskedClahe,170,255,cv2.THRESH_BINARY_INV)

            thresh=cv2.bitwise_and(thresh,mask)

            #cv2.imshow(str(i),thresh)

            grayName=image.replace("rgb","gray")
            binaryName=image.replace("rgb","binary")

            if ctr==0:
                cv2.imshow("1",thresh)
            ctr=ctr+1
            print(str(cv2.countNonZero(thresh)))

            with open(textfile,"a") as f:
                f.write(name+","+str(cv2.countNonZero(thresh))+"\n")

            cv2.imwrite(path+grayName,blur)
            cv2.imwrite(path+binaryName,thresh)

train("./captured_images_balut_10days/","balut","training_records_10days.txt")
train("./captured_images_balut_14days/","balut","training_records_14days.txt")
train("./captured_images_abnoy_14days/","abnoy","training_records_14days.txt")   
train("./captured_images_penoy_10days/","penoy","training_records_10days.txt")


cv2.waitKey(0)
cv2.destroyAllWindows()
