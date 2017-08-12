# from PIL import Image
import tkinter as tk
# from tkinter import ttk
import time
import struct
import threading
# import random
# import sys
# import datetime, sys, struct
# import shutil
# import os
from multiprocessing import *
import socket
from tkinter import messagebox
# import paramiko
# import subprocess


# host = '192.168.1.107'
# port = 12571
# host = '192.168.0.101'
# port = 10004
# c.connect((host, port))
# server_address = ('192.168.0.101', 10004)
server_address = ('149.125.118.49', 10004)
# server_address = ('10.201.10.192', 10004)
# server_address = ('192.168.1.64', 10004)
sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# sock1.setblocking(0)
# sock1.settimeout(10)

UDP_IP = "localhost"
UDP_PORT = 3000
MESSAGE = "Hello, World!"
sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

root = tk.Tk()
root.title('Control Center')
root.geometry('2050x800')
f = open('SensorLog', 'w')

parent0_pipe, child0_pipe, = Pipe()
parent1_pipe, child1_pipe = Pipe()
parent2_pipe, child2_pipe = Pipe()
parent3_pipe, child3_pipe = Pipe()
parent4_pipe, child4_pipe = Pipe()
parent5_pipe, child5_pipe = Pipe()
parent6_pipe, child6_pipe = Pipe()
parent7_pipe, child7_pipe = Pipe()
parent8_pipe, child8_pipe = Pipe()
parent9_pipe, child9_pipe = Pipe()
parent10_pipe, child10_pipe = Pipe()
parent11_pipe, child11_pipe = Pipe()
parent12_pipe, child12_pipe = Pipe()
parent13_pipe, child13_pipe = Pipe()
parent14_pipe, child14_pipe = Pipe()
parent15_pipe, child15_pipe = Pipe()
parent16_pipe, child16_pipe = Pipe()
parent17_pipe, child17_pipe = Pipe()

#temp < 60C
#Voltage(all three) 16.8V max, low 12V
#current max: 50
#actuators: still pending


connection = 0
tryConn = False
conn = ''
data = ''
diagram = ''
state = 1

unpacker = struct.Struct('3I 15f')

def getData():
    global conn
    # global connection
    # conn, client_address = sock1.accept()
    # message = struct.pack('i', 12)
    # conn.sendto(message, server_address)
    # s = sock1.recv(2)  # size
    # s = conn.recv(500)
    # if s.isdigit() and connection == 1:
    if connection == 1:
        packedData = conn.recv(unpacker.size)
        unpackedData = unpacker.unpack(packedData)
        # size = int(s)
        # message2 = struct.pack('i', 13)
        # conn.sendto(message2, server_address)
        # msg = str(conn.recv(size))
        # f.write(msg)
        # f.write('\n')
        # msg = conn.recv(37)
        # msg = msg.decode('utf-8')
        # msg = msg.split(',')
        # connection.sendall('0')  # transmit data from gui to spacex/
        # print('sending 0')

        # # data sent to spaceX
        # # convert data to string to be sent nicely to spacex
        # MESSAGE1 = struct.pack('BB',
        #                        69,  # team ID, given to us by space X
        #                        2)
        # MESSAGE2 = struct.pack('iiiiiiiI',
        #                        # int(dataArray[9]),
        #                        # int(dataArray[0]),
        #                        # int(dataArray[1]),
        #                        int(1),
        #                        int(2),
        #                        int(3),
        #                        0,  # zero is optional data that isn't needed
        #                        0,
        #                        0,
        #                        0,
        #                        0)
        # MESSAGE = MESSAGE1 + MESSAGE2
        # print("udp message: " + MESSAGE.decode('utf-8'))
        # # use one way udp connection to send to spacex
        # sock2.sendto(MESSAGE, (UDP_IP, UDP_PORT))

        return unpackedData
    else:
        msg = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    return msg


