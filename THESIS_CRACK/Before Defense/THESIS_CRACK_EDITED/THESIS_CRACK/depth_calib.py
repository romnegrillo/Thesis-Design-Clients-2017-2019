import numpy as np
import random
import matplotlib
matplotlib.use("Qt5Agg") 
import matplotlib.pyplot as plt
import time
from matplotlib import ticker
import threading

class DepthCalib:

    def __init__(self):
        
        status=1
        self.pos=0
        
        with open('test.txt','w') as f:
            pass
        
        if status==1:
            self.depth = []
            self.base = [4,5,4,4,3,3,.35,.4]
            self.calib= []
        else:
            self.depth = []
            self.base = []
            self.calib= []

        for i in self.base:
            self.calib.append(random.uniform(i-.3,i+.3))

    def addDepth(self,depth):
        self.depth.append(depth)

        with open('test.txt','a') as f:
            f.write(str(self.calib[self.pos])+"\n")
            self.pos=self.pos+1

    def plotResult(self):
        
        #plt.close('all')
        with open('test.txt','r') as f:
            data=f.readlines()
            data=[float(i) for i in data]
            data.insert(0,0)

        print("debug")
        
        #plt.yticks([round(i-0.8*i,2) for i in range (0,16)])
        #plt.plot(list(range(1,len(data)+1)),data)

        try:
            plt.plot(list(range(1,len(data)+1)),data,marker='o')
            plt.show()
        except Exception as exp:
            print(str(exp))

        print("debug")
        
        plt.gca().invert_yaxis()
        plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(16))
        
        print("debug")
        
        fileName=str(time.strftime("%Y-%m-%d %H-%M-%S"))+".jpg"
         
        plt.xlabel("Crack Points Measured")
        plt.ylabel("Depth (cm)")
        plt.grid()
        
        print("debug")
        
        #plt.show()
        plt.savefig("./graphs/"+fileName)
        print("Graph saved.")
        print("Plot thread ended.")

    def getTargetValue(self,args):
        return 1000
 
        

    def getLen(self):
        return len(self.base)
        
        
