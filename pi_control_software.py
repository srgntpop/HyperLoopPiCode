# Kevin Tarczali     9 August 2017
# pi_control_software.py     version 2

# List of States
# 0  Idle       |   2   Ready           |   3   Pushing          |
# 4  Coasting   |   5   Braking         |   6   Disengage Brakes |
# 7 Power Off   |   11  Fault Brakes    | 12 Fault No Brakes     |

# List of Inputs
# 0 None | 1 Insert Pod |   2   Start | 3   Power Off | 4   Engage Brakes | 5 Disengage Brakes

# Imports
import socket
import struct
import random
import serial

# Constants
ACCELERATION_THRESHOLD = .5         # threshold at which pod can be determined to be accelerating, m/s^2
DECELERATING_THRESHOLD = 0          # threshold at which pod can be determined to be deccelerating, m/s^2
IN_MOTION_THRESHOLD = 2             # threshold at which pod can be determined to be in motion, m/s
MAX_AMPERAGE = 50                   # maximum safe amperage, w
MIN_AMPERAGE = 0                    # minimum safe amperage, w
MAX_DISTANCE = 3000                 # maximum distance pod can travel before brakes engage automatically, m
MAX_TAPE_COUNT = 50                 # maximum tape reads that can be read before brakes engage automatically, #
MAX_TEMPERATURE_AMBIENT = 60        # maximum safe ambient temperature reading in the pod, C
MAX_TEMPERATURE_BATTERY = 60        # maximum safe temperature of battery, C
MAX_TEMPERATURE_PI = 60             # maximum safe temperature of pi, C
MAX_TIME = 1000                     # maximum time pod is coasting before brakes engage automatically, s
MAX_VOLTAGE = 16.8                  # maximum safe voltage, v
MIN_VOLTAGE = 12                    # minimum safe voltage, v
STOPPED_ACCELERATION_HIGH = 0.8     # high-end for acceleration reading when pod is stopped, m/s^2
STOPPED_ACCELERATION_LOW = 0        # low-end for acceleration reading when pod is stopped, m/s^2
STOPPED_VELOCITY_HIGH = 2           # high-end for velocity reading when pod is stopped, m/s
STOPPED_VELOCITY_LOW = 0            # low-end for velocity reading when pod is stopped, m/s
TAPE_COUNT_MOVING = 3               # tape count that indicates pod is moving
TRANSITION_CHECK_COUNT = 10         # number of times a transition is requested before it actually transitions, hysteresis

# sensor variables
guiInput = 0                        # command sent from GUI
mode = 0                            # state that SpaceX has designated in the safety manual
proposedStateNumber = 0             # number corresponding to state that software wishes to change to
proposedStateCount = 0              # number of times state change has been proposed
    # The following sensor variables will be packed and sent to GUI
currentState = 0                    # current state of software
time = 0                            # time counter for coasting, s
tapeCount = 0                       # tape count measured from color sensor
position = 0.0                      # calculated position, m
accelerationX = 0.0                 # forward acceleration of pod, m/s^2
accelerationY = 0.0					# sideways acceleration of pod, m/s^2
accelerationZ = 0.0					# vertical acceleration of pod, m/s^2
velocityX = 0.0                     # velocity in x direction, m/s
velocityY = 0.0                     # velocity in y direction, m/s
velocityZ = 0.0                     # velocity in z direction, m/s
roll = 0.0                          # pod roll, TODO insert measurement units
pitch = 0.0                         # pod pitch, TODO insert measurement units
yaw = 0.0                           # pod yaw, TODO insert measurement units
        # These require Health Check
amperage1 = 0.0                     # amperage reading 1, a
amperage2 = 0.0                     # amperage reading 2, a
voltage1 = 0.0                      # voltage reading 1, v
voltage2 = 0.0                      # voltage reading 2, v
temp_ambient = 0.0                  # ambient pod temperature, C
temp_battery1 = 0.0                 # battery temperature, C
temp_battery2 = 0.0                 # raspberry pi temperature, C

# Socket Communication
guiConnect = False

# Master Arduino Communication
masterBaud = 9600
masterUsbPort = '/dev/ttyACM0'
masterConnect = False

# TODO: setup vn connection code
# Vector Navigation 100 AHRS/IMU
vnConnect = False

# Struct
packer = struct.Struct('3I 15f')