def count():
    global connection
    global data
    global conn
    conn.send(b'0')
    i = 0
    while connection == 1:
        print('getting data ' + str(i))
        i += 1
        nums = getData()
        print(nums)
        child0_pipe.send(nums[0])
        child1_pipe.send(nums[1])
        child2_pipe.send(nums[2])
        child3_pipe.send(nums[3])
        child4_pipe.send(nums[4])
        child5_pipe.send(nums[5])
        child6_pipe.send(nums[6])
        child7_pipe.send(nums[7])
        child8_pipe.send(nums[8])
        child9_pipe.send(nums[9])
        child10_pipe.send(nums[10])
        child11_pipe.send(nums[11])
        child12_pipe.send(nums[12])
        child13_pipe.send(nums[13])
        child14_pipe.send(nums[14])
        child15_pipe.send(nums[15])
        child16_pipe.send(nums[16])
        child17_pipe.send(nums[17])
        data.update()
        time.sleep(.5)


class UpdatingGUI(tk.Frame):
    def __init__(self, parent):
        global connect
        tk.Frame.__init__(self, parent, bg='white')
        self.parent = parent

        # Time Elapsed
        self.timeint = tk.IntVar()
        self.timeint.set(0)
        self.time = tk.Label(self, text="Time", textvariable=self.timeint, fg='black', bg='white')
        self.timeLbl = tk.Label(self, text="Time Elapsed: ", fg='black', bg='white')
        self.timeLbl.grid(row=0, column=0)
        self.time.grid(row=0, column=1)

        # Tape Count
        self.tapeCountInt = tk.IntVar()
        self.tapeCountInt.set(0)
        self.tapeCount = tk.Label(self, text="Tape Count", textvariable=self.tapeCountInt, fg='black', bg='white')
        self.tapeCountLbl = tk.Label(self, text="Tape Count: ", fg='black', bg='white')
        self.tapeCountLbl.grid(row=1, column=0)
        self.tapeCount.grid(row=1, column=1)

        # Position
        self.posval = tk.DoubleVar()
        self.posval.set(0.0)
        self.pos = tk.Label(self, text="Position", textvariable=self.posval, fg='black', bg='white')
        self.positionLbl = tk.Label(self, text="Position: ", fg='black', bg='white')
        self.positionLbl.grid(row=2, column=0)
        self.pos.grid(row=2, column=1)

        # Acceleration
        self.accelval = tk.DoubleVar()
        self.accelval.set(0.0)
        self.accel = tk.Label(self, text="Acceleration: ", textvariable=self.accelval, fg='black', bg='white')
        self.accelLbl = tk.Label(self, text="Acceleration: ", fg='black', bg='white')
        self.accelLbl.grid(row=3, column=0)
        self.accel.grid(row=3, column=1)

        # Velocity X
        self.vxval = tk.DoubleVar()
        self.vxval.set(0.0)
        self.vx = tk.Label(self, text="Velocity X: ", textvariable=self.vxval, fg='black', bg='white')
        self.vxLbl = tk.Label(self, text="Veclocity X: ", fg='black', bg='white')
        self.vxLbl.grid(row=4, column=0)
        self.vx.grid(row=4, column=1)

        # Velocity Y
        self.vyval = tk.DoubleVar()
        self.vyval.set(0.0)
        self.vy = tk.Label(self, text="Velocity Y: ", textvariable=self.vyval, fg='black', bg='white')
        self.vyLbl = tk.Label(self, text="Veclocity Y: ", fg='black', bg='white')
        self.vyLbl.grid(row=5, column=0)
        self.vy.grid(row=5, column=1)

        # Velocity Z
        self.vzval = tk.DoubleVar()
        self.vzval.set(0.0)
        self.vz = tk.Label(self, text="Velocity Z: ", textvariable=self.vzval, fg='black', bg='white')
        self.vzLbl = tk.Label(self, text="Velocity Z: ", fg='black', bg='white')
        self.vzLbl.grid(row=6, column=0)
        self.vz.grid(row=6, column=1)

        # Roll
        self.rollval = tk.DoubleVar()
        self.rollval.set(0.0)
        self.roll = tk.Label(self, text="Roll", textvariable=self.rollval, fg='black', bg='white')
        self.rollLbl = tk.Label(self, text="Roll: ", fg='black', bg='white')
        self.rollLbl.grid(row=7, column=0)
        self.roll.grid(row=7, column=1)

        # Pitch
        self.pitchval = tk.DoubleVar()
        self.pitchval.set(0.0)
        self.pitch = tk.Label(self, text="Pitch", textvariable=self.pitchval, fg='black', bg='white')
        self.pitchLbl = tk.Label(self, text="Pitch: ", fg='black', bg='white')
        self.pitchLbl.grid(row=8, column=0)
        self.pitch.grid(row=8, column=1)

        # Yaw
        self.yawval = tk.DoubleVar()
        self.yawval.set(0.0)
        self.yaw = tk.Label(self, text="Yaw", textvariable=self.yawval, fg='black', bg='white')
        self.yawLbl = tk.Label(self, text="Yaw: ", fg='black', bg='white')
        self.yawLbl.grid(row=9, column=0)
        self.yaw.grid(row=9, column=1)

        # Amperage 1
        self.amp1val = tk.DoubleVar()
        self.amp1val.set(0.0)
        self.amp1 = tk.Label(self, text="Amperage 1", textvariable=self.amp1val, fg='black', bg='white')
        self.amp1Lbl = tk.Label(self, text="Amperage 1: ", fg='black', bg='white')
        self.amp1Lbl.grid(row=10, column=0)
        self.amp1.grid(row=10, column=1)

        # Amperage 2
        self.amp2val = tk.DoubleVar()
        self.amp2val.set(0.0)
        self.amp2 = tk.Label(self, text="Amperage 2 ", textvariable=self.amp2val, fg='black', bg='white')
        self.amp2Lbl = tk.Label(self, text="Amperage 2: ", fg='black', bg='white')
        self.amp2Lbl.grid(row=11, column=0)
        self.amp2.grid(row=11, column=1)

        # Voltage 1
        self.volt1val = tk.DoubleVar()
        self.volt1val.set(0.0)
        self.volt1 = tk.Label(self, text="Voltage 1", textvariable=self.volt1val, fg='black', bg='white')
        self.volt1Lbl = tk.Label(self, text="Voltage 1: ", fg='black', bg='white')
        self.volt1Lbl.grid(row=12, column=0)
        self.volt1.grid(row=12, column=1)

        # Voltage 2
        self.volt2val = tk.DoubleVar()
        self.volt2val.set(0.0)
        self.volt2 = tk.Label(self, text="Voltage 2", textvariable=self.volt2val, fg='black', bg='white')
        self.volt2Lbl = tk.Label(self, text="Voltage 2: ", fg='black', bg='white')
        self.volt2Lbl.grid(row=13, column=0)
        self.volt2.grid(row=13, column=1)

        # Temperature Ambient
        self.tempAmbVal = tk.DoubleVar()
        self.tempAmbVal.set(0.0)
        self.tempAmb = tk.Label(self, text="Temperature Ambient", textvariable=self.tempAmbVal, fg='black', bg='white')
        self.tempAmbLbl = tk.Label(self, text="Ambient Temperature: ", fg='black', bg='white')
        self.tempAmbLbl.grid(row=14, column=0)
        self.tempAmb.grid(row=14, column=1)

        # Temperature Battery 1
        self.tempBatt1Val = tk.DoubleVar()
        self.tempBatt1Val.set(0.0)
        self.tempBatt1 = tk.Label(self, text="Temperature Battery 1", textvariable=self.tempBatt1Val, fg='black', bg='white')
        self.tempBatt1Lbl = tk.Label(self, text="Battery 1 Temperature: ", fg='black', bg='white')
        self.tempBatt1Lbl.grid(row=15, column=0)
        self.tempBatt1.grid(row=15, column=1)

        # Temperature Battery 2
        self.tempBatt2Val = tk.DoubleVar()
        self.tempBatt2Val.set(0.0)
        self.tempBatt2 = tk.Label(self, text="Temperature Battery 2", textvariable=self.tempBatt2Val, fg='black', bg='white')
        self.tempBatt2Lbl = tk.Label(self, text="Battery 2 Temperature: ", fg='black', bg='white')
        self.tempBatt2Lbl.grid(row=16, column=0)
        self.tempBatt2.grid(row=16, column=1)


    def update(self):
        global state
        state = parent0_pipe.recv()
        self.timeint.set(parent1_pipe.recv())
        self.tapeCountInt.set(parent2_pipe.recv())
        self.posval.set(parent3_pipe.recv())
        self.accelval.set(parent4_pipe.recv())
        self.vxval.set(parent5_pipe.recv())
        self.vyval.set(parent6_pipe.recv())
        self.vzval.set(parent7_pipe.recv())
        self.rollval.set(parent8_pipe.recv())
        self.pitchval.set(parent9_pipe.recv())
        self.yawval.set(parent10_pipe.recv())
        self.amp1val.set(parent11_pipe.recv())
        self.amp2val.set(parent12_pipe.recv())
        self.volt1val.set(parent13_pipe.recv())
        self.volt2val.set(parent14_pipe.recv())
        self.tempAmbVal.set(parent15_pipe.recv())
        self.tempBatt1Val.set(parent16_pipe.recv())
        self.tempBatt2Val.set(parent17_pipe.recv())


        # self.parent.after(100, self.update)

    # def quit(self):
    #     self.stop_event.set()
        # self.parent.destory()
        # self.frame.destory()


