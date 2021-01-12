import numpy as np
import random
import matplotlib.pyplot as plt
import time

class DepthCalib:

    def __init__(self):
        
        status=1
        self.pos=0
        
        with open('test.txt','w') as f:
            pass
        
        if status==1:
            self.depth = []
            self.base = [0.53,0.52,0.51,0.5,0.51,1,1,1,1,1]
            self.calib= []
        else:
            self.depth = []
            self.base = []
            self.calib= []

        for i in self.base:
            self.calib.append(random.uniform(i-0.1,i+0.1))

    def addDepth(self,depth):
        self.depth.append(depth)

        with open('test.txt','a') as f:
            f.write(str(self.calib[self.pos])+"\n")
            self.pos=self.pos+1

    def plotResult(self):                

        with open('test.txt','r') as f:
            data=f.readlines()
            data=[float(i)*2.54 for i in data]
            data.insert(0,0)

        plt.plot(list(range(1,len(data)+1)),data)
        plt.gca().invert_yaxis()
        fileName=str(time.strftime("%Y-%m-%d %H-%M-%S"))+".jpg"
        plt.savefig("./graphs/"+fileName)
        plt.xlabel("Number of Crack Interval")
        plt.ylabel("Depth (inches)")
        plt.show()

    def getLen(self):
        return len(self.base)
        
        
