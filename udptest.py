#!/usr/bin/python
import socket
import struct

UDP_IP = "localhost"
UDP_PORT = 3000
#MESSAGE = "Hello, World!"

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT
#print "message:", MESSAGE

MESSAGE1 = struct.pack('BB',
            33,
            4)
MESSAGE2 = struct.pack('iiiiiiiI',
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,)
MESSAGE = MESSAGE1 + MESSAGE2
print MESSAGE

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