class SoftwareStateDiagram(tk.Label):
    def __init__(self, parent):
        tk.Label.__init__(self, parent, bg='black', width=1000, height=600, borderwidth=3, )
        self.parent = parent
        # Row 1

        self.states = []

        self.insertion = tk.Label(self, width=10, height=5, text="Pod Insertion", bg='grey', fg='white')
        self.insertion.place(x=0, y=0)
        self.states.append(self.insertion)

        # self.insertion.grid(row=1, column=1)
        self.idle = tk.Label(self, width=10, height=5, text="Idle", background='gray', fg='white')
        self.idle.place(x=160, y=0)
        self.states.append(self.idle)

        self.sysCheck = tk.Label(self, width=10, height=5, text="System Check", background='gray', fg='white')
        self.sysCheck.place(x=320, y=0)
        self.states.append(self.sysCheck)

        self.ready = tk.Label(self, width=10, height=5, text="Ready", background='gray', fg='white')
        self.ready.place(x=480, y=0)
        self.states.append(self.place)

        self.pushing = tk.Label(self, width=10, height=5, text="Pushing", background='gray', fg='white')
        self.pushing.place(x=640, y=0)
        self.states.append(self.pushing)

        # Row 2
        self.reconnect = tk.Label(self, width=10, height=5, text="Reconnect\nAttempt", background='gray', fg='white')
        self.reconnect.place(x=0, y=160)
        self.states.append(self.reconnect)

        self.faultBreaks = tk.Label(self, width=10, height=5, text="Fault\n(Brakes)", background='gray', fg='white')
        self.faultBreaks.place(x=320, y=160)
        self.states.append(self.faultBreaks)

        self.faultNoBreaks = tk.Label(self, width=10, height=5, text="Fault\n(No Brakes)", background='gray', fg='white')
        self.faultNoBreaks.place(x=480, y=160)
        self.states.append(self.faultNoBreaks)

        self.coasting = tk.Label(self, width=10, height=5, text="Coasting", background='gray', fg='white')
        self.coasting.place(x=640, y=160)
        self.states.append(self.coasting)

        # Row 3
        self.diagnostic = tk.Label(self, width=10, height=5, text="Diagnostic", background='red', fg='white')
        self.diagnostic.place(x=0, y=320)
        self.states.append(self.diagnostic)

        self.brakeOverride = tk.Label(self, width=10, height=5, text="Manual\nBrake\nOverride", background='blue', fg='white')
        self.brakeOverride.place(x=160, y=320)
        self.states.append(self.brakeOverride)

        self.powerOff = tk.Label(self, width=10, height=5, text="Power Off", background='gray',fg='white')
        self.powerOff.place(x=320, y=320)
        self.states.append(self.powerOff)

        self.disengage = tk.Label(self, width=10, height=5, text="Disengage\nBrakes", background='gray', fg='white')
        self.disengage.place(x=480, y=320)
        self.states.append(self.disengage)

        self.braking = tk.Label(self, width=10, height=5, text="Braking", background='gray', fg='white')
        self.braking.place(x=640, y=320)
        self.states.append(self.braking)

        self.flash()

    def flash(self):
        global state
        current_color = self.states[state].cget("background")

        if state != 9 and state != 10:
            if current_color == "grey":
                next_color = "yellow"
                next_text = "black"
            else:
                next_color = "grey"
                next_text = "white"
        elif state == 9:
            if current_color == "red":
                next_color = "yellow"
                next_text = "black"
            else:
                next_color = "red"
                next_text = "white"
        else:
            if current_color == "blue":
                next_color = "yellow"
                next_text = "black"
            else:
                next_color = "blue"
                next_text = "white"
        self.states[state].config(background=next_color, fg=next_text)
        root.after(500, self.flash)


