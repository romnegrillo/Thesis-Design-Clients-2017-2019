with open("sensorReading.txt","r") as f:
    list_reading = f.read().split(",")


print(len(list_reading))
