# List of States
# 0  Idle                |   2   Ready               |   3   Pushing     |
# 4  Coasting            |   5   Braking         |   6   Disengage Brakes
# 11  Fault Brakes      | 12 Fault No Brakes     |

# List of Inputs
# 0 None | 1 Insert Pod |   2   Start | 3   Power Off | 4   Engage Brakes | 5 Disengage Brakes

# Constants
ACCELERATION_THRESHOLD = .5
DECCELERATING_THRESHOLD = 0
IN_MOTION_THRESHOLD = 2
MAX_AMPERAGE = 10
MAX_DISTANCE = 3000
MAX_TAPE_COUNT = 50
MAX_TEMPERATURE_AMBIENT = 60
MAX_TEMPERATURE_BATTERY = 50
MAX_TEMPERATURE_PI = 60
MAX_TIME = 1000
MAX_VOLTAGE = 12
MIN_AMPERAGE = 0
MIN_VOLTAGE = 0
STOPPED_ACCELERATION_HIGH = 0.8
STOPPED_ACCELERATION_LOW = 0
STOPPED_VELOCITY_HIGH = 2
STOPPED_VELOCITY_LOW = 0
TAPE_COUNT_MOVING = 3
TRANSITION_CHECK_COUNT = 10

# sensor variables
acceleration = 0.0
amperage1 = 0.0
amperage2 = 0.0
currentState = 0
guiInput = 0
mode = 0  # mode is the state that SpaceX has designated in the safety manual
pitch = 0.0
position = 0.0
proposedStateNumber = 0
proposedStateCount = 0
roll = 0.0
tapeCount = 0
temp_ambient = 0.0
temp_battery = 0.0
temp_pi = 0.0
time = 0
velocityX = 0.0
velocityY = 0.0
velocityZ = 0.0
voltage1 = 0.0
voltage2 = 0.0
yaw = 0.0


def readMaster():
    print("read masta")


def readGUI():
    print("read GUI")


def compute():
    print("compute")


def diagnostic():
    print("running diagnostic")


def powerOff():
    print("powering down...")


def criticalSensorValueCheck():
    print("checking if sensor values are critical...")
    if (amperage1 > MAX_AMPERAGE | amperage2 > MAX_AMPERAGE | voltage1 > MAX_VOLTAGE | voltage2 > MAX_VOLTAGE | temp_ambient > MAX_TEMPERATURE_AMBIENT | temp_battery > MAX_TEMPERATURE_BATTERY | temp_pi > MAX_TEMPERATURE_PI):
        return True
    return False


def engageBrakes():
    print("engaging brakes...")


def disengageBrakes():
    print ("disengaging brakes...")


def stateChange():
    global currentState
    global proposedStateCount
    global proposedStateNumber
    print ("state change")
    # idle
    if (currentState == 0):
        # needs to get updated to accept 10 inputs sequentially
        if (guiInput == 1):
            while (guiInput == 1):
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

        elif (guiInput == 4 | (
                acceleration > ACCELERATION_THRESHOLD & velocityX > IN_MOTION_THRESHOLD) | criticalSensorValueCheck()):
            if (proposedStateCount > TRANSITION_CHECK_COUNT):
                currentState = 12
                proposedStateCount = 0
            else:
                proposedStateCount += 1
        elif (guiInput == 4 | (
                acceleration > DECCELERATING_THRESHOLD & velocityX > IN_MOTION_THRESHOLD) | criticalSensorValueCheck()):
            if (proposedStateCount > TRANSITION_CHECK_COUNT):
                currentState = 11
                proposedStateCount = 0
            else:
                proposedStateCount += 1
        elif (guiInput == 3):
            if (proposedStateCount > TRANSITION_CHECK_COUNT):
                powerOff()
            else:
                proposedStateCount += 1
    # ready
    elif (currentState == 2):
        if (acceleration > ACCELERATION_THRESHOLD | velocityX > IN_MOTION_THRESHOLD | tapeCount > TAPE_COUNT_MOVING):
            if (proposedStateCount > TRANSITION_CHECK_COUNT):
                currentState = 3
                proposedStateCount = 0
            else:
                proposedStateCount += 1
        elif (guiInput == 4 | criticalSensorValueCheck()):
            if (proposedStateCount > TRANSITION_CHECK_COUNT):
                currentState = 12
                proposedStateCount = 0
            else:
                proposedStateCount += 1
    # Pushing
    elif (currentState == 3):
        if (acceleration < DECCELERATING_THRESHOLD):
            if (proposedStateCount > TRANSITION_CHECK_COUNT):
                currentState = 4
                proposedStateCount = 0
            else:
                proposedStateCount += 1
        elif (guiInput == 4 | criticalSensorValueCheck()):
            if (proposedStateCount > TRANSITION_CHECK_COUNT):
                currentState = 12
                proposedStateCount = 0
            else:
                proposedStateCount += 1
    # Coasting
    elif (currentState == 4):
        if (time > MAX_TIME | tapeCount > MAX_TAPE_COUNT | position > MAX_DISTANCE):
            if (proposedStateCount > TRANSITION_CHECK_COUNT):
                currentState = 5
                proposedStateCount = 0
            else:
                proposedStateCount += 1
        elif (guiInput == 4 | criticalSensorValueCheck()):
            if (proposedStateCount > TRANSITION_CHECK_COUNT):
                currentState = 11
                proposedStateCount = 0
            else:
                proposedStateCount += 1
    # Braking
    elif (currentState == 5):
        if (guiInput == 5 & acceleration < STOPPED_ACCELERATION_HIGH & acceleration > STOPPED_ACCELERATION_LOW & velocityX < STOPPED_VELOCITY_LOW & velocityX > STOPPED_VELOCITY_LOW):
            if (proposedStateCount > TRANSITION_CHECK_COUNT):
                currentState = 6
                proposedStateCount = 0
            else:
                proposedStateCount += 1
        elif (guiInput == 4 | criticalSensorValueCheck()):
            currentState = 11
            proposedStateCount = 0
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
            currentState = 12
            proposedStateCount = 0
        elif (guiInput == 5):
            currentState = 6
            proposedStateCount = 0
        else:
            engageBrakes()
    # Fault No Brakes
    elif (currentState == 12):
        if (acceleration < DECCELERATING_THRESHOLD):
            currentState = 11
            proposedStateCount = 0
        else:
            disengageBrakes()


def main():
    readMaster()
    readGUI()
    compute()
    stateChange()


main()
