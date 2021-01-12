import matplotlib.pyplot as plt
from matplotlib import ticker

fig, ax = plt.subplots()


data=[1,2,3]
plt.plot([1,2,3],data)
plt.title("Sample")
plt.xlabel("X Label")
plt.ylabel("Y Label")

plt.gca().invert_yaxis()
plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(16))

fig.canvas.draw()

plt.plot(list(range(1,len(data)+1)),data,marker='o')


labels = ["-" + str(item.get_text()) for item in ax.get_yticklabels()]
print(labels)

ax.set_yticklabels(labels)

plt.show()

 
 
