import io     # Used to create file streams.
import fcntl  # Used to access I2C parameters like addresses.
import time   # Used for sleep delay and timestamps.
import serial # Used for serial communication.

class atlas_i2c:
    long_timeout = 1.5                    
    short_timeout = .5   
    default_bus = 1        
    default_address = 99  

    def __init__(self, address=default_address, bus=default_bus):
        self.file_read = io.open("/dev/i2c-" + str(bus), "rb", buffering=0)
        self.file_write = io.open("/dev/i2c-" + str(bus), "wb", buffering=0)
        self.set_i2c_address(address)

    def set_i2c_address(self, addr):
        
        I2C_SLAVE = 0x703
        fcntl.ioctl(self.file_read, I2C_SLAVE, addr)
        fcntl.ioctl(self.file_write, I2C_SLAVE, addr)

    def write(self, string):
        
        string += "\00"
        self.file_write.write(bytes(string, 'UTF-8'))

    def read(self, num_of_bytes=31):
        
        res = self.file_read.read(num_of_bytes) 
        response = [x for x in res if x != '\x00']
        
        if response[0] == 1:  
          
            char_list = [chr(x & ~0x80) for x in list(response[1:])]
            return "Command succeeded " + ''.join(char_list)
        else:
            return "Error " + str(response[0])

    def query(self, string):
        
        self.write(string)

        if((string.upper().startswith("R")) or
           (string.upper().startswith("CAL"))):
            time.sleep(self.long_timeout)
        elif((string.upper().startswith("SLEEP"))):
            return "sleep mode"
        else:
            time.sleep(self.short_timeout)

        return self.read()

    def close(self):
        self.file_read.close()
        self.file_write.close()


# Global variable for arduin port.
arduinoPort=None

def main():

    # Create a the model blueprint.
    device = atlas_i2c()  

    # Addresses of the sensors.                      
    ORPAddress=98
    pHAddress=99

    # Variables for the sensor readings.
    ORPValue=0
    phValue=0

    # Create serial variable to send serial data.
    global arduinoPort
    arduinoPort=serial.Serial("COM8", 9600)
    arduinoPort.setDTR(False)
    time.sleep(1)
    arduinoPort.flushInput()
    arduinoPort.setDTR(True)
    arduinoPort.flush()
    
    # Infinite loop to read sensors, send and receive data.
    while True:

        try:
            arduinoPort.open()
        except:
            print("No Arduino detected!")
            break

        try:
            
            device.set_i2c_address(ORPAddress)
            queryValue=device.query("R")
            newList=[x for x in list(queryValue) if x.isdigit() or x=="."]
            ORPValue=float(''.join(newList))

            device.set_i2c_address(pHAddress)
            queryValue=device.query("R")
            newList=[x for x in list(queryValue) if x.isdigit() or x=="."]
            phValue=float(''.join(newList))

            print("ORP Value: {}".format(ORPValue))
            print("pH Value: {}".format(phValue))

            readingToSend=[]
            readingToSend.append(str(ORPValue))
            readingToSend.append(",")
            readingToSend.append(str(phValue))
            readingToSend="".join(readingToSend)
            readingToSend+="\n"

            # Delay three seconds.
            time.sleep(3)
            
            print("Sending to Arduino: {}".format(readingToSend),end="")
            arduinoPort.write(readingToSend.encode())

            
        except KeyboardInterrupt:
            print("Cancelled by the user.")
            break
        except:
            print("ORP and/or pH Sensor is/are not detected!")
            break

    print("Program halted!")
        
if __name__ == '__main__':
    main()
