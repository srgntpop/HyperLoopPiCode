#!/usr/bin/python
#this file is used to craete the the GUI
#This creates a server and displays the GUI
import socket
import sys
import threading
import struct
import random

from GUIwithstart import Ui_MainWindow
from PyQt4.QtGui import *

##import gtk

#pyuic4 GUI.ui -o GUI.py // run this afte0r changing GUI

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

<<<<<<< HEAD
# for address put in the router's address
server_address = ('iPv4 addr from router', 10004) 
# If the socket closes incorrectly, the port number will need to be
# incremented becasue the previous port is still open

=======
>>>>>>> d8461fd6f8b111a81c5cd1aab1d2e33aef3c4cb1
# Bind the socket to the port
server_address = ('localhost', 10004) # If the socket closes incorrectly, the port number will need to be incremented becasue the previous port is still open
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

sock.listen(1) #accepts one connection


#this tests the data we send to spaceX, you will need to test it on a seperate device instead of local host
#this needs to match the IP on the computer utilizing the spacex code
# UDP_IP = "192.168.0.101" #"localhost" testing on my computer, change for later
# UDP_IP = '10.201.5.226'
UDP_IP = "localhost"
UDP_PORT = 3000
MESSAGE = "Hello, World!"
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
		self.random_gen()
		self.label.raise_()
		self.tableWidget.raise_()
		self.tableWidget.raise_()
		self.tableWidget.raise_()
		self.healthCheck.raise_()
		self.label_2.raise_()
		self.label_4.raise_()
		self.pushButton.raise_()
		global status
		status = 2
		# self.random_gen()


	def random_gen(self):
		random.seed()
		while True:
			print "loop"
			junkData1 = [random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)]
			junkData2 = [random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)]
			item = QTableWidgetItem()
			item.setText(str(junkData1[0]))
			self.healthCheck.setItem(0, 0, item)
			item = QTableWidgetItem()
			item.setText(str(junkData1[1]))
			self.healthCheck.setItem(0, 1, item)
			item = QTableWidgetItem()
			item.setText(str(junkData1[2]))
			self.healthCheck.setItem(0, 2, item)

			item = QTableWidgetItem()
			item.setText(str(junkData2[0]))
			self.healthCheck.setItem(1, 0, item)
			item = QTableWidgetItem()
			item.setText(str(junkData2[1]))
			self.healthCheck.setItem(1, 1, item)
			item = QTableWidgetItem()
			item.setText(str(junkData2[2]))
			self.healthCheck.setItem(1, 2, item)

			#sends and recieves data and updates GUI
	def data_transfer(self):
		global connection
		connection, client_address = sock.accept()
		counter  = 0
		global stopped
		global status
		# random.seed()
		# print "loop"
		while True:
			# print "loop"
			# junkData1 = [random.randint(0,100), random.randint(0,100), random.randint(0,100)]
			# junkData2 = [random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)]
			# item = QTableWidgetItem()
			# item.setText(junkData1[0])
			# self.healthCheck.setItem(0,0,item)
			# item = QTableWidgetItem()
			# item.setText(junkData1[1])
			# self.healthCheck.setItem(0, 1, item)
			# item = QTableWidgetItem()
			# item.setText(junkData1[2])
			# self.healthCheck.setItem(0, 2, item)
            #
			# item = QTableWidgetItem()
			# item.setText(junkData2[0])
			# self.healthCheck.setItem(1, 0, item)
			# item = QTableWidgetItem()
			# item.setText(junkData2[1])
			# self.healthCheck.setItem(1, 1, item)
			# item = QTableWidgetItem()
			# item.setText(junkData2[2])
			# self.healthCheck.setItem(1, 2, item)

			if stopped != 1:
				data = connection.recv(500)
			if data.count(',') == 10: 
				data = data[:len(data)-2]
				dataArray = data.split(",")
<<<<<<< HEAD
				# print dataArray
				for i in range(0,8,1):
					item = QTableWidgetItem()
					item.setText(dataArray[i])
					self.tableWidget.setItem(i,0, item)


				if data:
					connection.sendall('0')
					#print('sending 0')

					# data sent to spaceX
					MESSAGE1 = struct.pack("BB",
            					  69, #team ID, given to us by space X
         					  status)
					MESSAGE2 = struct.pack('iiiiiiiI',
					         int(dataArray[9]),
            					  int(dataArray[0]),
=======
				print dataArray
				item = QTableWidgetItem()
				item.setText(dataArray[0])
				self.tableWidget.setItem(0,0, item)
				
				#for i in range(1, 9):
				#	item = QTableWidgetItem()
				#	item.setText(dataArray[i])
				#	self.tableWidget.setItem(i,0, item)
			
	##################################################### remove with for loop
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
<<<<<<< HEAD
			       
	##################################################### 
				 if data:
					connection.sendall('0') #transmit data from gui to spacex
=======
				if data:
					connection.sendall('0')
>>>>>>> d8461fd6f8b111a81c5cd1aab1d2e33aef3c4cb1
					print('sending 0')
					
					
					#data sent to spaceX
<<<<<<< HEAD
					#convert data to string to be sent nicely to spacex
=======
>>>>>>> d8461fd6f8b111a81c5cd1aab1d2e33aef3c4cb1
					MESSAGE1 = struct.pack('BB',
            					  69, #team ID, given to us by space X
         					  status)
					MESSAGE2 = struct.pack('iiiiiiiI',
					          int(dataArray[9]),
            		  		   int(dataArray[0]),
>>>>>>> origin/master
						  int(dataArray[1]),
						  0,#zero is optional data that isn't needed
						  0,
						  0,
						  0,
						  0)
					MESSAGE = MESSAGE1 + MESSAGE2
<<<<<<< HEAD
					# team_id = 70
					# MessageNew = ""
					# MessageNew += "Team_ID = " + str(team_id) + " "
					# MessageNew += "Status = " + str(status) + " "
					print "udp message: " + MESSAGE1
=======
<<<<<<< HEAD
					print "udp message: " + MESSAGE
					
					#use one way udp connection to send to spacex
=======
					print MESSAGE
>>>>>>> origin/master

>>>>>>> d8461fd6f8b111a81c5cd1aab1d2e33aef3c4cb1
					sock2.sendto(MESSAGE, (UDP_IP, UDP_PORT))
					# sock2.sendto(00000, (UDP_IP, UDP_PORT))

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
##	gtk.gdk.threads_init()
	window = MainWindow()
	window.show()
	app.exec_()
	sys.exit(app.exec_())
