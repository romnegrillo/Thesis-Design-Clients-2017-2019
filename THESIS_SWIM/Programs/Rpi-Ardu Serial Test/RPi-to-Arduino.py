# Import necessary libraries
import serial
import time

# Create a variable that will create
# a communication between the Raspberry Pi
# and the Arduino

# Serial(arg1, arg2)
# The first argument, arg1 to the Serial variable
# is the port name.
# The second argument arg2 to the Serial variable
# is the baud rate.

# In this example, 'COM8' is the port where
# Arduino is connected. We are using Windows
# here. Refer to the document named READ ME (Step 4).docx
# on how to do this is Raspberry Pi. But for now let us do
# this on Windows.
port=serial.Serial('COM8',9600)
port.setDTR(False)
time.sleep(1)
port.flushInput()
port.setDTR(True)
# try and except block
# The try and except block are
# used to handles errors.
# If any errors has been detected in the
# try block, it will stop and jump
# to the except block.

# For example, you are writing data to the serial port
# but you have disconnected the hardware connection,
# then that connection does not exists anymore.
# If we do not have a try and except block, the program
# will throw an error and stop executing.

try:

    # Create an infinite loop to continously run
    while True:

        # Send a string to the connected device.
        # May /n used as terminator.
        # Hanggang dun lang tayo magbabasa ibig sabihin.
        # May b sa unahin bago yung string, meaning
        # by bytes siya sinesend, hindi whole string agad.
        port.write(b'Jezzamae\n')
        print("Writing to port...")
        # Delay for five seconds.
        time.sleep(5)
except:

    # Close the port if some error occurs.
    # You can also press Ctrl+C to stop the infinite loop above
    # and get to this line.
    port.close()
    