# TODO: finish setting variables
# dependencies: sending data from Master
# function that reads information from master arduino and updates sensor variables
def readMaster():
    print("read master")

    # GUI value Testing Code
    global currentState
    global time
    global tapeCount
    global position
    global acceleration
    global amperage1
    global amperage2
    global voltage1
    global voltage2
    global pitch
    global roll
    global yaw
    global temp_ambient
    global temp_battery1
    global temp_battery2
    global velocityX
    global velocityY
    global velocityZ
    currentState = random.randint(0, 10)
    time = random.randint(0, 100)
    tapeCount = random.randint(0, 100)
    position = random.uniform(0.0, 100.0)
    acceleration = random.uniform(0.0, 100.0)
    amperage1 = random.uniform(0.0, 100.0)
    amperage2 = random.uniform(0.0, 100.0)
    voltage1 = random.uniform(0.0, 100.0)
    voltage2 = random.uniform(0.0, 100.0)
    pitch = random.uniform(0.0, 100.0)
    roll = random.uniform(0.0, 100.0)
    yaw = random.uniform(0.0, 100.0)
    temp_ambient = random.uniform(0.0, 100.0)
    temp_battery1 = random.uniform(0.0, 100.0)
    temp_battery2 = random.uniform(0.0, 100.0)
    velocityX = random.uniform(0.0, 100.0)
    velocityY = random.uniform(0.0, 100.0)
    velocityZ = random.uniform(0.0, 100.0)

    if(masterConnect == False):
		try:
			masterSerial = serial.serial(masterUsbPort, masterBaud)
			masterConnect = True
		except Exception as exc:
            print("Master connect failed. Exception raised: ")
			print(exc)
    else:
        print("Master connected...")
		serialData = masterSerial.readline()
		serialArray = serialData.strip().split(',')
		# set variables equal to the array indeces

# TODO: set guiInput variable from GUI
# function that reads information from GUI and updates guiInput variable
def readGUI():
    global guiConnect
    if(guiConnect == False):
        sock.send(b'0')
        retVal = sock.recv(1)
        retVal = retVal.decode('utf-8')
        if(retVal == '0'):
            guiConnect = True
        else:
            print('GUI connection could not be made')
    else:
        print('read GUI')
    global guiInput


# TODO: use vn100 to calculate velocity, acceleration and position
# this function does any computations to update the variables, like position and velocity
def compute():
	global accelerationX
	global accelerationY
	global accelerationZ
    global position
    global velocityX
    global velocityY
    global velocityZ
    print("compute")


#attempt to reconnect wireless network with TRANSITION_CHECK_COUNT number of attempts
def diagnostic():
    print("running diagnostic")
	if (guiConnect == False):
		for connectAttempt in range(TRANSITION_CHECK_COUNT):
			# DOLAN TODO: write code for reconnecting wifi in this loop
			# sock.connect() ? <--  idk something like that 

#turns off pi, (batteries?), do we want there to be no electricity?, do we have a switch for the batteries
#TODO: discuss with anthony and tyler what else needs to be shut down for the batteries
def powerOff():
    print("powering down...")

#checks if any of the sensor values are in critical ranges
def criticalSensorValueCheck():
    print("checking if sensor values are critical...")
    if (amperage1 > MAX_AMPERAGE or amperage2 > MAX_AMPERAGE or voltage1 > MAX_VOLTAGE or voltage2 > MAX_VOLTAGE or temp_ambient > MAX_TEMPERATURE_AMBIENT or temp_battery > MAX_TEMPERATURE_BATTERY or temp_battery2 > MAX_TEMPERATURE_PI):
        return True
    return False

#TODO: implement Pi's interrupt with I/O pins with anthony
#sends command to slave to engage brakes
def engageBrakes():
    print("engaging brakes...")

#TODO: serial.write brake command to master
#sends command to slave to retract brakes
def disengageBrakes():
    print ("disengaging brakes...")

