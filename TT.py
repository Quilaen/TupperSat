def init():
	from TT import tempInit
	from TT import temp
	from TT import getExtTemp
	from TT import getIntTemp
	from log import log

def tempInit():
	open("/sys/bus/w1/devices/28-0417c2b877ff/w1_slave")
	open("/sys/bus/w1/devices/28-00000bc26d08/w1_slave")

def temp(location):
	fullstr = open( "/sys/bus/w1/devices/" + location + "/w1_slave", "r").readlines()
	pos = fullstr[1].find('t=')
	return float(fullstr[1][pos+2:])/1000.0
	print float(fullstr[1][pos+2:])/1000.0

def getExtTemp():
	temp('28-0417c2b877ff')

def getIntTemp():
	temp('28-00000bc26d08')
