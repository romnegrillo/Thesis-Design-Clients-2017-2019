import cv2
import os
import shutil
import glob

# 3 buttons.
# Power button for power supply.
# Button for USB hub for usb mode or scanning mode.
# Start button for starting the scanning. Check first if
# usb hub is in scanning mode. This can be done by
# counting the number of mounted directory.
# Check if the number of images in sd card of the scanners are equal.
# Copy the last two images and place it in images folder that will be for stitching.

# Onboot, motor will go back in the beginning.
# 2 limit switches.

# Constants for absolute directory name.
currentDirectory=os.path.dirname(os.path.abspath(__file__))
tempImageDirectory=currentDirectory+"/temp"
currentImageDirectory=currentDirectory+"/images"
outputDirectory=currentDirectory+"/outputs"
scanner1Dir=currentDirectory+"/scanner1"
scanner2Dir=currentDirectory+"/scanner2"

# Raspberry Pi used GPIO
def stitchImage(scanner1Dir,scanner2Dir,outputDIR):

    imageList=getImageFromTwoScanners(scanner1Dir,scanner2Dir)

    if len(imageList)==0:
        return

    stitcher = cv2.Stitcher_create()
    (status, stitched) = stitcher.stitch(imageList)

    # if the status is '0', then OpenCV successfully performed image
    # stitching
    if status == 0:
            # display the output stitched image to our screen
            cv2.imshow("Stitched", stitched)

            # write the output stitched image to disk

            # get number of output images first
            # to use as a basis for naming
            numOutputImages=countNumFiles(outputDirectory)

            outputName=outputDIR+"/output_"+str(numOutputImages+1)+".png"
            cv2.imwrite(outputName, stitched)

            deleteImage(currentImageDirectory)

            cv2.waitKey(0)

    # otherwise the stitching failed, likely due to not enough keypoints)
    # being detected
    else:
            print("Image stitching failed ({})".format(status))
            return 0

def countNumFiles(targetDIR):
    return len([name for name in os.listdir(targetDIR) if os.path.isfile(os.path.join(targetDIR, name))])

def deleteImage(targetDIR):
    folder = targetDIR
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

def getImageFromTwoScanners(scanner1, scanner2):
    scanner1Images=os.listdir(scanner1Dir)
    scanner2Images=os.listdir(scanner2Dir)

    scanner1Images.sort()
    scanner2Images.sort()

    imageList=[]

    print(scanner1Images)
    print(scanner2Images)

    if len(scanner1Images) == len(scanner2Images):
        image1=cv2.imread(scanner1Dir+"/"+scanner1Images[0])
        image2=cv2.imread(scanner2Dir+"/"+scanner2Images[0])


        imageList.append(image1)
        imageList.append(image2)

        return imageList
        cv2.imshow("image1",image1)
        cv2.imshow("image2",image2)

    else:
        return imageList

def moveMotorForward():
    pass

def moveMotorBackward():
    pass

# Test
#print(currentDirectory)
#print(tempImageDirectory)
#print(outputDirectory)
#print(countNumFiles(tempImageDirectory))
#deleteImage(currentImageDirectory)
#stitchImage(currentImageDirectory,outputDirectory)
#print(scanner1Dir)
#print(scanner2Dir)
#getImageFromTwoScanners(scanner1Dir,scanner2Dir)
stitchImage(scanner1Dir,scanner2Dir,outputDirectory)
