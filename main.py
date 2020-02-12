import logging
import smbus
import time
import serial


class sensor:
    def __init__(self, ext, int, gps, pressure):
        logging.basicConfig(filename="DryRun01", level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
        # setting up the logging session
        self.ext = ext  # setting the toggle for recording external temp
        self.extn = "/sys/bus/w1/devices/28-0417c2b877ff/w1_slave",  # setting the location of the external temp device
        self.exto = open("/sys/bus/w1/devices/28-0417c2b877ff/w1_slave", "r")  # opening the external temp file
        self.int = int  # setting the toggle for recording internal temp
        self.intn = "/sys/bus/w1/devices/28-00000bc26d08/w1_slave",  # setting the location of the internal temp device
        self.into = open("/sys/bus/w1/devices/28-00000bc26d08/w1_slave", "r")  # opening the internal tmep file
        self.gps = gps  # setting the toggle for recording GPS
        self.gpsn = serial.Serial('/dev/ttyACM0', 9600) #setting location of the GPS module
        self.pressure = pressure  # setting the toggle for recording pressure/temp
        self.pressuren = 0x77 #setting location of the pressure module
        self.bus = smbus.SMBus(1)  # setting which bus to read
        self.addr = self.pressuren  # setting the i2c address
#        self.bus = smbus.SMBus(1)
#        self.address = 0x77
        self.C1bytes = self.bus.read_i2c_block_data(self.addr, 0xA2)
        self.C1 = (self.C1bytes[0] << 8) + self.C1bytes[1]
        self.C2bytes = self.bus.read_i2c_block_data(self.addr, 0xA4)
        self.C2 = (self.C2bytes[0] << 8) + self.C2bytes[1]
        self.C3bytes = self.bus.read_i2c_block_data(self.addr, 0xA6)
        self.C3 = (self.C3bytes[0] << 8) + self.C3bytes[1]
        self.C4bytes = self.bus.read_i2c_block_data(self.addr, 0xA8)
        self.C4 = (self.C4bytes[0] << 8) + self.C4bytes[1]
        self.C5bytes = self.bus.read_i2c_block_data(self.addr, 0xAA)
        self.C5 = (self.C5bytes[0] << 8) + self.C5bytes[1]
        self.C6bytes = self.bus.read_i2c_block_data(self.addr, 0xAC)
        self.C6 = (self.C6bytes[0] << 8) + self.C6bytes[1]
        self.D1 = 0
        self.D2 = 0
        self.TEMP = 0.0  # Calculated temperature
        self.PRES = 0.0  # Calculated Pressure
        self.dT = 0
        self.OFF = 0
        self.SENS = 0
        self.P = 0
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
                # myradio.send_telemetry(datetime.datetime.now(), GPS(), intTemp(), extTemp(), pres() )
                # GPS() gives lattitude, longitude, horizontal dilution, altitude
                # intTemp() gives the internal temperature
                # extTemp() gives the external temperature
                # pres() gives the pressure
                # when radioFunction() is working, the below can be commented out, as the logging should happen as
                # the radioFunction() calls the functions
                self.extTemp()  # call external temperature & log it
                self.intTemp()  # call internal temperature & log it
#                self.GPS()  # call GPS data & log it
                self.pres()  # call pressure data & log it
                time.sleep(2.0)  # waits for 2 seconds to run again
            except KeyboardInterrupt:  # allows for the system to be interrupted
                break  # ends the repeat by breaking out of the code

    def extTemp(self):
        if self.ext:  # checking if we want to read the external
            self.exto.seek(0)  # goes to the start of the ext temp file
            extM = self.exto.readlines()  # reading the lines
            extP = extM[1].find('t=')  # locating the temperature
            ext = float(extM[1][extP+2:])/1000.0  # converting the temperature
            logging.info('Ext Temp: %f', ext)  # logging the data
            return ext or None # returns the temperature for use in the radioFunction()

    def intTemp(self):
        if self.int:  # checking if we want to read the internal temp
            self.into.seek(0) #goes to the start of the int temp file
            intM = self.into.readlines()  # reading the lines
            intP = intM[1].find('t=')  # locating the temperature
            int = float(intM[1][intP+2:])/1000.0  # converting the temperature
            logging.info('Int Temp: %f', int)  # logging the data
            return int or None # returns the temperature for use in the radioFunction()

    def GPS(self):
        if self.GPS:  # checking if we want to read he GPS
            sentence = self.gpsn.readline().decode('utf8')  # reading the gps data & decoding
            sentenceid = sentence[3:6]  # parsing out the prefix
            if sentenceid == 'GGA':  # if it is the GPS data we want
                GPSData = sentence.split(",")  # split the sentence to allow the use of the data
                gps = (GPSData[2] + GPSData[3] + ', ' + GPSData[4] + GPSData[5] + ', '+GPSData[8]+ ',' +GPSData[9]+ ' m')
                # combine the data
                # [2] & [3] are latitude and hemisphere N/S
                # [4] & [5] are longitude and hemisphere E/W
                # [8] is horizontal dilution
                # [9] is the altitude in meters.
                logging.info('GPS Data: %W', gps)  # log the data
                if GPSData[2] == "N" and GPSData[4] == "W":  # checking the hemispheres
                    return float(GPSData[2]), float(GPSData[4]*-1), float(GPSData[8]), float(GPSData[9]) or None
                elif GPSData[2] == "N" and GPSData[4] == "E":  # checking the hemispheres
                    return float(GPSData[2]), float(GPSData[4]), float(GPSData[8]), float(GPSData[9]) or None
                elif GPSData[2] == "S" and GPSData[4] == "W":  # checking the hemispheres
                    return float(GPSData[2]*-1), float(GPSData[4]*-1), float(GPSData[8]), float(GPSData[9]) or None
                else:  # if none of the above
                    return float(GPSData[2]*-1), float(GPSData[4]), float(GPSData[8]), float(GPSData[9]) or None

    def pres(self):
        if self.pressure:  # checking if we want to read the pressure system
            self.bus.write_byte(self.addr, 0x58)  # writing a new bite to the bus
            time.sleep(0.05)  # pause to allow completion of previous step
            tempadcbytes = self.bus.read_i2c_block_data(self.addr, 0x00)  # temperature ADC bytes
            time.sleep(0.05)  # pause to allow completion of previous step
            self.D2 = (tempadcbytes[0] * 65536.0) + (tempadcbytes[1] * 256.0) + (tempadcbytes[2])  # temp reading convert
            self.bus.write_byte(self.addr, 0x48)  # writing a new bite to the bus
            time.sleep(0.05)  # pause to allow completion of previous step
            presadcbytes = self.bus.read_i2c_block_data(self.addr, 0x00)  # pressure ADC bytes
            time.sleep(0.05)  # pause to allow completion of previous step
            self.D1 = (presadcbytes[0] << 16)+(presadcbytes[1] << 8)+(presadcbytes[2])  # pressure reading convert

            logging.info('Pressure: %f', self.calculatePressure())  # logging the pressure
#            logging.info('Temp (P): %f', tempadc)  # logging the temperature
            return self.calculatePressure() or None # returning the pressure data for the radioFunction() to use

    def calculatePressure(self):
        self.dT =  self.D2 - self.C5*pow(2,8)
        self.TEMP = 20 + self.dT*self.C6/pow(2,23)
        self.OFF = self.C2*pow(2,16)+(self.C4*self.dT)/pow(2,7)
        self.SENS = self.C1*pow(2,15) + (self.C3*self.dT)/pow(2,8)
        self.P = self.D1*(self.SENS/pow(2,21)-self.OFF)/pow(2,15)
        return self.P


if __name__ == "__main__":  # runs the below only when testing
    Sensor = sensor(True, True, True, True)  # sets the external reading, and none of the others.
    Sensor.measure()
