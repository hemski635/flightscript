#!/bin/python3


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
	f = open(logName, "a")
	currentTime = getTime()
	f.write(currentTime + "," + action + " \n")
	f.close()



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
	BMPAltitude = "BMP Altitude," + str(total/averageFromBMP)
	return total/averageFromBMP

groundAltitude = getGroundAltitude()

def getBMPAltitude():
	total = float(0)
	for i in range(1, averageFromBMP):
		i = sensor.read_altitude()
		total = total + i
	BMPAltitude = "BMP Altitude," + str(total/averageFromBMP-groundAltitude)
	writeLog(BMPAltitude, BMPLog)
	return total/averageFromBMP-groundAltitude



#On ground
lockParachute()
while True:
    currentAltitude = getBMPAltitude()
    if (currentAltitude - groundAltitude) > 5:
        writeLog("Launched!", LaunchLog)
        break
    #REMEMBER TO REMOVE THIS OUT
#    elif input('launch yet?') == 'y':
#        writeLog("Launch!", LaunchLog)
#        break
    else:
        continue


while True:
    currentAltitude = getBMPAltitude()
    highestAltitude = float(0)
    writing = "Altitude: " + currentAltitude
    writeLog(writing, BMPLog)
    if currentAltitude > highestAltitude:
        highestAltitude = currentAltitude
        continue
    else:
        writing = "Apogee at " + str(highestAltitude)
        writeLog(writing, LaunchLog)
        writeLog("Attempting to launch parachute", LaunchLog)
        parachuteLaunch()
        break


#Decending
while True:
    currentAltitude = getBMPAltitude()
    writing = "Altitude: " + currentAltitude
    writeLog(writing, BMPLog)
    if (groundAltitude + 3) > currentAltitude > (groundAltitude - 3):
        writeLog("Another happy landing!  - Obi-Wan Kenobi, The Revenge of the Sith", LaunchLog)
        break
    else:
        continue


timenow = time.strftime("%d%m%Y_%H%M", time.gmtime())
BMPLogName = 'BMP_' + timenow + '.log'
rename(BMPLog, BMPLogName)
LaunchLogName = 'launch_' + timenow + '.log'
rename(LaunchLog, LaunchLogName)
