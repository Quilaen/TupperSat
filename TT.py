import time

def Temp():
	t1 = "/sys/bus/w1/devices/28-00000bc26d08/w1_slave"
	fullstr1 =  open(t1, "r").readlines()
	pos1 = fullstr1[1].find('t=')
	return float(fullstr1[1][pos1+2:])/1000.0


