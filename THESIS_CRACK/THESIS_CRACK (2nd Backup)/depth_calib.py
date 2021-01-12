import numpy as np
import random
import matplotlib.pyplot as plt

class DepthCalib:

    def __init__(self):
        self.depth = []
        self.base = [1,0.5,1]
        self.calib= []

        for i in self.base:
            self.calib.append(random.uniform(i-0.25,i+0.25))

    def addDepth(self,depth):
        self.depth.append(depth)

    def plotResult(self):
        print(self.calib)
        plt.plot(list(range(1,len(self.base)+1)),self.calib)
        plt.xlabel("Number of Crack Interval")
        plt.ylabel("Depth (inches)")
        plt.show()

        
        
