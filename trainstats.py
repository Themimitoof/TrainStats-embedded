#!/usr/bin/env python3
import serial
import time
import math
import os, sys
import getopt
import curses


print("TrainStats Embedded probe\nVersion: 0.1.0\nAuthor: Michael Vieira <contact+dev[at]mvieira[dot]fr>\n")

fileName = [None] * 3 # Create an empty array for the name of the output file.

#
# Read command arguments for the name of the session
#
try:
    opts, args = getopt.getopt(sys.argv[1:], "hd:s:t:l:", longopts=["help", "device=", "section=", "train=", "line="])

    if(len(opts) == 0):
        print("Usage: trainstats.py -d <tty> [options]")
        sys.exit(2)

    for opt, arg in opts:
        if(opt == "-h" or opt == "--help"):
            print("Available command commands:\n\t-h, --help\t\t\tShow this message\n\t-d, --device <tty>\t\tAssign the serial port\n\t-s, --section <section_info>\tGive the section infos (for example: the point A and point Z of your route) \n\t-t, --train <train_id>\t\tAssign a train ID for this session\n\t\t\t\t\t(for example: Z20500 for the most common RER D train in Paris)\n\t-l, --line <line_name>\t\tAssign the name of the line to the session")
            print("\n\nExamples:\n\t./trainstats.py -d /dev/ttyUSB0\t\tThe minimal command to start TrainStats\n\t./trainstats.py -d /dev/ttyUSB0 -s VSG-PGL")
            sys.exit(0)
        elif(opt == "-s" or opt == "--section"):
            if(arg != ""): fileName[0] = arg
            else:
                print("No section information defined.\nUsage: trainstats.py -d <tty> [options]")
                sys.exit(2)
        elif(opt == "-t" or opt == "--train"):
            if(arg != ""): fileName[1] = arg
            else:
                print("No train information defined.\nUsage: trainstats.py -d <tty> [options]")
                sys.exit(2)
        elif(opt == "-l" or opt == "--line"):
            if(arg != ""): fileName[2] = arg
            else:
                print("No line information defined.\nUsage: trainstats.py -d <tty> [options]")
                sys.exit(2)
    
        # Parse the device argument for initializing the serial port
        elif(opt == "-d" and arg != "" or opt == "--device" and arg != ""):
            try:
                # Init serial port
                port = serial.Serial(
                    port = arg,
                    baudrate = 9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                )
            except serial.SerialException:
                print("The serial port not exists or is not available.")
                sys.exit(2)
        else:
            print("Usage: trainstats.py -d <tty> [options]")
            sys.exit(2)

except getopt.GetoptError:
    print("Usage: trainstats.py -d <tty> [options]")
    sys.exit(2)




# Create "sessions" folder if not exists, create the file and add the header for csv purpose
sessionName = str(math.floor(time.time()))

if(fileName[0] == None and fileName[1] == None and fileName[2] == None): sessionName += "_untitled-session"
else:
    for entry in fileName:
        if(entry != None): sessionName += "_" + entry

os.makedirs("sessions", exist_ok=True)
file = open("sessions/" + sessionName + ".dat", "w", encoding="utf-8")
file.write("timestamp,lat,lon,speed\n")


# Initialize curses and create the "layout"
stdscr = curses.initscr() 
curses.noecho()
stdscr.addstr(0, 0, "\tTrainStats (ctrl+c to close the program)\t", curses.A_REVERSE)
stdscr.addstr(2, 0, "Latitude:")
stdscr.addstr(3, 0, "Longitude:")
stdscr.addstr(4, 0, "Speed:")
stdscr.addstr(5, 0, "Nb messages:")
stdscr.refresh()


# Function to convert DMS to GPS position
def positionParser(pos):
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
nbMessages = 0


# Retrieve informations, parse and write into file
while True:
    try:
        data = str(port.readline(), "utf-8")
        data = data.split(",")

        if(data[0] == "$GPGLL"):
            tempData[0] = positionParser(data[1])
            tempData[1] = positionParser(data[3])

            # Clear the line before showing the new values
            stdscr.addstr(2, 14, "\t\t\t\t\t\t\t")
            stdscr.addstr(3, 14, "\t\t\t\t\t\t\t")
            
            # Show the content on the screen
            stdscr.addstr(2, 14, data[1] + data[2] + "\t(" + tempData[0] + ")")
            stdscr.addstr(3, 14, data[3] + data[4] + "\t(" + tempData[1] + ")")
        elif(data[0] == "$GPVTG"):
            stdscr.addstr(4, 14, "\t\t\t\t\t\t\t")            
            stdscr.addstr(4, 14, data[5] + "kts\t\t(" + data[7] + "km/h)")
            tempData[2] = data[5]

        if(tempData[0] != None and tempData[1] != None and tempData[2] != None):
            # Show on the screen the number of received messages
            nbMessages = nbMessages + 1
            stdscr.addstr(5, 14, str(nbMessages) + " messages received.")
            stdscr.refresh()

            # Write the complete information into the file
            file.write(str(math.floor(time.time())) + "," + tempData[0] + "," + tempData[1] + "," + tempData[2] + "\n")
            tempData = [None] * 3

    except KeyboardInterrupt:
        # Close the serial port and the file and quit the program
        port.close()
        file.close()
        curses.endwin()
        sys.exit(0)