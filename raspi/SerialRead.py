import serial
ser = serial.Serial('/dev/cu.usbmodem1411') # MacBook's
#ser = serial.Serial('/dev/ttyACM0') # RPi's

while True:
    pkg = ser.readline()

    print pkg
