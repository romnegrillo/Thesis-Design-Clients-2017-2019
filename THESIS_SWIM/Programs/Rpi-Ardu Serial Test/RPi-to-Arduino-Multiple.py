import serial
import time

arduinoPort=None

def main():
    
    try:
        global arduinoPort
        arduinoPort=serial.Serial("COM8", 9600)
        arduinoPort.setDTR(False)
        time.sleep(1)
        arduinoPort.flushInput()
        arduinoPort.setDTR(True)
        arduinoPort.flush()
        num1=0.00
        num2=0.00
        
        while True:
            num1=num1+1
            num2=num2+1
            toSend='{}'.format(''.join([str(num1),",",str(num2)]))
            toSend+="\n"

            time.sleep(5)
                        
            print("Writing to port...")
            print(toSend,end='')
            arduinoPort.write(toSend.encode())
    except:
        arduinoPort.flush()
        arduinoPort.close()
        print("No Arduino detected")
        print("or you have disconnected it!")
        print("Re run the program!")
main()
