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
TRANSITION_CHECK_COUNT = 10         # number of times a transition is requested before it actually transitions, histeresis

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
accelerationY = 0.0                 # sideways acceleration of pod, m/s^2
accelerationZ = 0.0                 # vertical acceleration of pod, m/s^2
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
sock = None
server_address = ('149.125.118.49', 10004) # Must be modified based on what network you are connected to
guiConnect = False

# Master Arduino Communication
masterBaud = 9600
masterUsbPort = '/dev/ttyAMC0'
masterConnect = False
masterSerial = None

# TODO: setup vn connection code
# Vector Navigation 100 AHRS/IMU
vnConnect = False

# Struct
packer = struct.Struct('1? 3I 17f')


# function that reads information from master arduino and updates sensor variables
def readMaster():
    print("read master")

    # GUI value Testing Code
    global currentState
    global time
    global tapeCount
    global position
    global accelerationX
    global accelerationY
    global accelerationZ
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
    accelerationX = random.uniform(0.0, 100.0)
    accelerationY = random.uniform(0.0, 100.0)
    accelerationZ = random.uniform(0.0, 100.0)
    amperage1 = random.uniform(0.0, 75.0)
    amperage2 = random.uniform(0.0, 75.0)
    voltage1 = random.uniform(0.0, 25.0)
    voltage2 = random.uniform(0.0, 25.0)
    pitch = random.uniform(0.0, 100.0)
    roll = random.uniform(0.0, 100.0)
    yaw = random.uniform(0.0, 100.0)
    temp_ambient = random.uniform(0.0, 100.0)
    temp_battery1 = random.uniform(0.0, 100.0)
    temp_battery2 = random.uniform(0.0, 100.0)
    velocityX = random.uniform(0.0, 100.0)
    velocityY = random.uniform(0.0, 100.0)
    velocityZ = random.uniform(0.0, 100.0)

    global masterConnect, masterSerial

    if (masterConnect == False):
        try:
            masterSerial = serial.Serial(masterUsbPort, masterBaud)
            masterConnect = True
        except Exception as exc:
            print("Master connect failed. Exception raised: ")
            print(exc)
    else:
        print("Master connected...")
        serialData = masterSerial.readline()
        serialArray = serialData.strip().split(',')
        # set variables equal to the array indeces


# function that reads information from GUI and updates guiInput variable
def readGUI():
    global guiConnect, guiInput, sock
    if guiConnect == False :
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect(server_address)
            sock.send(b'0')
            retVal = sock.recv(1)
            retVal = retVal.decode('utf-8')
            if retVal == '0' :
                guiConnect = True
            else:
                guiConnect = False
                print('Correct verification message not sent')
        except Exception as exc:
            guiConnect = False
            print('GUI connection failed. Exception raised: ')
            print(exc)
    else:
        try:
            command = sock.recv(1)
            command = command.decode('utf-8')
            guiInput = int(command)
            # print(guiInput)
        except Exception as exc:
                guiConnect = False
                sock.close()
                print('GUI connection has dropped. Exception raised: ')
                print(exc)


# this function does any computations to update the variables, like position and velocity
def compute():
    global position
    global velocityX
    global velocityY
    global velocityZ
    global accelerationX
    global accelerationY
    global accelerationZ
    print("compute")


#attempt to reconnect wireless network with TRANSITION_CHECK_COUNT number of attempts
def diagnostic():
    print("running diagnostic")
    if (guiConnect == False):
        print('not connected')
        # DOLAN TODO

#turns off pi
def powerOff():
    print("powering down...")

#checks if any of the sensor values are in critical ranges
def criticalSensorValueCheck():
    print("checking if sensor values are critical...")
    if (amperage1 > MAX_AMPERAGE or amperage2 > MAX_AMPERAGE or voltage1 > MAX_VOLTAGE or voltage2 > MAX_VOLTAGE or temp_ambient > MAX_TEMPERATURE_AMBIENT or temp_battery1 > MAX_TEMPERATURE_BATTERY or temp_battery2 > MAX_TEMPERATURE_PI):
        return True
    return False

