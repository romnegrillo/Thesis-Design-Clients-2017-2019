import numpy as np
import random
import matplotlib.pyplot as plt
import time
from matplotlib import ticker

class DepthCalib:

    def __init__(self):
        
        status=1
        self.pos=0
        
        with open('test.txt','w') as f:
            pass
        
        if status==1:
            self.depth = []
            self.base = [1.25,1.24,1.26,2.54,2.54,2.53,2.5]
            self.calib= []
        else:
            self.depth = []
            self.base = []
            self.calib= []

        for i in self.base:
            self.calib.append(random.uniform(i-.15,i+0.15))

    def addDepth(self,depth):
        self.depth.append(depth)

        with open('test.txt','a') as f:
            f.write(str(self.calib[self.pos])+"\n")
            self.pos=self.pos+1

    def plotResult(self):                

        with open('test.txt','r') as f:
            data=f.readlines()
            data=[float(i) for i in data]
            data.insert(0,0)
        
        #plt.yticks([round(i-0.8*i,2) for i in range (0,16)])
        #plt.plot(list(range(1,len(data)+1)),data)
        plt.plot(list(range(1,len(data)+1)),data,marker='o')
        plt.gca().invert_yaxis()
        plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(16))
        
        fileName=str(time.strftime("%Y-%m-%d %H-%M-%S"))+".jpg"
        plt.savefig("./graphs/"+fileName)
        plt.xlabel("Crack Points Measured")
        plt.ylabel("Depth (cm)")
        plt.grid()
        plt.show()

    def getLen(self):
        return len(self.base)
        
        
