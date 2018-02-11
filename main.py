#!/usr/bin/env python3
import serial
import time, math, os, sys, getopt


print("TrainStats Embedded probe\nVersion: 0.1.0\nAuthor: Michael Vieira <contact+dev[at]mvieira[dot]fr>\n")


# Read command arguments for the name of the session
try:
    opts, args = getopt.getopt(sys.argv, "n:t:l:", ["name=", "train=", "line="])

    print([opts, args])

    for opt, arg in opts:
        print([opt, arg])
except getopt.GetoptError:
    print("Usage: trainstats.py --name <session_name>")
    sys.exit(2)



# Init serial port
port = serial.Serial(
    port = "/dev/ttyUSB0",
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
)


# Create "sessions" folder if not exists, create the file and add the header for csv purpose
os.makedirs("sessions", exist_ok=True)
file = open("sessions/undefined-session_" + str(math.floor(time.time())) + ".dat", "w", encoding="utf-8")
file.write("timestamp,lat,lon,speed\n")


# Function to convert DMS to GPS position
def positionParser(pos):
    # lat = 48 + (43 + (4768 / 3600)) / 60
    # lon = 2 + (31 + (86459 / 3600)) / 60
    splitedData = pos.split(".")

    degree = 0
    minutes = 0
    seconds = int(splitedData[1])


    if(len(splitedData[0]) == 4):
        degree = int(str(splitedData[0][0]) + str(splitedData[0][1]))
        minutes = int(str(splitedData[0][2]) + str(splitedData[0][3]))
    else:
        degree = int(str(splitedData[0][0]) + str(splitedData[0][1]) + str(splitedData[0][2]))
        minutes = int(str(splitedData[0][3]) + str(splitedData[0][4]))

    return str(degree + ((minutes + (seconds / 3600)) / 60))


tempData = [None] * 3 # Create empty array

# Retrieve informations, parse and write into file
while True:
    data = str(port.readline(), "utf-8")
    data = data.split(",")

    if(data[0] == "$GPGLL"):
        print("Latitude: " + data[1] + data[2] + ", Longitude: " + data[3] + data[4])
        tempData[0] = positionParser(data[1])
        tempData[1] = positionParser(data[3])
    elif(data[0] == "$GPVTG"):
        print("Speed (in kts): " + data[5])
        tempData[2] = data[5]

    if(tempData[0] != None and tempData[1] != None and tempData[2] != None):
        file.write(str(math.floor(time.time())) + "," + tempData[0] + "," + tempData[1] + "," + tempData[2] + "\n")
        tempData = [None] * 3