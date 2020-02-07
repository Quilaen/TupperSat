import time

def TemperatureSetup():
	f_in = open('/sys/bus/w1/devices/28-00000bc26d08/w1_slave', 'r')
	f_out = open('/sys/bus/w1/devices/28-0417c2b877ff/w1_slave', 'r')
	lines_in = f_in.readlines()
	lines_out = f_out.readlines()
	equals_pos_in = lines_in[1].find('t=')
	equals_pos_out = lines_out[1].find('t=')
	temp_string_in = lines_in[1][equals_pos_in+2:]
	temp_string_out = lines_out[1][equals_pos_out+2:]
	temp_c_in = float(temp_string_in)/1000.0
	temp_c_out = float(temp_string_out)/1000.0
	return  temp_c_in, temp_c_out


def Temperature():
	repeat = True
	while repeat:
		print('Temp Inside (C): ', TemperatureSetup()[0], '\nTemp Outside (C): ', TemperatureSetup()[1])
		time.sleep(int('2'))
