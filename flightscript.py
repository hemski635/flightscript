#!/bin/python3






#
#
#
#
# REMEMBER TO COMMENT OUT ELIF STATEMENT ON ROW 108 BEFORE REAL TESTS
#
#
#
#



import Adafruit_BMP.BMP085 as BMP085
from gpiozero import Servo
import time
from os import rename

#define variables and stuff
servo = Servo(17)
sensor = BMP085.BMP085()
averageFromBMP = 5 #Number of iterations for averaging altitude
BMPLog = 'BMP.log'
LaunchLog = 'launch.log'


def getTime():
	time_in_ms = int(round(time.time() * 1000))
	timeGetted = time.strftime('%Y-%m-%d %H:%M:%S:{}'.format(time_in_ms%1000), time.gmtime(time_in_ms/1000.0))
	return timeGetted


def writeLog(action, logName):
	logfile = open(logName, "a")
	currentTime = getTime()
	logfile.write(currentTime + "," + action + " \n")
	logfile.close()



def parachuteLaunch():
	servo.min()
	writeLog("Parachute launched!", LaunchLog)
	return True


def lockParachute():
	servo.max()
	return True

def getGroundAltitude():
	total = float(0)
	for i in range(1, averageFromBMP):
		i = sensor.read_altitude()
		total = total + i
	return total/averageFromBMP

groundAltitude = getGroundAltitude()

def getBMPAltitude():
	total = float(0)
	for i in range(1, averageFromBMP):
		i = sensor.read_altitude()
		total = total + i
	BMPAltitude = "BMP Altitude " + str(total/averageFromBMP-groundAltitude)
	writeLog(BMPAltitude, LaunchLog)
	return total/averageFromBMP-groundAltitude

def ifWithin(testarray, tolerance, referenceNumber):
    okTest = 0
    for i in testarray:
        if (i + tolerance) > referenceNumber > (i - tolerance):
            okTest += 1
    if okTest == len(testarray):
        return True
    else:
        return False

def ifBackOnGround(tolerance, numberCount):
    testArray = []
    testAltitude = getBMPAltitude()
    time.sleep(1)
    testArray.append(testAltitude)
    while True:
        testAltitude = getBMPAltitude()
        test = ifWithin(testArray, tolerance, testAltitude)
        if test == True:
            testArray.append(testAltitude)
            if len(testArray) >= numberCount:
                break
        time.sleep(1)
    return True


#On ground
launchAltitude = float(0)
lockParachute()
while True:
    currentAltitude = getBMPAltitude()
    if (currentAltitude - launchAltitude) > 5:
        writeLog("Launched!", LaunchLog)
        break
    #REMEMBER TO REMOVE THIS OUT
    elif input('launch yet?') == 'y':
        writeLog("Launch!", LaunchLog)
        break
    else:
        continue

#Wait for apogee/parachute
highestAltitude = float(0)
while True:
    currentAltitude = getBMPAltitude()
    if currentAltitude > highestAltitude:
        highestAltitude = currentAltitude
        continue
    else:
        writing = "Apogee at " + str(highestAltitude)
        writeLog(writing, LaunchLog)
        writing = "Attempting to launch parachute"
        writeLog(writing, LaunchLog)
        parachuteLaunch()
        break


#Decending
if (ifBackOnGround(3, 5)):
    writing = "Landing detected, exiting"
    writeLog(writing, LaunchLog)


timenow = time.strftime("%Y%m%d_%H%M", time.gmtime())
BMPLogName = 'logs/BMP_' + timenow + '.log'
rename(BMPLog, BMPLogName)
LaunchLogName = 'logs/launch_' + timenow + '.log'
rename(LaunchLog, LaunchLogName)
