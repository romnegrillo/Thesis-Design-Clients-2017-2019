#import packages
import heartpy as hp
import matplotlib.pyplot as plt

sample_rate = 250

data = hp.get_data('sensorReading_new_16.txt')

plt.figure(figsize=(12,4))
plt.plot(data)
plt.show()


