import serial
#ser = serial.Serial('/dev/cu.usbmodem1411') # change in RPi
ser = serial.Serial('/dev/ttyACM0') # change in RPi
values = ''
while True:
    pkg = ser.readline()
    #values.strip() for x in pkg.split(',')]

    print pkg
