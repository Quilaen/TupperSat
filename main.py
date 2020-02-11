import logging
# import smbus
import time
# import serial


class sensor:
    def __init__(self, ext, int, gps, pressure):
        logging.basicConfig(filename="Test", level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
        # setting up the logging session
        self.ext = ext  # setting the toggle for recording external temp
        self.extn = "/sys/bus/w1/devices/28-0417c2b877ff/w1_slave",  # setting the location of the external temp device
#        self.ext.type2 = open("/sys/bus/w1/devices/28-0417c2b877ff/w1_slave", "r")  # opening the external temp file
        self.int = int  # setting the toggle for recording internal temp
        self.intn = "/sys/bus/w1/devices/28-00000bc26d08/w1_slave",  # setting the location of the internal temp device
#        self.int.type2 = open("/sys/bus/w1/devices/28-00000bc26d08/w1_slave", "r")  # opening the internal tmep file
        self.gps = gps  # setting the toggle for recording GPS
#        self.gpsn = serial.Serial('COM5', 9600) #setting location of the GPS module
        self.pressure = pressure  # setting the toggle for recording pressure/temp
#        self.pressuren = "0x77" #setting location of the pressure module
        if self.ext:  # if reading external temp
            logging.info("Logging External Temperature.")  # make a record of it
        else:  # otherwise
            logging.info("Not Logging External Temperature.")  # make a record of it
        if self.int:  # if reading internal temp
            logging.info("Logging Internal Temperature.")  # make a record of it
        else:  # otherwise
            logging.info("Not Logging Internal Temperature.")  # make a record of it
        if self.gps:  # if reading GPS
            logging.info("Logging GPS.")  # make a record of it
        else:  # otherwise
            logging.info("Not Logging GPS.")  # make a record of it
        if self.pressure:  # if reading pressure
            logging.info("Logging Pressure.")  # make a record of it
        else:  # otherwise
            logging.info("Not Logging Pressure.")  # make a record of it

    def measure(self):
        while True:
            try:
                # radioFunction("preamble|"+self.extTemp()+"|"+self.intTemp()+"|"+self.GPS()+"|"+self.pres())
                # when radioFunction() is working, the below can be commented out, as the logging should happen as
                # the radioFunction() calls the functions
                self.extTemp()  # call external temperature & log it
                self.intTemp()  # call internal temperature & log it
                self.GPS()  # call GPS data & log it
                self.pres()  # call pressure data & log it
                time.sleep(2.0)  # waits for 2 seconds to run again
            except KeyboardInterrupt:  # allows for the system to be interrupted
                break  # ends the repeat by breaking out of the code

    def extTemp(self):
        if self.ext:  # checking if we want to read the external
            extM = read(self.extn, "r").readlines()  # reading the lines
            extP = extM[1].find('t=')  # locating the temperature
            ext = float(extM[1][extP+2:])/1000.0  # converting the temperature
            logging.info('Ext Temp: %f', ext)  # logging the data
            return ext  # returns the temperature for use in the radioFunction()

    def intTemp(self):
        if self.int:  # checking if we want to read the internal temp
            intM = read(self.intn, "r").readlines()  # reading the lines
            intP = intM[1].find('t=')  # locating the temperature
            int = float(intM[1][intP+2:])/1000.0  # converting the temperature
            logging.info('Int Temp: %f', int)  # logging the data
            return int  # returns the temperature for use in the radioFunction()

    def GPS(self):
        if self.GPS:  # checking if we want to read he GPS
            sentence = self.gpsn.readline().decode('utf8')  # reading the gps data & decoding
            sentenceid = sentence[3:6]  # parsing out the prefix
            if sentenceid == 'GLL':  # if it is the GPS data we want
                GPSData = sentence.split(",")  # split the sentence to allow the use of the data
                gps = (GPSData[1] + GPSData[2] + ', ' + GPSData[3] + GPSData[4])  # combine the data
                logging.info('GPS Data: %W', gps)  # log the data
                return gps  # returns the GPS data -- this may be better using GPSData variable depending
                            # on the requirements of the radio

    def pres(self):
        if self.pressure:  # checking if we want to read the pressure systems
            bus = smbus.SMBus(1)  # setting which bus to read
            addr = self.pressuren  # setting the i2c address
            bus.write_byte(addr, 0x58)  # writing a new bite to the bus
            time.sleep(0.05)  # pause to allow completion of previous step
            tempadcbytes = bus.read_i2c_block_data(addr, 0x00)  # temperature ADC bytes
            time.sleep(0.05)  # pause to allow completion of previous step
            tempadc = tempadcbytes[0] * 65536.0 + tempadcbytes[1] * 256.0 + tempadcbytes[2]  # temp reading convert
            bus.write_byte(addr, 0x48)  # writing a new bite to the bus
            time.sleep(0.05)  # pause to allow completion of previous step
            presadcbytes = bus.read_i2c_block_data(addr, 0x00)  # pressure ADC bytes
            time.sleep(0.05)  # pause to allow completion of previous step
            presadc = (presadcbytes[0] << 16)+(presadcbytes[1] << 8)+(presadcbytes[2])  # pressure reading convert
            logging.info('Pressure: %f', presadc)  # logging the pressure
            logging.info('Temp (P): %f', tempadc)  # logging the temperature
            return presadc, tempadc  # returning the pressure and temp data for the radioFunction() to use


if __name__ == "__main__":  # runs the below only when testing
    Sensor = sensor(True, False, False, False)  # sets the external reading, and none of the others.
