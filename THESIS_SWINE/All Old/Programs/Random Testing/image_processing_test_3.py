import cv2

def drawCenterLine(img,x,y,w,h):
    cv2.line(img,(x,y),(w,h),(0),1)

# Get image.
img=cv2.imread(r"./images/pig2.jpg")
cv2.imshow("Input",img)

# Convert image to grayscale.
gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
cv2.imshow("Grayed",gray)

# Get the threshold values in otsu thresholding
# to be used as upper and lower boundaries
# in canny edge detector.
upperThresh,thresh=cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV +
                                cv2.THRESH_OTSU)
# Half or the otsu thresh.
lowerThresh=(0.5)*upperThresh

cv2.imshow("Threshold",thresh)

# Use canny edge detector.
edges=cv2.Canny(gray,lowerThresh,upperThresh)
cv2.imshow("Edges",edges)

# Dilate to expand 1's.
dilate=cv2.dilate(edges,None,iterations=1)
cv2.imshow("Dilated",dilate)

# Copy the dilated image to be used in contours.
mask=dilate.copy()

# Detect contours.
_,cnts,_=cv2.findContours(mask,cv2.RETR_EXTERNAL,
                          cv2.CHAIN_APPROX_SIMPLE)
# Fill the contours with 1's
cv2.drawContours(mask,cnts,-1,(255),-1)

# Create a list to find the lengths of contours,
# sort it and find the largest contour.
cntsLenList=[]

for i in cnts:
    cntsLenList.append(len(i))

largestC=cntsLenList.index(max(cntsLenList))

# Draw the largest contours on the copied original image.
imgToDisplay=img.copy()
cv2.drawContours(imgToDisplay,cnts,largestC,(255,0,0),2)
cv2.imshow("Contours",imgToDisplay)

# Erode after dilate to bring the normal size of binary image.
mask=cv2.erode(mask,None,iterations=1)

# OR the threshold to the eroded mask
# to add the missed white pixels from the ROI.
maskFinal=cv2.bitwise_or(mask,thresh)
cv2.imshow("Mask",mask)

# Now to remove the excess, AND the mask with the original
# mask.
maskFinal=cv2.bitwise_and(maskFinal,mask)
cv2.imshow("Final Mask",maskFinal)

# Mask the original image.
masked=cv2.bitwise_and(img,img,mask=maskFinal)
cv2.imshow("Masked",masked)

# Draw rectangle on the largest contour (Swine)
x,y,w,h=cv2.boundingRect(cnts[largestC])
#cv2.rectangle(maskFinal,(x,y),(x+w,y+h),(255),1)
cv2.imshow("Final Mask",maskFinal)

imageWidth=maskFinal.shape[1]
imageLength=maskFinal.shape[0]

# Get center of the rectangle.
firstLine=maskFinal.copy()
xL=x
yL=(y+h)//3+((y+h)//3)
wL=x+w
hL=(y+h)//3+((y+h)//3)


firstLine=maskFinal.copy()
drawCenterLine(firstLine,xL,yL,wL,hL)
xL=x
yL=int((y+h)//4+2.5*((y+h)//4))
wL=x+w
hL=int((y+h)//4+2.5*((y+h)//4))
#drawCenterLine(firstLine,xL,yL,wL,hL)

firstPointFound=False
firstPoint=[]
lastPoint=[]
for i in range(0,imageWidth):
    targetPixel=firstLine[yL,i]

    if targetPixel==255 and not firstPointFound:
        firstPoint=(yL,i)
        firstPointFound=True
    else:
        lastPoint=(yL,i)
        
print(firstPoint)
print(lastPoint)
midPoint=lastPoint[1]-firstPoint[1]
drawCenterLine(firstLine,firstPoint[1],y,firstPoint[1],y+h)
drawCenterLine(firstLine,midPoint,y,midPoint,h)
cv2.imshow("First Line", firstLine)

cv2.waitKey(0)
cv2.destroyAllWindows()
