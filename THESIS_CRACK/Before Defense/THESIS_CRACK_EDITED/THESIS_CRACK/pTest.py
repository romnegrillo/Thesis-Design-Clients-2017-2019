import matplotlib
matplotlib.use("Qt5Agg") 
import matplotlib.pyplot as plt
from matplotlib import ticker
import time
import threading

class Plot:

    def __init__(self):
        pass
    
    def toPlot(self):
        plt.close('all')
        
        with open('test.txt','r') as f:
            data=f.readlines()
            data=[float(i) for i in data]
            data.insert(0,0)

        print(data)

        fig, ax = plt.subplots()
        #plt.yticks([round(i-0.8*i,2) for i in range (0,16)])
        #plt.plot(list(range(1,len(data)+1)),data)
         
        plt.gca().invert_yaxis()
        plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(16))

        print("debug")
        fileName=str(time.strftime("%Y-%m-%d %H-%M-%S"))+".png"
     

        plt.xlabel("Crack Length Measured")
        plt.ylabel("Depth (cm)")
        plt.grid()


        #plt.plot(list(range(1,len(data)+1)),data)
        plt.plot(list(range(1,len(data)+1)),data,marker='o')
        #plt.gca().invert_yaxis()
        plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(16))

        fig.canvas.draw()

        plt.plot(list(range(1,len(data)+1)),data,marker='o')
        #plt.plot(,data,marker='o')
        
        labels = ["-" + str(item.get_text()) for item in ax.get_yticklabels()]

        ax.set_yticklabels(labels)
        ax.set_xticklabels([i for i in range(0,len(data)*2+1,2)])

        plt.show()

        print("debug")
        fileName=str(time.strftime("%Y-%m-%d %H-%M-%S"))+".png"
     
        plt.xlabel("Crack Length Measured")
        plt.ylabel("Depth (cm)")
        plt.grid()
        plt.savefig("./graphs/"+fileName)
        print("Graph saved.")

if __name__=="__main__":
    test=Plot()
    test.toPlot()

 