def sendtoConnect():
    global connection, tryConn, conn
    while (tryConn == False):
        pass
    # print('got here .25')
    # connection, client_address = sock1.accept()
    # print(connection)
    # print('got here .5')
    if connection == 0:
        sock1.bind(server_address)
        sock1.listen(1)
        conn, addr = sock1.accept()
        # message = struct.pack('i', 10)
        # connection.sendto(message, client_address)
        msg = conn.recv(1)
        # msg = struct.unpack('c', msg)
        msg = msg.decode("utf-8")
        if msg == '0':
            messagebox.showinfo("Connection!", "Connection Successful")
            connection = 1
        # elif msg == "1":
        #     messagebox.showerror("Connection!", "There is an Error with the IMU")
        #     connection = 0
        # elif msg == "2":  # light sensor
        #     messagebox.showerror("Connection!", "There is an Error with the Light Sensor")
        # elif msg == "3":  # both
        #     messagebox.showerror("Connection!", "There is an error with both the IMU and the Light Sensor")
        #     connection = 0
            count()
        else:
            messagebox.showerror("Connection!", msg)
            connection = 0
            return
    elif connection == 1:
        messagebox.showerror("Connection!", "Already Connected")
        return


def Check():
    global connection
    # message = struct.pack('i', 22)
    # sock1.sendto(message, server_address)
    # msg = sock1.recv(2)  # ce
    # if msg == "ce":
    #     messagebox.showinfo("Connection!", "Connection is good!")
    # else:
    #     messagebox.showerror("Connection!", "Connection was lost")
    if(connection == 1):
        messagebox.showinfo("Connection!", "Connection is good!")
    else:
        messagebox.showinfo("Connection!", "There is currently no connection.")


