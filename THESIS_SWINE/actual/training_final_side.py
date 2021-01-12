import cv2
import numpy as np
import os

basePath = "./swine_allside/"
outputPath = basePath+"outputs/"

imageList = [i for i in os.listdir(basePath) if ".jpg" in i]
print(imageList)

with open("topview_data.txt", "w") as f:
    pass

for inputImage in imageList:
    print(inputImage)
    image = cv2.imread(basePath+inputImage)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use otsu thresholding to get the high and low
    # threshold value to be used in Canny edge detector.
    t, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV +
                              cv2.THRESH_OTSU)

    # Perform dilation and erosion
    dilated = cv2.dilate(thresh, None, iterations=1)
    eroded = cv2.erode(dilated, None, iterations=1)

    # Find contours.
    _, cnts, _ = cv2.findContours(eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

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
        maskBinary = np.zeros(image.shape[:2], dtype="uint8")
        maskCnts = np.zeros(image.shape[:2], dtype="uint8")
        maskBinaryEllipse = np.zeros(image.shape, dtype="uint8")

        cv2.drawContours(maskBinary, cnts, maxIdxCnts, (255), -1)
        cv2.drawContours(maskCnts, cnts, maxIdxCnts, (255), 2)
        cv2.drawContours(maskBinaryEllipse, cnts, maxIdxCnts, (255, 255, 255), -1)

        ellipse = cv2.fitEllipse(cnts[maxIdxCnts])
        (x, y), (ma, MA), angle = cv2.fitEllipse(cnts[maxIdxCnts])
        cv2.ellipse(maskBinaryEllipse, ellipse, (0, 0, 255), 3)

        numWhitePixels = cv2.countNonZero(maskBinary)
        totalPixels = image.shape[0]*image.shape[1]
        areaPercentage = (numWhitePixels/totalPixels)*100

        imageBGR = image
        maskBinary = maskBinary
        maskCnts = maskCnts

        # cv2.imshow("input",imageBGR)
        # cv2.imshow("binary",maskBinary)
        #cv2.imshow("contours", maskCnts)
        # cv2.imshow("ellipse",maskBinaryEllipse)

        cv2.imwrite(outputPath+str(inputImage).replace("rgb","binary"), maskBinary)
        cv2.imwrite(outputPath+str(inputImage).replace("rgb","cnts"), maskCnts)
        cv2.imwrite(outputPath+str(inputImage).replace("rgb","ellipse"), maskBinaryEllipse)

        toWrite = str(inputImage)
        toWrite += ","
        toWrite += str(areaPercentage)
        toWrite += ","
        toWrite += str(MA)
        toWrite += ","
        toWrite += str(ma)

        toWrite += "\n"

        with open("sideview_data.txt", "a") as f:
            f.write(toWrite)
