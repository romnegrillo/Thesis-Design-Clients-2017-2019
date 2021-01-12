import matplotlib.pyplot as plt
from matplotlib import ticker
import csv
import numpy as np

plt.switch_backend('Qt5Agg')


class BabiesFuzzy:

    def __init__(self):

        self.timeList = []
        self.leftArmList = []
        self.rightArmList = []
        self.leftLegList = []
        self.rightLegList = []

    def readCSV(self, fileName):
        rowList = []

        # Read rows of the CSV as lists.
        with open(fileName, "r") as csvFile:
            readCSV = csv.reader(csvFile, delimiter=',')

            for row in readCSV:
                rowList.append(row)

        if len(rowList) > 0:

            self.timeList = []
            self.leftArmList = []
            self.rightArmList = []
            self.leftLegList = []
            self.rightLegList = []

            cnt = 0

            for row in rowList:

                if cnt > 0:
                    self.timeList.append(row[0])
                    self.leftArmList.append(float(row[1]))
                    self.rightArmList.append(float(row[2]))
                    self.leftLegList.append(float(row[3]))
                    self.rightLegList.append(float(row[4]))

                cnt = cnt+1

            xValue = list(range(0, len(self.timeList)))
            leftArmVar = np.var(self.leftArmList)
            rightArmVar = np.var(self.rightArmList)
            leftLegVar = np.var(self.leftLegList)
            rightLegVar = np.var(self.rightLegList)

            print(leftArmVar, rightArmVar, leftLegVar, rightLegVar)

            accel = "LOW"

            if not ((leftArmVar > 0.03) or not (rightArmVar > 0.03)) and (not(leftLegVar > 0.0050) or not(rightLegVar > 0.0050)):
                accel = "LOW"
            elif ((leftArmVar >= 0.03) or (rightArmVar >= 0.03)) and ((leftLegVar >= 0.0050) or (rightLegVar >= 0.0050)):
                accel = "HIGH"

            if accel == "HIGH":
                self.cpClassificationLabel = "With signs of CP."
            elif accel == "LOW":
                self.cpClassificationLabel = "Without signs of CP."

            plt.title("Data of 4 Nodes")
            plt.xlabel("Time")
            plt.ylabel("Weight of Each Nodes")
            plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(5))
            plt.plot(xValue, self.leftArmList)
            plt.plot(xValue, self.rightArmList)
            plt.plot(xValue, self.leftLegList)
            plt.plot(xValue, self.rightLegList)
            plt.legend(["Left Arm", "Right Arm", "Left Leg", "Right Leg"])

            # print(self.leftArmList)

            # figManager = plt.get_current_fig_manager()
            # figManager.window.showMaximized()

            plt.show()

            return 1

        else:

            return 0

    def getClassification(self):
        return self.cpClassificationLabel

    def closeAllPlots(self):
        plt.close("all")


if __name__ == "__main__":
    test = BabiesFuzzy()
