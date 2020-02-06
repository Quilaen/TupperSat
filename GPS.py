import serial
import time

gpsCheck = True
gpsData = []

def parseGLL(prompt):
    keyData = prompt.split(",")
    return keyData

print(parseGLL("GLL,oct,1234,7,10202,w,n,wwrgqe3rhgw"))


def gpsFunction(delay):
    gps = serial.Serial('/dev/ttyACM0', 9600)
    global gpsCheck
    global GPSData
    while gpsCheck:
        sentence = gps.readline().decode('utf8')
        sentenceid = sentence[3:6]
        if sentenceid == 'GLL':
            GPSData = parseGLL(sentence)
        time.sleep(delay)
