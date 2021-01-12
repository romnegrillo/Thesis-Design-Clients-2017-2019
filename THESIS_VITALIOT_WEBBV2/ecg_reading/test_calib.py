import serial

sensorSerial = serial.Serial("COM13", 9600)

while 1:
    try:
        data = sensorSerial.readline().decode()
        data_filter = int(data)

        if data_filter > 1000:
            continue
        
        print(data[0:-2])

        with open("sensorReading_new_16.txt","a") as f:
            f.write(str(data[0:-2])+"\n")
    except Exception as exp:
        print(str(exp))

            