#sends command to slave to engage brakes
def engageBrakes():
    print("engaging brakes...")

#sends command to slave to retract brakes
def disengageBrakes():
    print ("disengaging brakes...")

#function that controls the logic of the state changes
def stateChange():
    global currentState
    global proposedStateCount
    global proposedStateNumber
    global guiInput

    print ("state change")
    # idle
    if (currentState == 0):
        # needs to get updated to accept 10 inputs sequentially
        if (guiInput == 1):
            while(guiInput != '1'):
                readGUI()
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

        elif (guiInput == 4 or (
                accelerationX > ACCELERATION_THRESHOLD and velocityX > IN_MOTION_THRESHOLD) or criticalSensorValueCheck()):
            if (proposedStateCount > TRANSITION_CHECK_COUNT):
                currentState = 12
                proposedStateCount = 0
            else:
                if (proposedStateNumber != 12):
                    proposedStateNumber = 12
                    proposedStateCount = 1
                else:
                    proposedStateCount += 1
        elif (guiInput == 4 or (
                accelerationX > DECELERATING_THRESHOLD and velocityX > IN_MOTION_THRESHOLD) or criticalSensorValueCheck()):
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
        if (accelerationX > ACCELERATION_THRESHOLD or velocityX > IN_MOTION_THRESHOLD or tapeCount > TAPE_COUNT_MOVING):
            if (proposedStateCount > TRANSITION_CHECK_COUNT):
                currentState = 3
                proposedStateCount = 0
            else:
                if (proposedStateNumber != 3):
                    proposedStateNumber = 3
                    proposedStateCount = 1
                else:
                    proposedStateCount += 1
        elif (guiInput == 4 or criticalSensorValueCheck()):
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
        if (accelerationX < DECELERATING_THRESHOLD):
            if (proposedStateCount > TRANSITION_CHECK_COUNT):
                currentState = 4
                proposedStateCount = 0
            else:
                if (proposedStateNumber != 4):
                    proposedStateNumber = 4
                    proposedStateCount = 1
                else:
                    proposedStateCount += 1
        elif (guiInput == 4 or criticalSensorValueCheck()):
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
        elif (guiInput == 4 or criticalSensorValueCheck()):
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
        if (guiInput == 5 and accelerationX < STOPPED_ACCELERATION_HIGH or accelerationX > STOPPED_ACCELERATION_LOW and velocityX < STOPPED_VELOCITY_LOW or velocityX > STOPPED_VELOCITY_LOW):
            if (proposedStateCount > TRANSITION_CHECK_COUNT):
                currentState = 6
                proposedStateCount = 0
            else:
                if (proposedStateNumber != 6):
                    proposedStateNumber = 5
                    proposedStateCount = 1
                else:
                    proposedStateCount += 1
        elif (guiInput == 4 or criticalSensorValueCheck()):
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
        if (accelerationX > ACCELERATION_THRESHOLD):
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
        if (accelerationX < DECELERATING_THRESHOLD):
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
    global sock, guiConnect
    guiData = packer.pack(masterConnect, currentState, time, tapeCount, position, accelerationX, accelerationY, accelerationZ, velocityX, velocityY, velocityZ,
                          roll, pitch, yaw, amperage1,  amperage2,  voltage1,  voltage2,  temp_ambient,  temp_battery1,
                          temp_battery2)
    try:
        sock.send(guiData)
    except Exception as exc:
        print('Failed to send data to GUI. Exception raised: ')
        guiConnect = False
        sock.close()
        print(exc)

def writeMaster():
    print('write acceleration data to master')

# main method, wizard that controls the various tasks
def main():
    while(True):
        readMaster()
        readGUI()
        compute()
        if(masterConnect == True):
            writeMaster()
            compute()
            stateChange()
        if(guiConnect == True):
            writeGUI()

# Run Main
main()