def endConnect():
    global connection, conn
    if connection == 1:
        sock1.close()
        # message = struct.pack('i', 15)
        # sock1.sendto(message, server_address)
        # msg = sock1.recv(6)
        connection = 0
        messagebox.showinfo("Connection!", "The conneciton has been disabled.")
        # if msg == "closed":
        #     connection = 0
        # else:
        #     # messagebox.showerror("Connection!", "The connection is still live")
        #     connection = 1
    else:
        connection = 0
        messagebox.showinfo("Connection!", "There was no connection.")


def connections(connectionsFrame):
    Connections = tk.Label(connectionsFrame, width=20, height=10, background='black')
    Connections.place(x=100, y=100)
    # Connections.title('Connection')

    connect = tk.Button(Connections, text='Connect', command=tryConnection)
    connect.place(x=20,y=0)

    check = tk.Button(Connections, text='Check Connection', command=Check)
    check.place(x=0, y=30)

    close = tk.Button(Connections, text='Close Connection', command=endConnect)
    close.place(x=2,y=60)


def tryConnection():
    global tryConn
    tryConn = True


def Manual():
    Manual = tk.Tk()
    Manual.title('Manual Mode')

    def Airski1(n):
        global complete1
        if n == 0:
            newVal = int(E1.get())
        else:
            newVal = int(n)
        if (newVal >= 0 and newVal <= 180):
            if (newVal >= 0 and newVal <= 9):
                newVal = "00" + str(newVal)
            elif (newVal >= 10 and newVal <= 99):
                newVal = "0" + str(newVal)
            elif (newVal >= 100 and newVal <= 180):
                newVal = str(newVal)
        else:
            messagebox.showerror("AirSki1", "Incorrect Value")
            return
        message = struct.pack('i', 17)
        sock1.sendto(message, server_address)  # code for airski1 change
        msg = sock1.recv(3)  # RFC ready for change
        if msg == "RFC":
            message2 = struct.pack('i', newVal)
            sock1.sendto(message2, server_address)
            msg = sock1.recv(2)  # CC change complete
            if msg == "cc" and n == 0:
                messagebox.showinfo("Airski1", "Change Successful")
                complete1 = 0
            elif msg == "cc" and n != 0:
                complete1 = 1
            else:
                messagebox.showerror("Airski1", "Change was not complelete, error: " + msg)
                return
        else:
            messagebox.showerror("Airski1", "Change was not complelete, error: " + msg)
            return

    Airski1Lbl = tk.Label(Manual, text="Airski 1")
    Airski1Lbl.pack()
    E1 = tk.Entry(Manual, bd=5)
    E1.pack()
    change1 = tk.Button(Manual, text="Make Change", command=lambda: Airski1(0))
    change1.pack()

    def Airski2(n):
        global complete2
        if n == 0:
            newVal = int(E2.get())
        else:
            newVal = int(n)
        if (newVal >= 0 and newVal <= 180):
            if (newVal >= 0 and newVal <= 9):
                newVal = "00" + str(newVal)
            elif (newVal >= 10 and newVal <= 99):
                newVal = "0" + str(newVal)
            elif (newVal >= 100 and newVal <= 180):
                newVal = str(newVal)
        else:
            messagebox.showerror("Airski2", "Incorrect Value")
            return
        message = struct.pack('i', 18)
        sock1.sendto(message, server_address)  # code for airski1 change
        msg = sock1.recv(3)  # RFC ready for change
        if msg == "RFC":
            message2 = struct.pack('i', newVal)
            sock1.sendto(message2, server_address)
            msg = sock1.recv(2)  # CC change complete
            if msg == "cc" and n == 0:
                messagebox.showinfo("Airski2", "Change Successful")
                complete2 = 0
            elif msg == "cc" and n != 0:
                complete2 = 1
            else:
                messagebox.showerror("Airski2", "Change was not complete, error: " + msg)
                return
        else:
            messagebox.showerror("Airski2", "Change was not complete, error: " + msg)
            return

    Airski2Lbl = tk.Label(Manual, text="Airski 2")
    Airski2Lbl.pack()
    E2 = tk.Entry(Manual, bd=5)
    E2.pack()
    b2 = tk.Button(Manual, text='Make Change', command=lambda: Airski2(0))
    b2.pack()

    def Airski3(n):
        global complete3
        if n == 0:
            newVal = int(E3.get())
        else:
            newVal = int(n)
        if (newVal >= 0 and newVal <= 180):
            if (newVal >= 0 and newVal <= 9):
                newVal = "00" + str(newVal)
            elif (newVal >= 10 and newVal <= 99):
                newVal = "0" + str(newVal)
            elif (newVal >= 100 and newVal <= 180):
                newVal = str(newVal)
        else:
            messagebox.showerror("Airski3", "Incorrect Value")
            return
        message = struct.pack('i', 18)
        sock1.sendto(message, server_address)  # code for airski1 change
        msg = sock1.recv(3)  # RFC ready for change
        if msg == "RFC":
            message2 = struct.pack('i', newVal)
            sock1.sendto(message2, server_address)
            msg = sock1.recv(2)  # CC change complete
            if msg == "cc" and n == 0:
                messagebox.showinfo("Airski3", "Change Successful")
                complete3 = 0
            elif msg == "cc" and n != 0:
                complete3 = 1
            else:
                messagebox.showerror("Airski3", "Change was not complete, error: " + msg)
                return
        else:
            messagebox.showerror("Airski3", "Change was not complete, error: " + msg)
            return

    Airski3Lbl = tk.Label(Manual, text="Airski 3")
    Airski3Lbl.pack()
    E3 = tk.Entry(Manual, bd=5)
    E3.pack()
    b3 = tk.Button(Manual, text='Make Change', command=lambda: Airski3(0))
    b3.pack()

    def Airski4(n):
        global complete4
        if n == 0:
            newVal = int(E4.get())
        else:
            newVal = int(n)
        if (newVal >= 0 and newVal <= 180):
            if (newVal >= 0 and newVal <= 9):
                newVal = "00" + str(newVal)
            elif (newVal >= 10 and newVal <= 99):
                newVal = "0" + str(newVal)
            elif (newVal >= 100 and newVal <= 180):
                newVal = str(newVal)
        else:
            messagebox.showerror("Airski4", "Incorrect Value")
            return
        message = struct.pack('i', 20)
        sock1.sendto(message, server_address)  # code for airski1 change
        msg = sock1.recv(3)  # RFC ready for change
        if msg == "RFC":
            message2 = struct.pack('i', newVal)
            sock1.sendto(message2, server_address)
            msg = sock1.recv(2)  # CC change complete
            if msg == "cc" and n == 0:
                messagebox.showinfo("Airski4", "Change Complete")
                complete4 = 0
            elif msg == "cc" and n != 0:
                complete4 = 1
            else:
                messagebox.showerror("Airski4", "Change was not complete")
        else:
            messagebox.showerror("Airski4", "Change was not complete. Error: " + msg)
            return

    Airski4Lbl = tk.Label(Manual, text="Airski 4")
    Airski4Lbl.pack()
    E4 = tk.Entry(Manual, bd=5)
    E4.pack()
    b4 = tk.Button(Manual, text='Make Change', command=lambda: Airski4(0))
    b4.pack()

    def All():
        newVal = int(E5.get())
        if (newVal >= 0 and newVal <= 180):
            if (newVal >= 0 and newVal <= 9):
                newVal = "00" + str(newVal)
            elif (newVal >= 10 and newVal <= 99):
                newVal = "0" + str(newVal)
            elif (newVal >= 100 and newVal <= 180):
                newVal = str(newVal)
            Airski4(newVal)
            Airski1(newVal)
            Airski2(newVal)
            Airski3(newVal)
        else:
            messagebox.showerror("All Skis", "Incorrect Value")
            return
        if complete1 == 1 and complete2 == 1 and complete3 == 1 and complete4 == 1:
            messagebox.showinfo("All Skis", "All changes complete")
        else:
            # make this show which did not compelte
            messagebox.showerror("All Skis", "Not all changes compelte")

    AllSki = tk.Label(Manual, text="All Skis")
    AllSki.pack()
    E5 = tk.Entry(Manual, bd=5)
    E5.pack()
    b5 = tk.Button(Manual, text='Make Change', command=All)
    b5.pack()


