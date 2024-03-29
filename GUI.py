from PIL import Image
import Tkinter as tk
import time, datetime, sys, struct
import shutil
import os
from multiprocessing import *
import socket
import tkMessageBox

connect = 0
Oldvalue1 = 0
Oldvalue2 = 0
Oldvalue3 = 0
Oldvalue4 = 0

c = socket.socket()
host = '192.168.1.144'
port = 12348
#c.connect((host, port))

def getSensorData():
	c.send("12")
	msg = ""
	s = c.recv(2)
	if s.isdigit():
		size = int(s)
		c.send("13")
		msg = str(c.recv(size)).split()
		return msg
	return msg

def count(pipe, pipe1, pipe2, pipe3, pipe4, pipe5, pipe6, pipe7, pipe8, pipe9, root, stop):
	global connect
	global red
	print connect
	while not stop.is_set():
		nums = getSensorData()
		pipe.send(nums[0])
		pipe1.send(nums[1])
		pipe2.send(nums[2])
		pipe3.send(nums[3])
		pipe4.send(nums[4])
		pipe5.send(nums[5])
		pipe6.send(nums[6])
		pipe7.send(nums[7])
		pipe8.send(nums[8])
		pipe9.send(nums[9])
		
		time.sleep(.5)

class UpdatingGUI(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent, bg = 'black')
		self.parent = parent
		#height
		self.parent_pipe, self.child_pipe, = Pipe()
		#roll
		self.parent1_pipe, self.child1_pipe = Pipe()
		#pitch
		self.parent2_pipe, self.child2_pipe = Pipe()
		#yaw
		self.parent3_pipe, self.child3_pipe = Pipe()
		#ax
		self.parent4_pipe, self.child4_pipe = Pipe()
		#ay
		self.parent5_pipe, self.child5_pipe = Pipe()
		#az
		self.parent6_pipe, self.child6_pipe = Pipe()
		#mx
		self.parent7_pipe, self.child7_pipe = Pipe()
		#my
		self.parent8_pipe, self.child8_pipe = Pipe()
		#mz
		self.parent9_pipe, self.child9_pipe = Pipe()

		self.stop_event = Event()

		#Height
		self.updating_int = tk.IntVar()
		self.updating_int.set(0)
		self.updating_lbl = tk.Label(self, text = "Height", textvariable = self.updating_int, fg = 'white', bg = 'black')
		self.updating_lbl.pack()
		self.heightLbl = tk.Label(self, text = "Height: ", fg = 'white', bg = 'black')
		self.heightLbl.pack(padx = 5, pady = 5, side = tk.RIGHT)
		self.updating_lbl.pack(padx = 2, pady = 2, side = tk.RIGHT)

		#Yaw
		self.updating_yaw= tk.IntVar()
		self.updating_yaw.set(0)
		self.updating_yawLbl = tk.Label(self, text = "Yaw", textvariable = self.updating_yaw, fg = 'white', bg = 'black')
		self.updating_yawLbl.pack() 
		self.YawLbl = tk.Label(self, text = "Yaw: ", fg = 'white', bg = 'black')
		self.YawLbl.pack(padx = 5, pady = 10, side = tk.RIGHT)
		self.updating_yawLbl.pack(padx = 5, pady = 5, side = tk.RIGHT)

		#Pitch
		self.updating_pitch = tk.IntVar()
		self.updating_pitch.set(0)
		self.updating_pitchLbl = tk.Label(self, text = "Pitch", textvariable = self.updating_pitch, fg = 'white', bg = 'black')
		self.updating_pitchLbl.pack() 
		self.PitchLbl = tk.Label(self, text = "Pitch: ", fg = 'white', bg = 'black')
		self.PitchLbl.pack(padx = 5, pady = 10, side = tk.RIGHT)
		self.updating_pitchLbl.pack(padx = 5, pady = 5, side = tk.RIGHT)

		#Roll
		self.updating_roll = tk.IntVar()
		self.updating_roll.set(0)
		self.updating_rollLbl = tk.Label(self, text = "Roll", textvariable = self.updating_roll, fg = 'white', bg = 'black')
		self.updating_rollLbl.pack() 
		self.RollLbl = tk.Label(self, text = "Roll: ", fg = 'white', bg = 'black')
		self.RollLbl.pack(padx = 5, pady = 10, side = tk.RIGHT)
		self.updating_rollLbl.pack(padx = 5, pady = 5, side = tk.RIGHT)

		#Accel Z
		self.updating_az = tk.IntVar()
		self.updating_az.set(0)
		self.updating_azLbl = tk.Label(self, text = "Accel Z: ", textvariable = self.updating_roll, fg = 'white', bg = 'black')
		self.updating_azLbl.pack() 
		self.AzLbl = tk.Label(self, text = "Accel Z: ", fg = 'white', bg = 'black')
		self.AzLbl.pack(padx = 5, pady = 10, side = tk.RIGHT)
		self.updating_azLbl.pack(padx = 5, pady = 5, side = tk.RIGHT)

		#Accel Y
		self.updating_ay = tk.IntVar()
		self.updating_ay.set(0)
		self.updating_ayLbl = tk.Label(self, text = "Accel Y: ", textvariable = self.updating_roll, fg = 'white', bg = 'black')
		self.updating_ayLbl.pack() 
		self.AyLbl = tk.Label(self, text = "Accel Y: ", fg = 'white', bg = 'black')
		self.AyLbl.pack(padx = 5, pady = 10, side = tk.RIGHT)
		self.updating_ayLbl.pack(padx = 5, pady = 5, side = tk.RIGHT)

		#Accel X
		self.updating_ax = tk.IntVar()
		self.updating_ax.set(0)
		self.updating_axLbl = tk.Label(self, text = "Accel X: ", textvariable = self.updating_roll, fg = 'white', bg = 'black')
		self.updating_axLbl.pack() 
		self.AxLbl = tk.Label(self, text = "Accel X: ", fg = 'white', bg = 'black')
		self.AxLbl.pack(padx = 5, pady = 10, side = tk.RIGHT)
		self.updating_axLbl.pack(padx = 5, pady = 5, side = tk.RIGHT)

		#Magz
		self.updating_mz = tk.IntVar()
		self.updating_mz.set(0)
		self.updating_mzLbl = tk.Label(self, text = "Mag Z: ", textvariable = self.updating_roll, fg = 'white', bg = 'black')
		self.updating_mzLbl.pack() 
		self.MzLbl = tk.Label(self, text = "Mag Z: ", fg = 'white', bg = 'black')
		self.MzLbl.pack(padx = 5, pady = 10, side = tk.RIGHT)
		self.updating_mzLbl.pack(padx = 5, pady = 5, side = tk.RIGHT)
		
		#Magy
		self.updating_my = tk.IntVar()
		self.updating_my.set(0)
		self.updating_myLbl = tk.Label(self, text = "Mag Y: ", textvariable = self.updating_roll, fg = 'white', bg = 'black')
		self.updating_myLbl.pack() 
		self.MyLbl = tk.Label(self, text = "Mag Y: ", fg = 'white', bg = 'black')
		self.MyLbl.pack(padx = 5, pady = 10, side = tk.RIGHT)
		self.updating_myLbl.pack(padx = 5, pady = 5, side = tk.RIGHT)

		#Magx
		self.updating_mx = tk.IntVar()
		self.updating_mx.set(0)
		self.updating_mxLbl = tk.Label(self, text = "Mag X: ", textvariable = self.updating_roll, fg = 'white', bg = 'black')
		self.updating_mxLbl.pack() 
		self.MxLbl = tk.Label(self, text = "Mag X: ", fg = 'white', bg = 'black')
		self.MxLbl.pack(padx = 5, pady = 10, side = tk.RIGHT)
		self.updating_mxLbl.pack(padx = 5, pady = 5, side = tk.RIGHT)



		self.counter = Process(target = count, args = (self.child_pipe, self.child1_pipe, self.child2_pipe, self.child3_pipe, self.child4_pipe, self.child5_pipe, self.child6_pipe, self.child7_pipe, self.child8_pipe, self.child9_pipe, parent, self.stop_event))
		self.counter.start()
		self.update()

	def update(self):
		while self.parent_pipe.poll():
			self.updating_int.set(self.parent_pipe.recv())
			self.updating_roll.set(self.parent1_pipe.recv())
			self.updating_pitch.set(self.parent2_pipe.recv())
			self.updating_yaw.set(self.parent3_pipe.recv())
			self.updating_ax.set(self.parent4_pipe.recv())
			self.updating_ay.set(self.parent5_pipe.recv())
			self.updating_az.set(self.parent6_pipe.recv())
			self.updating_mx.set(self.parent7_pipe.recv())
			self.updating_my.set(self.parent8_pipe.recv())
			self.updating_mz.set(self.parent9_pipe.recv())
		self.parent.after(100, self.update)

	def quit(self):
		print "here"
		self.stop_event.set()
		self.parent.destory()
		self.frame.destory()

