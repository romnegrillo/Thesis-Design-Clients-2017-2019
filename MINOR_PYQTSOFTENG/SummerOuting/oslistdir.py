import os
import cv2

pathsource=r"images/candidates/"
pathdest=r"images/candidates_resized/"

images=os.listdir(pathsource)
print(images)

for image in images:
    print(pathsource+image)
    img=cv2.imread(pathsource+image)
    resized=cv2.resize(img,(271,361),interpolation=cv2.INTER_AREA)
    cv2.imshow("test",resized)
    cv2.imwrite(pathdest+image, resized)
