def tempInit():
	open("/sys/bus/w1/devices/28-0417c2b877ff/w1_slave")
	open("/sys/bus/w1/devices/28-00000bc26d08/w1_slave")

def temp(location):
	f = open( "/sys/bus/w1/devices/"+location+"/w1_slave", "r").readlines()
	pos = f[1].find('t=')
	d = float(f[1][pos+2:])/1000.0
	print(d)
#	f.flush()
	return d

def getExtTemp():
	temp('28-0417c2b877ff')

def getIntTemp():
	temp('28-00000bc26d08')


import logging


def main():
    logging.basicConfig(filename = "/home/pi/logs/Log01", level=logging.INFO, format= '%(asctime)s %(levelname)s: %(message)s')

    # do some stuff
    while True:
          In = getIntTemp()
          Out = getExtTemp()
          logging.info('Ext Temp: %f', Out)
          logging.info('Int Temp: %f', In)
          print("Ext:Int Temperatures are: "+Out+ ":"+In)


if __name__=="__main__":
	main()
