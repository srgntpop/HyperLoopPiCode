#newClient.py

#!/usr/bin/env python
import socket
import sys
import serial
import time
import numpy

serIMU = serial.Serial('/dev/ttyUSB0', 115200)
startTime = time.time() 
timesRead = 0

velocityX = 0.0
velocityY = 0.0
velocityZ = 0.0

dt = 0.01
passedOnce = False

newImuVals = []
newImuDirs = []
oldImuVals = []
oldImuDirs = []

while True:
	if (newImuVals != []):
		passedOnce = True
		oldImuVals = newImuVals
		oldImuDirs = newImuDirs
	checkTime = time.time()
	timePassed = checkTime - startTime
	print(timePassed)	
	imuLine = serIMU.readline()
	timesRead += 1
	print(timesRead)
	#print(IMULine)
	imuDataArr = imuLine.strip().split(',')
	print(imuDataArr)
	
	newImuVals = [int(float(imuDataArr[1][1:])), int(float(imuDataArr[2][1:])), int(float(imuDataArr[3][1:7]))]
	newImuDirs = [imuDataArr[1][0], imuDataArr[2][0], imuDataArr[3][0]]

	#print("newImuDirs: ")
	#print(newImuDirs)
	print(newImuVals)
	
	# get velocity data in x direction
	# TODO:
	# implement low pass filter
	# account for offset 
	# acount for negative directions
	if (passedOnce):
		if (newImuDirs[0] == oldImuDirs[0] and newImuDirs[0] == '+'):
			velocityX += (newImuVals[0] + oldImuVals[0])/2.0*dt
			print("velocity X: " + str(velocityX))
		
		elif (newImuDirs[0] == oldImuDirs[0] and newImuDirs[0] == '-'):
			velocityX += (newImuVals[0] + oldImuVals[0])/2.0*dt
			print("velocity X: " + str(velocityX))

		else:
			velocityX += (newImuVals[0] - oldImuVals[0])/2.0*dt
			print("velocity X: " + str(velocityX))
		
		
		if (newImuDirs[1] == oldImuDirs[1] and newImuDirs[1] == '+'):
			velocityY += (newImuVals[1] + oldImuVals[1])/2.0*dt
			print("velocity Y: " + str(velocityY))
		
		elif (newImuDirs[1] == oldImuDirs[1] and newImuDirs[1] == '-'):
			velocityY -= (newImuVals[1] + oldImuVals[1])/2.0*dt
			print("velocity Y: " + str(velocityY))

		else:
			velocityY += (newImuVals[1] - oldImuVals[1])/2.0*dt
			print("velocity Y: " + str(velocityY))


		if (newImuDirs[2] == oldImuDirs[2] and newImuDirs[2] == '+'):
			velocityZ += (newImuVals[2] + oldImuVals[2])/2.0*dt
			print("velocity Z: " + str(velocityZ))
		
		elif (newImuDirs[2] == oldImuDirs[2] and newImuDirs[2] == '-'):
			velocityZ -= (newImuVals[2] + oldImuVals[2])/2.0*dt
			print("velocity Z: " + str(velocityZ))

		else:
			velocityZ += (newImuVals[2] - oldImuVals[2])/2.0*dt
			print("velocity Z: " + str(velocityZ))

# Create a TCP/IP socket
# TCP (not UDP) --> bidirectional socket connection from host to client 
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# print "init success"

# Connect the socket to the port where the server is listening
# the server address for client and host have to be same, not school wifi -docx
# changed server address from '0.102' to '0.101' -SM



server_address = ('192.168.0.101', 10004)

#use command ifconfig on HOST computer to get IP addresss
print >>sys.stderr, ('connecting to %s port %s' % server_address)
sock.connect(server_address)

ser = serial.Serial('/dev/ttyACM0',9600)

#ser = serial.Serial('/dev/serial/by-id/usb-Arduino_Srl_Arduino_Uno_75436343430351607011-if00',9600)

#ser = serial.Serial('/dev/serial/by-id/usb-Arduino__www.arduino.cc__0042_755333433363511061A0-if00', 9600)
#this commented out line used to work but stopped for whatever reason.
#Google that line with fix if the new line doens't work anymore

ser.write('0')
print ("Serial write successful")

while True:
	print(serIMU.readline())

while True:
    print ("Entering loop")
    #ser.write('0')
    read_serial1 = ser.readline()
    print (read_serial1)
    if read_serial1.count(',') == 10:
        print (read_serial1)
        sock.sendall(read_serial1)
        data = sock.recv(100)
        for x in range(0, len(data)): # for x in range(0, len(data)-1):
            if data[x:x+1] != '0':
                print (data)
                ser.write('1')
                print >>sys.stderr,( 'POD STOP')
                while 1:
                    ser.write('1')
        ser.write('0')

        print >>sys.stderr, ('received "%s"' % data)
    else:
        print ("not enough data")
        ser.write('0')
    

print >>sys.stderr, ('closing socket')
sock.close()
