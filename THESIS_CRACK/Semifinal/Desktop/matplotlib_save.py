from matplotlib import pyplot as plt
import os
import time

depth=[1,1.3,1.2,1.5,1.7,1.75,1.56,2,3]


plt.plot(depth)
plt.gca().invert_yaxis()

fileName=str(time.strftime("%Y-%m-%d %H-%M-%S"))+".jpg"
print(fileName)

try:
    plt.savefig("./graphs/"+fileName)
except Exception as exp:
    print(str(exp))
plt.show()