def connections():
	Connections = tk.Tk()
	Connections.title('Connection')

	connect = tk.Button(Connections, text = 'Connect', command = sendConnect)
	connect.pack()

	check = tk.Button(Connections, text = 'Check Connection', command = Check)
	check.pack()

	close = tk.Button(Connections, text = 'Close Connection', command = endConnect)
	close.pack()

def sendConnect():
	global connect
	if connect == 0:
		print "send connection"
		c.send("10")
		msg = c.recv(1)
		if msg == "0":
			tkMessageBox.showinfo("Connection!", "Connection Successful")
			connect = 1
		#print connected
		elif msg == "1":
			tkMessageBox.showerror("Connection!", "There is an Error with the IMU")
			connect = 0
		else:
			tkMessageBox.showerror("Connection!", msg)
			connect = 0
			return
	elif connect == 1:
		tkMessageBox.showerror("Connection!", "Already Connected")
		return


###Have to do this one
def Check():
	print "checking connection"




def endConnect():
	global connect
	if connect == 1:
		c.send("15")
		msg = c.recv(6)
		if msg == "closed":
			tkMessageBox.showinfo("Connection!", "Connection Terminated")
			connect = 0
		else:
			tkMessgeBox.showerror("Connection!", "The connection is still live")
			connect = 1
	else:
		tkMessageBox.showinfo("Connection!", "Connection Terminated")



