# runGui.py

# !/usr/bin/python
#this file is used to create the GUI
#This creates a server and displays the GUI

# NETWORK STUFF: Pi, SpaceX, GUI communications
# setup a tcp/ip connection with the pi, receive data with sock.accept/recv
# setup udp conneciton with spacex, send data from gui to spacex

from PyQt4.QtGui import * 
from PyQt4.QtCore import * 
from GUIwithstart import Ui_MainWindow
import struct
import sys
import socket
import threading
import gtk


#pyuic4 GUI.ui -o GUI.py # run this after changing GUI

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# put the localhost address for first argument 
# localhost = 127.0.0.1
server_address = ('', 10000) 
# If the socket closes incorrectly, the port number will need to be
# incremented becasue the previous port is still open

# Bind the socket to the port
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

sock.listen(1) #accepts one connection

#this tests the data we send to spaceX, you will need to test it on a 
#seperate device instead of local host 
UDP_IP = "localhost" #testing on my computer, change for later
UDP_PORT = 3000
MESSAGE = "Hello, World!"
#setup UDP connection
sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

stopped = 0
status = 0

class MainWindow(QMainWindow, Ui_MainWindow):


	def __init__(self, parent = None):
        	QMainWindow.__init__(self, parent)
        	self.setupUi(self)
        	self.pushButton.clicked.connect(self.button_clicked)
        	self.pushButton_2.clicked.connect(self.button2_clicked)
        	threading.Thread(target=self.data_transfer).start()
        	
    #stops the pod
	def button_clicked(self):
		self.pushButton.setText("THE POD HAS STOPPED")
		global stopped 
		stopped = 1
		
		
	#When the pod is ready
	def button2_clicked(self):

		self.label.raise_()
		self.tableWidget.raise_()
		self.tableWidget.raise_()
		self.tableWidget.raise_()
		self.label_2.raise_()
		self.label_4.raise_()
		self.pushButton.raise_()
		global status
		status = 2

			

	#sends and recieves data and updates GUI
	def data_transfer(self):
		global connection
		# wait for connection use accept() return open connection and client address
		connection, client_address = sock.accept()
		counter  = 0
		global stopped
		global status
		while True:
		    if stopped != 1:
				# recv() - reads from connection, 500 may not be best value 
		    	data = connection.recv(500) #takes buffsize # bytes - power of 2
			if data.count(',') == 10: 
				data = data[:len(data)-2]
		 	        dataArray = data.split(",")
		 	        print dataArray
		 	        item = QTableWidgetItem()
				# clean this up with a for loop to reduce file space - SM
				item.setText(dataArray[0])
				self.tableWidget.setItem(0,0, item)
			
				item = QTableWidgetItem()
				item.setText(dataArray[1])
				self.tableWidget.setItem(1,0, item)
			
				item = QTableWidgetItem()
				item.setText(dataArray[2])
				self.tableWidget.setItem(2,0, item)
			
				item = QTableWidgetItem()
				item.setText(dataArray[3])
				self.tableWidget.setItem(3,0, item)
			
			
				item = QTableWidgetItem()
				item.setText(dataArray[4])
				self.tableWidget.setItem(4,0, item)
			
				item = QTableWidgetItem()
				item.setText(dataArray[5])
				self.tableWidget.setItem(5,0, item)
			
				item = QTableWidgetItem()
				item.setText(dataArray[6])
				self.tableWidget.setItem(6,0, item)
			
				item = QTableWidgetItem()
				item.setText(dataArray[7])
				self.tableWidget.setItem(7,0, item)

				item = QTableWidgetItem()
				item.setText(dataArray[8])
				self.tableWidget.setItem(8,0, item)
			        if data:
					connection.sendall('0') #transmit data from gui to spacex
					print('sending 0')
					
					
					#data sent to spaceX
					# convert data to string to be sent nicely to spacex
					MESSAGE1 = struct.pack('BB',
            					  69, #team ID, given to us by space X
         					  status)
					MESSAGE2 = struct.pack('iiiiiiiI',
					          int(dataArray[9]),
            					  int(dataArray[0]),
						  int(dataArray[1]),
						  0,#zero is optional data that isn't needed
						  0,
						  0,
						  0,
						  0)
					MESSAGE = MESSAGE1 + MESSAGE2
					print MESSAGE
					
					#use one way udp connection to send to spacex
					sock2.sendto(MESSAGE, (UDP_IP, UDP_PORT))

				else:
					print >>sys.stderr, 'connection lost', client_address
					connection.sendall('1')
					sock.close()
			else:
				print ('not enough data recieved')
				print data
				connection.sendall('0')

		    else:
		    	print >>sys.stderr, 'stopping pod'
		    	connection.sendall('1')
			sock.close()

			

		
if __name__ == '__main__':
    from PyQt4.QtGui import QApplication    
    app = QApplication(sys.argv)
    gtk.gdk.threads_init()
    window = MainWindow()
    window.show()
    app.exec_()
    sys.exit(app.exec_())
   

