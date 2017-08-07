import serial

def main():

	serMaster = serial.Serial('/dev/ttyACM0', 9600)
	
	# read in one array consisting of all sensor data
	while True:
		
		# read in temps and strip '\n'
		temp1In = serMaster.readline().strip()
		temp2In = serMaster.readline().strip()
		temp3In = serMaster.readline().strip()
		
		#convert bytes to string 
		temp1 = temp1In.decode("utf-8") 
		temp2 = temp2In.decode("utf-8")
		temp3 = temp3In.decode("utf-8")
		
		#print 
		print("temp1: " + temp1)
		print("temp2: " + temp2)
		print("temp3: " + temp3)
main()