def Manual():
	global Oldvalue1
	global Oldvalue2
	global Oldvalue3
	global Oldvalue4
	Manual = tk.Tk()
	Manual.title('Manual Mode')


	def Airski1():
		print E1.get()
		newVal = int(E1.get())
		print newVal
		if(newVal >= 0 and newVal <= 180):
			if(newVal >= 0 and newVal <= 9):
				newVal = "00" + str(newVal)
			elif(newVal >= 10 and newVal <= 99):
				newVal = "0"+ str(newVal)
			elif(newVal >= 100 and newVal <= 180):
				newVal = str(newVal)
		else:
			tkMessageBox.showerror("AirSki1", "Incorrect Value")
		c.send("17") #code for airski1 change
		msg = c.recv(3) #RFC ready for change
		if msg == "RFC":
			c.send(newVal)
			msg = c.recv(2) #CC change complete
			if msg == "cc":
				tkMessageBox.showinfo("Airski1", "Change Successful")
			else:
				tkMessageBox.showerror("Airski1", "Change was not complelete, error: " + msg)
				return
		else:
			tkMessageBox.showerror("Airski1", "Change was not complelete, error: " + msg)
			return
	Airski1Lbl = tk.Label(Manual, text = "Airski 1")
	Airski1Lbl.pack()
	E1 = tk.Entry(Manual, bd = 5)
	E1.pack()
	change1 = tk.Button(Manual, text = "Make Change", command = Airski1)
	change1.pack()

	
	def Airski2():
		print E2.get()
		newVal = int(E2.get())
		print newVal
		if(newVal >= 0 and newVal <= 180):
			if(newVal >= 0 and newVal <= 9):
				newVal = "00" + str(newVal)
			elif(newVal >= 10 and newVal <= 99):
				newVal = "0"+ str(newVal)
			elif(newVal >= 100 and newVal <= 180):
				newVal = str(newVal)
		else:
			tkMessageBox.showerror("Airski2", "Incorrect Value")
		c.send("18") #code for airski1 change
		msg = c.recv(3) #RFC ready for change
		if msg == "RFC":
			c.send(newVal)
			msg = c.recv(2) #CC change complete
			if msg == "cc":
				tkMessageBox.showinfo("Airski2", "Change Successful")
			else:
				tkMessageBox.showerror("Airski2", "Change was not complete, error: " + msg)
				return
		else:
			tkMessageBox.showerror("Airski2", "Change was not complete, error: " + msg)
			return
	Airski2Lbl = tk.Label(Manual, text = "Airski 2")
	Airski2Lbl.pack()
	E2 = tk.Entry(Manual, bd = 5)
	E2.pack()
	b2 = tk.Button(Manual, text = 'Make Change', command = Airski2)
	b2.pack()

	
	def Airski3():
		print E3.get()
		newVal = int(E3.get())
		print newVal
		if(newVal >= 0 and newVal <= 180):
			if(newVal >= 0 and newVal <= 9):
				newVal = "00" + str(newVal)
			elif(newVal >= 10 and newVal <= 99):
				newVal = "0"+ str(newVal)
			elif(newVal >= 100 and newVal <= 180):
				newVal = str(newVal)
		else:
			tkMessageBox.showerror("Airski3", "Incorrect Value")
		c.send("19") #code for airski1 change
		msg = c.recv(3) #RFC ready for change
		if msg == "RFC":
			c.send(newVal)
			msg = c.recv(2) #CC change complete
			if msg == "cc":
				tkMessageBox.showinfo("Airski3", "Change Successful")
			else:
				tkMessageBox.showerror("Airski3", "Change was not complete, error: " + msg)
				return
		else:
			tkMessageBox.showerror("Airski3", "Change was not complete, error: " + msg)
			return
	Airski3Lbl = tk.Label(Manual, text = "Airski 3")
	Airski3Lbl.pack()
	E3 = tk.Entry(Manual, bd = 5)
	E3.pack()
	b3 = tk.Button(Manual, text = 'Make Change', command = Airski3)
	b3.pack()

	
	def Airski4():
		print E4.get()
		newVal = int(E4.get())
		print newVal
		if(newVal >= 0 and newVal <= 180):
			if(newVal >= 0 and newVal <= 9):
				newVal = "00" + str(newVal)
			elif(newVal >= 10 and newVal <= 99):
				newVal = "0"+ str(newVal)
			elif(newVal >= 100 and newVal <= 180):
				newVal = str(newVal)
		else:
			tkMessageBox.showerror("Airski4", "Incorrect Value")

		c.send("20") #code for airski1 change
		msg = c.recv(3) #RFC ready for change
		if msg == "RFC":
			c.send(newVal)
			msg = c.recv(2) #CC change complete
			if msg == "cc":
				tkMessageBox.showinfo("Airski4", "Change Complete")
			else:
				tkMessageBox.showerror("Airski4", "Change was not complete")
		else:
			tkMessageBox.showerror("Airski4", "Change was not complete. Error: " + msg)
			return

	Airski4Lbl = tk.Label(Manual, text = "Airski 4")
	Airski4Lbl.pack()
	E4 = tk.Entry(Manual, bd = 5)
	E4.pack()
	b4 = tk.Button(Manual, text = 'Make Change', command = Airski4)
	b4.pack()

	def All():
		print E5.get()
		newVal = int(E5.get())
		print newVal
		if(newVal >= 0 and newVal <= 180):
			if(newVal >= 0 and newVal <= 9):
				newVal = "00" + str(newVal)
			elif(newVal >= 10 and newVal <= 99):
				newVal = "0"+ str(newVal)
			elif(newVal >= 100 and newVal <= 180):
				newVal = str(newVal)
		else:
			tkMessageBox.showerror("All Skis", "Incorrect Value")

		c.send("21") #code for airski1 change
		msg = c.recv(3) #RFC ready for change
		if msg == "RFC":
			c.send(newVal)
			msg = c.recv(2) #CC change complete
			if msg == "cc":
				tkMessageBox.showinfo("All Skis", "Change Complete")
			else:
				tkMessageBox.showerror("All Skis", "Change was not complete")
		else:
			tkMessageBox.showerror("All Skis", "Change was not complete. Error: " + msg)
			return

	AllSki = tk.Label(Manual, text = "All Skis")
	AllSki.pack()
	E5 = tk.Entry(Manual, bd = 5)
	E5.pack()
	b5 = tk.Button(Manual, text = 'Make Change', command = Airski4)
	b5.pack()

	

