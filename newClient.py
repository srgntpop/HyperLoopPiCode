#newClient.py

#!/usr/bin/env python
import socket
import sys
import serial

# Create a TCP/IP socket
# TCP (not UDP) --> bidirectional socket connection from host to client 
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# print "init success"

# Connect the socket to the port where the server is listening
# the server address for client and host have to be same, not school wifi -docx
# changed server address from '0.102' to '0.101' -SM
server_address = ('192.168.0.102', 10004)

#use command ifconfig on HOST computer to get IP addresss
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

#ser = serial.Serial('/dev/ttyACM0',9600)
ser = serial.Serial('/dev/serial/by-id/usb-Arduino_Srl_Arduino_Uno_75436343430351607011-if00',9600)

#ser = serial.Serial('/dev/serial/by-id/usb-Arduino__www.arduino.cc__0042_755333433363511061A0-if00', 9600)
#this commented out line used to work but stopped for whatever reason.
#Google that line with fix if the new line doens't work anymore

ser.write('0')
print "Serial write successful"

while True:
    print "Entering loop"
    #ser.write('0')
    read_serial1 = ser.readline()
    print read_serial1
    if read_serial1.count(',') == 10:
        print read_serial1
        sock.sendall(read_serial1)
        data = sock.recv(100)
        for x in range(0, len(data)): # for x in range(0, len(data)-1):
            if data[x:x+1] != '0':
                print data
                ser.write('1')
                print >>sys.stderr, 'POD STOP'
                while 1:
                    ser.write('1')
        ser.write('0')

        print >>sys.stderr, 'received "%s"' % data
    else:
        print "not enough data"
        ser.write('0')
    

print >>sys.stderr, 'closing socket'
sock.close()
