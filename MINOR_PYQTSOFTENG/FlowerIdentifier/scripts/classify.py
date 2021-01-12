from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report
import numpy as np
import cv2
import os
from rgbhistogram import RGBHistogram

data=[]
target=[]

imagePaths=os.getcwd()+"\\images"
maskPaths=os.getcwd()+"\\masks"

imagePaths=os.listdir(imagePaths)
maskPaths=os.listdir(maskPaths)

desc=RGBHistogram([8, 8, 8])

for (imagePath,maskPath) in zip(imagePaths,maskPaths):
    image=cv2.imread("images/"+imagePath)
    mask=cv2.imread("masks/"+maskPath)
    mask=cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

    features=desc.describe(image, mask)

    data.append(features)
    target.append(imagePath.split("_")[-2])


targetNames=np.unique(target)
le=LabelEncoder()
target=le.fit_transform(target)

(trainData, testData, trainTarget, testTarget)=train_test_split(data, target,
                                                                test_size=0.3,random_state=42)
model=RandomForestClassifier(n_estimators=25, random_state=84)
model.fit(trainData, trainTarget)

print(classification_report(testTarget, model.predict(testData), target_names=targetNames))

imagePath="images/"+imagePaths[233]
#maskPath="masks/"+maskPaths[1]

image=cv2.imread(imagePath)
#mask=cv2.imread(maskPath)
#mask=cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

features=desc.describe(image)

flower=le.inverse_transform(model.predict([features]))[0]

print("I think this flower is: {}".format(flower.upper()))
cv2.imshow("image", image)

cv2.waitKey(0)