def AutoPilot():
	print "AutoPilot"

def Hover(gui):
	c.send("11")
	msg = c.recv(2)
	if msg == "hc":
		tkMessageBox.showinfo("Hover","Hover Complete")
		gui.place(x = 175, y = 5)
	else:
		tkMessageBox.showerror("Hover", "There was an issue when trying to hover. Error: " + msg)

def Land():
	c.send("16")
	msg = c.recv(2)
	if msg == "lc":
		tkMessageBox.showinfo("Land", "Land Complete")
	else:
		tkMessageBox.showerror("Land", "There was an error when trying to land. Error: " + msg)

def controler(gui):
	controls = tk.Tk()
	controls.title('Controls')

	hover = tk.Button(controls, text = 'Hover', command = lambda: Hover(gui))
	hover.pack()
	manual = tk.Button(controls, text = 'Manual', command = Manual)
	manual.pack()

	autoPilot = tk.Button(controls, text = 'Auto Pilot', command = AutoPilot)
	autoPilot.pack()

	land = tk.Button(controls, text = 'Land', command = Land)
	land.pack()

def Stop():
	stopper = tk.Tk()
	stopper.title('Emergency Stop')

	def check():
		passw = E.get()
		if passw == "4656":
			print "Stop"
			c.send("14")
			msg = c.recv(2)
			if msg == "sc":
				tkMessageBox.showinfo("Emergency Stop", "The Testbed has Landed")
				endConnect()
			else:
				tkMessageBox.showerror("Emergency Stop", "There was an Error Stopping a Testbed. Error: " + msg)
		else:
			tkMessageBox.showerror("Emergency Stop", "Incorrect Password")
			
	question = tk.Label(text = 'Please Enter 4 Digit Code')
	E = tk.Entry(stopper, bd = 5)
	E.pack()
	B = tk.Button(stopper, text = 'Stop', command = check)
	B.pack()




