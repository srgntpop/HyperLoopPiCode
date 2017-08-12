
import socket

# this udp_ip needs to match spacex ip
# UDP_IP = "10.201.10.192"
UDP_IP = "127.0.0.1"
UDP_PORT = 3000

sock = socket.socket(socket.AF_INET,
                     socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print "finished initializing"

while True:
	data, addr = sock.recvfrom(34) #buffer size is 34 bytes
    # print data
	dataList = list(data)#.split('')
    # print len(dataList)
	#print len(dataList)
    # print dataList
	for i in range(34):
		try:
			print(ord(dataList[i])) #.encode("dec"))
		except IndexError:
			print "null"
	# fData = data.decode("ascii")
	print "received message: ", data
	#for i in range(255):
	#	dataList[0] = ord(dataList[0]) + 1
	#	print(dataList[0])			
