from PIL import Image
import Tkinter as tk
import shutil
import os
import ttk as ttk
import time, datetime, sys, struct
from multiprocessing import *
import tkMessageBox

connect = 0
red = 0

def count(pipe, pipe1, pipe2, pipe3, pipe4, pipe5, pipe6, pipe7, pipe8, pipe9, root, stop):
	global connect
	global red
	ii = 0
	iii = 1
	iiii = 2
	iv = 3
	vi = 4
	print connect
	while not stop.is_set():
		ii+=1
		iii +=1
		iiii +=1
		iv+=1
		vi+=1
		pipe.send(ii)
		pipe1.send(iii)
		pipe2.send(iiii)
		pipe3.send(iv)
		pipe4.send(vi)
		pipe5.send(vi)
		pipe6.send(vi)
		pipe7.send(vi)
		pipe8.send(vi)
		pipe9.send(vi)
		
		time.sleep(.5)



class UpdatingGUI(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent, bg = 'black')
		self.parent = parent
		self.parent_pipe, self.child_pipe, = Pipe()
		self.parent1_pipe, self.child1_pipe = Pipe()
		self.parent2_pipe, self.child2_pipe = Pipe()
		self.parent3_pipe, self.child3_pipe = Pipe()
		self.parent4_pipe, self.child4_pipe = Pipe()
		self.parent5_pipe, self.child5_pipe = Pipe()
		self.parent6_pipe, self.child6_pipe = Pipe()
		self.parent7_pipe, self.child7_pipe = Pipe()
		self.parent8_pipe, self.child8_pipe = Pipe()
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
	print connect
	if connect == 0:
		print "send connection"
		connect = 1
		tkMessageBox.showinfo("Connection", "Connection Successful")
	elif connect == 1:
		print "already connected"
		tkMessageBox.showinfo("Connection", "Already Connected")

def Check():
	print "checking connection"


def endConnect():
	print "end connection"

def Manual():
	Manual = tk.Tk()
	Manual.title('Manual Mode')


	def Airski1():
		print E1.get()
	Airski1Lbl = tk.Label(Manual, text = "Airski 1")
	Airski1Lbl.pack()
	E1 = tk.Entry(Manual, bd = 5)
	E1.pack()
	change1 = tk.Button(Manual, text = "Make Change", command = Airski1)
	change1.pack()

	
	def Airski2():
		print E2.get()
	Airski2Lbl = tk.Label(Manual, text = "Airski 2")
	Airski2Lbl.pack()
	E2 = tk.Entry(Manual, bd = 5)
	E2.pack()
	b2 = tk.Button(Manual, text = 'Make Change', command = Airski2)
	b2.pack()

	
	def Airski3():
		print E3.get()
	Airski3Lbl = tk.Label(Manual, text = "Airski 3")
	Airski3Lbl.pack()
	E3 = tk.Entry(Manual, bd = 5)
	E3.pack()
	b3 = tk.Button(Manual, text = 'Make Change', command = Airski3)
	b3.pack()

	
	def Airski4():
		print E4.get()
	Airski4Lbl = tk.Label(Manual, text = "Airski 4")
	Airski4Lbl.pack()
	E4 = tk.Entry(Manual, bd = 5)
	E4.pack()
	b4 = tk.Button(Manual, text = 'Make Change', command = Airski4)
	b4.pack()

	def All():
		print E5.get();
	AllSkis = tk.Label(Manual, text = "All Airskis")
	AllSkis.pack()
	E5 = tk.Entry(Manual, bd = 5)
	E5.pack()
	b5 = tk.Button(Manual, text = 'Change All', command = All)
	b5.pack()

	

def AutoPilot():
	print "AutoPilot"

def Hover(gui):
	global connect
	if connect == 1:
		print "Hover"
		gui.place(x = 175, y = 5)

def Land():
	print "Land"


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
		else:
			print "Incorrect Password"

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


	root.mainloop()
	gui.quit()
main()
