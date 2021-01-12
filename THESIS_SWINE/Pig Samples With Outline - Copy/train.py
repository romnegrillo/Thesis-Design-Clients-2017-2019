import cv2
import numpy as np
import os

basePath = "./Pig 5/"
outputPath = basePath+"outputs/"

imageList = [i for i in os.listdir(basePath) if ".jpg" in i]
imageList.sort()

with open(basePath+"/data.txt", "w") as f:
    pass

for inputImage in imageList:
    img = cv2.imread(basePath+inputImage)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower1 = (0, 70, 50)
    upper1 = (10, 255, 255)

    thresh1 = cv2.inRange(hsv, lower1, upper1)

    lower2 = (170, 70, 50)
    upper2 = (255, 255, 255)

    thresh2 = cv2.inRange(hsv, lower2, upper2)

    thresh = cv2.bitwise_or(thresh1, thresh2)

    k = np.ones((3,3), dtype = "uint8")
    thresh = cv2.dilate(thresh,k,iterations=3)


    y, x = thresh.shape[:2]
    yNew = 500
    xNew = int((x/y) * yNew)

    img = cv2.resize(img, (xNew, yNew))
    thresh = cv2.resize(thresh, (xNew, yNew))


    # Find contours.
    _, cnts, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # If there is atleast one contours.
    if len(cnts):

        # List for lengths of contours.
        cntsLen = []

        # Append all the length of cnts.
        for i in range(len(cnts)):
            cntsLen.append(len(cnts[i]))

        # Get the max length.
        maxIdxCnts = cntsLen.index(max(cntsLen))

        # Draw the max length contours on another mask.
        # Largest contours.
        maskBinary = np.zeros(thresh.shape[:2], dtype="uint8")
        maskCnts = np.zeros(thresh.shape[:2], dtype="uint8")
        maskBinaryEllipse = np.zeros(img.shape, dtype="uint8")

        cv2.drawContours(maskBinary, cnts, maxIdxCnts, (255), -1)
        cv2.drawContours(maskCnts, cnts, maxIdxCnts, (255), 2)
        cv2.drawContours(maskBinaryEllipse, cnts, maxIdxCnts, (255, 255, 255), -1)

        ellipse = cv2.fitEllipse(cnts[maxIdxCnts])
        (x, y), (ma, MA), angle = cv2.fitEllipse(cnts[maxIdxCnts])
        cv2.ellipse(maskBinaryEllipse, ellipse, (0, 0, 255), 3)

        numWhitePixels = cv2.countNonZero(maskBinary)
        totalPixels = img.shape[0]*img.shape[1]
        areaPercentage = (numWhitePixels/totalPixels)*100

        imageBGR = img
        maskBinary = maskBinary
        maskCnts = maskCnts

        # cv2.imshow("input",imageBGR)
        # cv2.imshow("binary",maskBinary)
        #cv2.imshow("contours", maskCnts)
        # cv2.imshow("ellipse",maskBinaryEllipse)

        cv2.imwrite(outputPath+"sample1_"+str(inputImage)+"_orig_resized.jpg", img)
        cv2.imwrite(outputPath+"sample1_"+str(inputImage)+"_binary.jpg", maskBinary)
        cv2.imwrite(outputPath+"sample1_"+str(inputImage)+"_cnts.jpg", maskCnts)
        cv2.imwrite(outputPath+"sample1_"+str(inputImage)+"_ellipse.jpg", maskBinaryEllipse)

        toWrite = str(inputImage)
        toWrite += ","
        toWrite += str(areaPercentage)
        toWrite += ","
        toWrite += str(MA)
        toWrite += ","
        toWrite += str(ma)

        toWrite += "\n"

        with open(basePath+"/data.txt", "a") as f:
            f.write(toWrite)

    #cv2.imshow("test", maskBinary)

cv2.waitKey(0)
cv2.destroyAllWindows()

