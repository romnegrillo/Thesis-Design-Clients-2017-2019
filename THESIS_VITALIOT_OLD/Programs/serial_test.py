import serial
import time

port = serial.Serial(port="/dev/ttyUSB0", baudrate=9600)

try:
    while 1:
        try:
            if port.isOpen():
                data = port.readline()
                data = data.decode()
                data = data.split(",")

                print(data)
        except Exception as exp:
            pass

        time.sleep(1)
except Exception as exp:
    print(str(exp))
finally:
    port.close()

print("Done")
