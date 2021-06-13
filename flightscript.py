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
GPSLog = 'GPS.log'
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

while True:
    currentAltitude1 = getBMPAltitude()
    time.sleep(0.5)
    currentAltitude2 = getBMPAltitude()
    if (currentAltitude2 - currentAltitude1) > 3:
        writeLog("Launch!", LaunchLog)
        break
    #REMEMBER TO REMOVE THIS OUT
    elif input('launch yet?') == 'y':
        writeLog("Launch!", LaunchLog)
        break
    else:
        continue


#Wait for apogee and parachute
while True:
    currentAltitude1 = getBMPAltitude()
    time.sleep(0.3)
    currentAltitude2 = getBMPAltitude()
    if not(currentAltitude2 - currentAltitude1) > 1:
        writing = "Apogee at " + str(currentAltitude2)
        writeLog(writing, LaunchLog)
        writeLog("Attempting to launch parachute", LaunchLog)
        parachuteLaunch()
        break
    else:
        continue


#Decending
while True:
    currentAltitude1 = getBMPAltitude()
    time.sleep(0.3)
    currentAltitude2 = getBMPAltitude()    
    if currentAltitude2 - currentAltitude1 < 1:
        writeLog("Another happy landing!  - Obi-Wan Kenobi, The Revenge of the Sith", LaunchLog)
        break
    else:
        continue

timenow = time.strftime("%d%m%Y_%H%M", time.gmtime())
BMPLogName = 'BMP_' + timenow + '.log'
rename(BMPLog, BMPLogName)
LaunchLogName = 'launch_' + timenow + '.log'
rename(LaunchLog, LaunchLogName)