def main():
	root = tk.Tk()
	root.title('Control Center')
	root.geometry('2050x800')

	canvas = tk.Canvas(width = 700, height = 600, bg = 'black')
	background = tk.PhotoImage(file = 'background.gif')
	canvas.create_image(0, 30, image = background, anchor = 'nw')
	canvas.pack(expand = 'yes', fill = 'both')


	stopIm = tk.PhotoImage(file = 'Stop.gif')
	stopButton = tk.Button(root, image = stopIm, background = 'black', height = 65, width = 65, command = Stop)
	stopButton.place(x = 0, y = 0)

	gui = UpdatingGUI(root)
	controls = tk.PhotoImage(file = 'controls.gif')
	controlButton = tk.Button(root, image = controls, bg = 'black', height = 65, width = 65, command = lambda: controler(gui))
	controlButton.place(x = 70, y = 0)

	connection = tk.PhotoImage(file = 'Connection.gif')
	connectButton = tk.Button(root, image = connection, bg = 'black', height = 65, width = 65, command = connections)
	connectButton.place(x = 1200, y = 0)

	title = tk.PhotoImage(file = 'Title.gif')
	titleLbl = tk.Label(root, image = title, bg = 'black')
	titleLbl.place(x = 325, y = 50)


	RedLbl = tk.Label(root, text = "Light Detection: ", fg = 'white', bg = 'black')
	RedLbl.place(x = 1150, y = 125)
	Light = tk.PhotoImage(file = 'vbar.gif')
	Red = tk.PhotoImage(file = 'RED.gif')
	LightLbl = tk.Label(root, image = Light, bg = 'black')
	LightLbl.place(x = 1190, y = 150)

	testP = tk.PhotoImage(file = 'TestBed.gif')
	testLbl = tk.Label(root, image = testP, height = 550, width = 770, bg = 'black')
	testLbl.place(x = 150, y = 150)

	


	#canvas = tk.Canvas(width = 700, height = 600, bg = 'black')
	#canvas.create_image(0, 30, image = testP, anchor = 'nw')
	#canvas.place(x = 150, y = 150)

	root.mainloop()



main()