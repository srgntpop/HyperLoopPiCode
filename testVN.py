from vnpy import *

import time as time


# from scipy import *



# def medianFilter(array):

# array = sorted array(array)

# return array(25)



def medianFilter(arrayIn):
    # sorted: worst case O(nlogn)

    median = 0.0

    sortedArrayIn = sorted(arrayIn)
    if (len(sortedArrayIn) % 2 == 1):

        median = sortedArrayIn[(len(sortedArrayIn) - 1) / 2]

    else:

        median = sortedArrayIn[len(sortedArrayIn) / 2]

    return median


def meanFilter(arrayIn):
    count = 0

    sum = 0.0

    for i in range(len(arrayIn) / 2):
        sum += arrayIn[i] + arrayIn[len(arrayIn) - i - 1]

        count += 1

    if (len(arrayIn) % 2 == 1):
        sum += arrayIn[(len(arrayIn) - 1) / 2]

    mean = sum / float(count)

    return mean


def main():
    s = VnSensor()

    s.connect('/dev/ttyUSB0', 115200)

    reg = s.read_yaw_pitch_roll_magnetic_acceleration_and_angular_rates()

    velocityX = 0.0
    position = 0.0
    deltaV = 0.0
    acceleration = 0.0
    deltaT = 0.0
    startTime = time.time()

    timesRead = 1

    while True:

        timePassed = time.time() - startTime
        deltaT = timePassed/timesRead
        if (timePassed < 5.0):
            timesRead+=1
            acceleration = reg.accel.x
            velocityX = velocityX + acceleration*deltaT
            position = velocityX*deltaT + (acceleration/2)*(deltaT*deltaT)
        else:
            break
        if (timePassed % 1 == 0):
            print(reg.accel.x, velocityX, position)



    print("time per loop: ")

    print(timePassed / timesRead)


main()