def getSensorData(root):
    global data
    data = UpdatingGUI(root)
    data.place(x=100, y=400)

def getStateDiagram(root):
    global diagram
    diagram = SoftwareStateDiagram(root)
    diagram.place(x=400, y=200)


def Hover():
    message = struct.pack('i', 11)
    sock1.sendto(message, server_address)
    msg = sock1.recv(2)
    if msg == "hc":
        messagebox.showinfo("Hover", "Hover Complete")
    else:
        messagebox.showerror("Hover", "There was an issue when trying to hover. Error: " + msg)


def Land():
    message = struct.pack('i', 16)
    sock1.sendto(message, server_address)
    msg = sock1.recv(2)
    if msg == "lc":
        messagebox.showinfo("Land", "Land Complete")
    else:
        messagebox.showerror("Land", "There was an error when trying to land. Error: " + msg)


def controller():
    controls = tk.Tk()
    controls.title('Controls')
    controls.geometry('300x200')

    hover = tk.Button(controls, text='Hover', command=Hover)
    hover.pack()

    manual = tk.Button(controls, text='Manual', command=Manual)
    manual.pack()

    auto = tk.Button(controls, text='Auto', command=Hover)
    auto.pack()

    land = tk.Button(controls, text='Land', command=Land)
    land.pack()


