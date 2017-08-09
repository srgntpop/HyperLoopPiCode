#Kevin Tarczali     9 August 2017
#pi_control_software.py     version 2

# List of States
# 0  Idle       |   2   Ready           |   3   Pushing          |
# 4  Coasting   |   5   Braking         |   6   Disengage Brakes |
#7 Power Off    |   11  Fault Brakes    | 12 Fault No Brakes     |

# List of Inputs
# 0 None | 1 Insert Pod |   2   Start | 3   Power Off | 4   Engage Brakes | 5 Disengage Brakes

# Constants
ACCELERATION_THRESHOLD = .5         #threshold at which pod can be determined to be accelerating, m/s^2
DECCELERATING_THRESHOLD = 0         #threshold at which pod can be determined to be deccelerating, m/s^2
IN_MOTION_THRESHOLD = 2             #threshold at which pod can be determined to be in motion, m/s
MAX_AMPERAGE = 10                   #maximum safe amperage, w
MAX_DISTANCE = 3000                 #maximum distance pod can travel before brakes engage automatically, m
MAX_TAPE_COUNT = 50                 #maximum tape reads that can be read before brakes engage automatically, #
MAX_TEMPERATURE_AMBIENT = 60        #maximum safe ambient tempererature reading in the pod, C
MAX_TEMPERATURE_BATTERY = 50        #maximum safe temperature of battery, C
MAX_TEMPERATURE_PI = 60             #maximum safe temperature of pi, C
MAX_TIME = 1000                     #maximum time pod is coasting before brakes engage automatically, s
MAX_VOLTAGE = 12                    #maximum safe voltage, v
MIN_AMPERAGE = 0                    #minimum safe amperage, w
MIN_VOLTAGE = 0                     #minimum safe voltage, v
STOPPED_ACCELERATION_HIGH = 0.8     #high-end for acceleration reading when pod is stopped, m/s^2
STOPPED_ACCELERATION_LOW = 0        #low-end for aceleration reading when pod is stopped, m/s^2
STOPPED_VELOCITY_HIGH = 2           #high-end for velocity reading when pod is stopped, m/s
STOPPED_VELOCITY_LOW = 0            #low-end for velocity reading when pod is stopped, m/s
TAPE_COUNT_MOVING = 3               #tape count that indicates pod is moving
TRANSITION_CHECK_COUNT = 10         #number of times a transition is requested before it actually transitions, historasis

# sensor variables
acceleration = 0.0                  #forward acceleration of pod, m/s^2
amperage1 = 0.0                     #amperage reading 1, w
amperage2 = 0.0                     #amperage reading 2, w
currentState = 0                    #current state of software
guiInput = 0                        #command sent from GUI
mode = 0                            #state that SpaceX has designated in the safety manual
pitch = 0.0                         #pod pitch, TODO insert measurement units
position = 0.0                      #calculated position, m
proposedStateNumber = 0             #number corresponding to state that software wishes to change to
proposedStateCount = 0              #number of times state change has been proposed
roll = 0.0                          #pod roll, TODO insert measurement units
tapeCount = 0                       #tape count measured from color sensor
temp_ambient = 0.0                  #ambient pod temperature, C
temp_battery = 0.0                  #battery temperature, C
temp_pi = 0.0                       #raspberry pi temperature, C
time = 0                            #time counter for coasting, s
velocityX = 0.0                     #velocity in x direction, m/s
velocityY = 0.0                     #velocity in y direction, m/s
velocityZ = 0.0                     #velocity in z direction, m/s
voltage1 = 0.0                      #voltage reading 1, v
voltage2 = 0.0                      #voltage reading 2, v
yaw = 0.0                           #pod yaw, TODO insert measurement units

#function that reads information from master arduino and updates sensor variables
def readMaster():
    global acceleration
    global yaw
    global pitch
    global roll
    global tapeCount
    global amperage1
    global amperage2
    global voltage1
    global voltage2
    global temp_pi
    global temp_battery
    global temp_ambient
    print("read masta")

#function that reads information from GUI and updates guiInput variable
def readGUI():
    global guiInput
    print("read GUI")

#this function does any computations to update the variables, like position and velocity
def compute():
    global position
    global velocityX
    global velocityY
    global velocityZ
    print("compute")


#attempt to reconnect wireless network with TRANSITION_CHECK_COUNT number of attempts
def diagnostic():
    print("running diagnostic")

#turns off pi
def powerOff():
    print("powering down...")

#checks if any of the sensor values are in critical ranges
def criticalSensorValueCheck():
    print("checking if sensor values are critical...")
    if (amperage1 > MAX_AMPERAGE | amperage2 > MAX_AMPERAGE | voltage1 > MAX_VOLTAGE | voltage2 > MAX_VOLTAGE | temp_ambient > MAX_TEMPERATURE_AMBIENT | temp_battery > MAX_TEMPERATURE_BATTERY | temp_pi > MAX_TEMPERATURE_PI):
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
                acceleration > ACCELERATION_THRESHOLD & velocityX > IN_MOTION_THRESHOLD) | criticalSensorValueCheck()):
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
                acceleration > DECCELERATING_THRESHOLD & velocityX > IN_MOTION_THRESHOLD) | criticalSensorValueCheck()):
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
        if (acceleration > ACCELERATION_THRESHOLD | velocityX > IN_MOTION_THRESHOLD | tapeCount > TAPE_COUNT_MOVING):
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
        if (acceleration < DECCELERATING_THRESHOLD):
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
        if (time > MAX_TIME | tapeCount > MAX_TAPE_COUNT | position > MAX_DISTANCE):
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
        if (guiInput == 5 & acceleration < STOPPED_ACCELERATION_HIGH & acceleration > STOPPED_ACCELERATION_LOW & velocityX < STOPPED_VELOCITY_LOW & velocityX > STOPPED_VELOCITY_LOW):
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
        if (acceleration < DECCELERATING_THRESHOLD):
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

#function that sends information back to GUI
def writeGUI():
    print ("write information back to GUI")

#main method, wizard that controlls the various tasks
def main():
    while(True):
        readMaster()
        readGUI()
        compute()
        stateChange()
        writeGUI()

#run main dude
main()