#TODO: review function with state diagram
#function that controls the logic of the state changes
def stateChange():
    global currentState
    global proposedStateCount
    global proposedStateNumber

    print ("state change")
    # idle
    if (currentState == 0):
        # needs to get updated to accept 10 inputs sequentially
        if (guiInput == 1):
            print("Insert a command here to halt the system until the correct byte is sent from the GUI")
        elif (guiInput == 2):
            if (proposedStateCount > TRANSITION_CHECK_COUNT):
                diagnostic()
                currentState = 2
                proposedStateCount = 0
            else:
                if(proposedStateNumber != 2):
                    proposedStateNumber = 2
                    proposedStateCount = 1
                else:
                    proposedStateCount += 1

        elif (guiInput == 4 | (
                acceleration > ACCELERATION_THRESHOLD and velocityX > IN_MOTION_THRESHOLD) or criticalSensorValueCheck()):
            if (proposedStateCount > TRANSITION_CHECK_COUNT):
                currentState = 12
                proposedStateCount = 0
            else:
                if (proposedStateNumber != 12):
                    proposedStateNumber = 12
                    proposedStateCount = 1
                else:
                    proposedStateCount += 1
        elif (guiInput == 4 | (
                acceleration > DECELERATING_THRESHOLD and velocityX > IN_MOTION_THRESHOLD) or criticalSensorValueCheck()):
            if (proposedStateCount > TRANSITION_CHECK_COUNT):
                currentState = 11
                proposedStateCount = 0
            else:
                if (proposedStateNumber != 1):
                    proposedStateNumber = 11
                    proposedStateCount = 1
                else:
                    proposedStateCount += 1
        elif (guiInput == 3):
            if (proposedStateCount > TRANSITION_CHECK_COUNT):
                powerOff()
            else:
                if (proposedStateNumber != 7):
                    proposedStateNumber = 7
                    proposedStateCount = 1
                else:
                    proposedStateCount += 1
    # ready
    elif (currentState == 2):
        if (acceleration > ACCELERATION_THRESHOLD or velocityX > IN_MOTION_THRESHOLD or tapeCount > TAPE_COUNT_MOVING):
            if (proposedStateCount > TRANSITION_CHECK_COUNT):
                currentState = 3
                proposedStateCount = 0
            else:
                if (proposedStateNumber != 3):
                    proposedStateNumber = 3
                    proposedStateCount = 1
                else:
                    proposedStateCount += 1
        elif (guiInput == 4 | criticalSensorValueCheck()):
            if (proposedStateCount > TRANSITION_CHECK_COUNT):
                currentState = 12
                proposedStateCount = 0
            else:
                if (proposedStateNumber != 12):
                    proposedStateNumber = 12
                    proposedStateCount = 1
                else:
                    proposedStateCount += 1
    # Pushing
    elif (currentState == 3):
        if (acceleration < DECELERATING_THRESHOLD):
            if (proposedStateCount > TRANSITION_CHECK_COUNT):
                currentState = 4
                proposedStateCount = 0
            else:
                if (proposedStateNumber != 4):
                    proposedStateNumber = 4
                    proposedStateCount = 1
                else:
                    proposedStateCount += 1
        elif (guiInput == 4 | criticalSensorValueCheck()):
            if (proposedStateCount > TRANSITION_CHECK_COUNT):
                currentState = 12
                proposedStateCount = 0
            else:
                if (proposedStateNumber != 12):
                    proposedStateNumber = 12
                    proposedStateCount = 1
                else:
                    proposedStateCount += 1
    # Coasting
    elif (currentState == 4):
        if (time > MAX_TIME or tapeCount > MAX_TAPE_COUNT or position > MAX_DISTANCE):
            if (proposedStateCount > TRANSITION_CHECK_COUNT):
                currentState = 5
                proposedStateCount = 0
            else:
                if (proposedStateNumber != 5):
                    proposedStateNumber = 5
                    proposedStateCount = 1
                else:
                    proposedStateCount += 1
        elif (guiInput == 4 | criticalSensorValueCheck()):
            if (proposedStateCount > TRANSITION_CHECK_COUNT):
                currentState = 11
                proposedStateCount = 0
            else:
                if (proposedStateNumber != 11):
                    proposedStateNumber = 11
                    proposedStateCount = 1
                else:
                    proposedStateCount += 1
    # Braking
    elif (currentState == 5):
        if (guiInput == 5 and acceleration < STOPPED_ACCELERATION_HIGH or acceleration > STOPPED_ACCELERATION_LOW and velocityX < STOPPED_VELOCITY_LOW or velocityX > STOPPED_VELOCITY_LOW):
            if (proposedStateCount > TRANSITION_CHECK_COUNT):
                currentState = 6
                proposedStateCount = 0
            else:
                if (proposedStateNumber != 6):
                    proposedStateNumber = 5
                    proposedStateCount = 1
                else:
                    proposedStateCount += 1
        elif (guiInput == 4 | criticalSensorValueCheck()):
            if (proposedStateCount > TRANSITION_CHECK_COUNT):
                currentState = 11
                proposedStateCount = 0
            else:
                if (proposedStateNumber != 11):
                    proposedStateNumber = 11
                    proposedStateCount = 1
                else:
                    proposedStateCount += 1
        else:
            engageBrakes()
    # Disengage Brakes
    elif (currentState == 6):
            disengageBrakes()
            currentState = 0
            proposedStateCount = 0
    # Fault with Brakes
    elif (currentState == 11):
        if (acceleration > ACCELERATION_THRESHOLD):
            if (proposedStateCount > TRANSITION_CHECK_COUNT):
                currentState = 12
                proposedStateCount = 0
            else:
                if (proposedStateNumber != 12):
                    proposedStateNumber = 12
                    proposedStateCount = 1
                else:
                    proposedStateCount += 1
        elif (guiInput == 5):
            if (proposedStateCount > TRANSITION_CHECK_COUNT):
                currentState = 6
                proposedStateCount = 0
            else:
                if (proposedStateNumber != 6):
                    proposedStateNumber = 6
                    proposedStateCount = 1
                else:
                    proposedStateCount += 1
        else:
            engageBrakes()
    # Fault No Brakes
    elif (currentState == 12):
        if (acceleration < DECELERATING_THRESHOLD):
            if (proposedStateCount > TRANSITION_CHECK_COUNT):
                currentState = 11
                proposedStateCount = 0
            else:
                if (proposedStateNumber != 11):
                    proposedStateNumber = 11
                    proposedStateCount = 1
                else:
                    proposedStateCount += 1
        else:
            disengageBrakes()

# function that sends information back to GUI
def writeGUI():
    guiData = packer.pack(currentState, time, tapeCount, position, acceleration, velocityX, velocityY, velocityZ,
                          roll, pitch, yaw, amperage1,  amperage2,  voltage1,  voltage2,  temp_ambient,  temp_battery1,
                          temp_battery2)
    sock.send(guiData)

# main method, wizard that controls the various tasks
def main():
    while(True):
        readMaster()
        readGUI()
		compute()
        if(masterConnect == True):
            compute()
            stateChange()
        if(guiConnect == True):
            writeGUI()

# Run Main
main()
