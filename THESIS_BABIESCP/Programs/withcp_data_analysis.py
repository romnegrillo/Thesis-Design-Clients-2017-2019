from matplotlib import pyplot as plt
import os
import csv
import numpy as np

root = "./with_cp/"
csvFiles = [i for i in os.listdir(root) if ".csv" in i]
# print(csvFiles)

leftArmSummary = []
rightArmSummary = []
leftLegSummary = []
rightLegSummary = []
ctr = 0

for csvFile in csvFiles:
    # Read rows of the CSV as lists.
    with open(root+csvFile, "r") as csvFile:
        readCSV = csv.reader(csvFile, delimiter=',')
        data = list(readCSV)
        data = data[1:]

        timeList = []
        leftArmList = []
        rightArmList = []
        leftLegList = []
        rightLegList = []

        for d in data:
            timeList.append(d[0])
            leftArmList.append(float(d[1]))
            rightArmList.append(float(d[2]))
            leftLegList.append(float(d[3]))
            rightLegList.append(float(d[4]))

    # print(leftArmList)

    leftArmVar = np.var(leftArmList)
    rightArmVar = np.var(rightArmList)
    leftLegVar = np.var(leftLegList)
    rightLegVar = np.var(rightLegList)

    leftArmSummary.append(leftArmVar)
    rightArmSummary.append(rightArmVar)
    leftLegSummary.append(leftLegVar)
    rightLegSummary.append(rightLegVar)

    print("==========================================")
    print(f'Left Arm var: {leftArmVar}')
    print(f'Right Arm var: {rightArmVar}')
    print(f'Left Leg var: {leftLegVar}')
    print(f'Right Leg var: {rightLegVar}')
    print("==========================================")

    accel = "LOW"

    if not ((leftArmVar > 0.03) or not (rightArmVar > 0.03)) and (not(leftLegVar > 0.0050) or not(rightLegVar > 0.0050)):
        accel = "LOW"
    elif ((leftArmVar >= 0.03) or (rightArmVar >= 0.03)) and ((leftLegVar >= 0.0050) or (rightLegVar >= 0.0050)):
        accel = "HIGH"

    if accel == "HIGH":
        ctr = ctr+1
    elif accel == "LOW":
        pass


print("==========================================")
print("DATA SUMMARY WITH SIGNS OF CP")
print("Variance of each nodes of all babies.")
print("==========================================")
print(f'Left Arm')
print(f'\tmax var: {np.max(leftArmSummary)}\n\tmin var: {np.min(rightArmSummary)}')
print(f'Right Arm')
print(f'\tmax var: {np.max(rightArmSummary)}\n\tmin var: {np.min(rightArmSummary)}')
print(f'Left Leg')
print(f'\t max var: {np.max(leftLegSummary)}\n\tmin var: {np.min(leftLegSummary)}')
print(f'Left Leg')
print(f'\t max var: {np.max(rightLegSummary)}\n\tmin var: {np.min(rightLegSummary)}')
print("==========================================")
print(ctr)