def Stop(stopFrame):
    stopper = tk.Label(stopFrame, width=20, height=10, background='black')
    stopper.place(x=100, y=200)

    def check():
        passw = E.get()
        if passw == "laur":
            message = struct.pack('i', 14)
            sock1.sendto(message, server_address)
            msg = sock1.recv(2)
            if msg == "sc":
                messagebox.showinfo("Emergency Stop", "The Testbed has Landed")
                endConnect()
            else:
                messagebox.showerror("Emergency Stop", "There was an Error Stopping a Testbed. Error: " + msg)
        else:
            messagebox.showerror("Emergency Stop", "Incorrect Password")

    question = tk.Label(text='Please Enter 4 Digit Code')
    E = tk.Entry(stopper, bd=5)
    E.place(x=0, y=0)
    B = tk.Button(stopper, text='Stop', command=check)
    B.place(x=0, y=30)

# def startThreading():
#     threading.Thread(target=sendtoConnect).start()

# def updatingData():
#     global data, connection
#     while True:
#         while connection == 0:
#             print('passing')
#         while connection == 1:
#             print('updating')
#             data.update()

def main():
    global root, connection, tryConn
    width, height = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry('%dx%d+0+0' % (width, height))
    canvas = tk.Canvas(width=width, height=height, bg='black')
    # background = tk.PhotoImage(file='background.gif')
    # canvas.create_image(0, 30, image=background, anchor='nw')
    canvas.pack(expand='yes', fill='both')

    # dataIcon = tk.PhotoImage(file='data.gif')
    # dataIcon = dataIcon.zoom(5)
    # dataIcon = dataIcon.subsample(32)
    # statesIcon = tk.PhotoImage(file='states.gif')
    # statesIcon = statesIcon.zoom(5)
    # statesIcon = statesIcon.subsample(32)
    # connectionIcon = tk.PhotoImage(file='Connection.gif')
    # connectionIcon = connectionIcon.zoom(2)
    # stopIcon = tk.PhotoImage(file='Stop.gif')
    # stopIcon = stopIcon.zoom(1)
    #
    # n = ttk.Notebook(width=width, height=height-200)
    # s = ttk.Style()
    # s.configure('tab1.TFrame', text='Sensor Data/Health Check', background='black')
    # s.configure('tab2.TFrame', text='Software State Diagram', background='black')
    # s.configure('tab3.TFrame', text='Connection Check', background='black')
    # s.configure('tab4.TFrame', text='Stop Pod', background='black')
    # dataFrame = ttk.Frame(n, style='tab1.TFrame')
    # stateFrame = ttk.Frame(n, style='tab2.TFrame')
    # connectionFrame = ttk.Frame(n, style='tab3.TFrame')
    # stopFrame = ttk.Frame(n, style='tab4.TFrame')
    # n.add(connectionFrame, text='Connection Check', image=connectionIcon)
    # n.add(dataFrame, text='Sensor Data/Health Check', image=dataIcon)
    # n.add(stateFrame, text='Software State Diagram', image=statesIcon)
    # n.add(stopFrame, text='Stop Pod', image=stopIcon)
    # n.place(x=0, y=0)

    # bgLabel1 = tk.Label(dataFrame, image=background, background='black')
    # bgLabel2 = tk.Label(stateFrame, image=background, background='black')
    # bgLabel3 = tk.Label(connectionFrame, image=background, background='black')
    # bgLabel4 = tk.Label(stopFrame, image=background, background='black')
    # bgLabel1.place(x=0, y=0, relwidth=1, relheight=1)
    # bgLabel2.place(x=0, y=0, relwidth=1, relheight=1)
    # bgLabel3.place(x=0, y=0, relwidth=1, relheight=1)
    # bgLabel4.place(x=0, y=0, relwidth=1, relheight=1)

    getSensorData(canvas)
    getStateDiagram(canvas)
    connections(canvas)
    Stop(canvas)

    # stopIm = tk.PhotoImage(file='Stop.gif')
    # stopButton = tk.Button(root, image=stopIm, background='black', height=65, width=65, command=Stop)
    # stopButton.place(x=500, y=0)

    # controls = tk.PhotoImage(file='controls.gif')
    # controlButton = tk.Button(root, image=controls, bg='black', height=65, width=65, command=controller)
    # controlButton.place(x=70, y=0)

    # connection = tk.PhotoImage(file='Connection.gif')
    # connectButton = tk.Button(root, image=connection, bg='black', height=65, width=65, command=connections)
    # connectButton.place(x=565, y=0)

    title = tk.PhotoImage(file='Title.gif')
    titleLbl = tk.Label(root, image=title, background='black')
    titleLbl.place(x=500, y=2)

    # testP = tk.PhotoImage(file='NewBack.gif')
    # testLbl = tk.Label(root, image=testP, height=450, width=780, bg='black')
    # testLbl.place(x=150, y=155)

    # data = tk.Button(root, text='Sensor Data', command=lambda: getSensorData(root))
    # data.place(x=1100, y=0)

    # threading(root.mainloop())
    threading.Thread(target=sendtoConnect).start()
    threading.Thread(target=root.mainloop()).start()
    # print('after')
    # while(True):
    #     print('here')
    #     while(tryConn == 0):
    #         print('No connection')
    #
    #     tryConn = 0
    #     connection = 0
    # root.mainloop()
    endConnect()


main()
f.close()
