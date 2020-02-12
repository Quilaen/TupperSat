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

    def initialize(self):
        self.bus = SMBus(I2C_bus_number)
        self.address = address
        self.C1 = 0
        self.C2 = 0
        self.C3 = 0
        self.C4 = 0
        self.C5 = 0
        self.C6 = 0
        self.D1 = 0
        self.D2 = 0
        self.TEMP = 0.0  # Calculated temperature
        self.PRES = 0.0  # Calculated Pressure
        ## The MS6511 Sensor stores 6 values in the EPROM memory that we need in order to calculate the actual temperature and pressure
        ## These values are calculated/stored at the factory when the sensor is calibrated.
        ##      I probably could have used the read word function instead of the whole block, but I wanted to keep things consistent.
        C1 = self.bus.read_i2c_block_data(self.address, self.0xA2)  # Pressure Sensitivity
        # time.sleep(0.05)
        C2 = self.bus.read_i2c_block_data(self.address, self.0xA4)  # Pressure Offset
        # time.sleep(0.05)
        C3 = self.bus.read_i2c_block_data(self.address, self.0xA6)  # Temperature coefficient of pressure sensitivity
        # time.sleep(0.05)
        C4 = self.bus.read_i2c_block_data(self.address,
                                          self.0xA8)  # Temperature coefficient of pressure offset
        # time.sleep(0.05)
        C5 = self.bus.read_i2c_block_data(self.address, self.OxAA)  # Reference temperature
        # time.sleep(0.05)
        C6 = self.bus.read_i2c_block_data(self.address,
                                          self.OxAC)  # Temperature coefficient of the temperature

        ## Again here we are converting the 2 8bit packages into a single decimal
        self.C1 = C1[0] * 256.0 + C1[1]
        self.C2 = C2[0] * 256.0 + C2[1]
        self.C3 = C3[0] * 256.0 + C3[1]
        self.C4 = C4[0] * 256.0 + C4[1]
        self.C5 = C5[0] * 256.0 + C5[1]
        self.C6 = C6[0] * 256.0 + C6[1]

#        self.update()

    def calculatePressureAndTemperature(self):
        dT = self.D2 - self.C5 * 2 ** 8
        self.TEMP = 2000 + dT * self.C6 / 2 ** 23

        OFF = self.C2 * 2 ** 16 + (self.C4 * dT) / 2 ** 7
        SENS = self.C1 * 2 ** 15 + (self.C3 * dT) / 2 ** 8

        if (self.TEMP >= 2000):
            T2 = 0
            OFF2 = 0
            SENS2 = 0
        elif (self.TEMP < 2000):
            T2 = dT * dT / 2 ** 31
            OFF2 = 5 * ((self.TEMP - 2000) ** 2) / 2
            SENS2 = OFF2 / 2
        elif (self.TEMP < -1500):
            OFF2 = OFF2 + 7 * ((self.TEMP + 1500) ** 2)
            SENS2 = SENS2 + 11 * (self.TEMP + 1500) ** 2 / 2

        self.TEMP = self.TEMP - T2
        OFF = OFF - OFF2
        SENS = SENS - SENS2

        self.PRES = (self.D1 * SENS / 2 ** 21 - OFF) / 2 ** 15

        self.TEMP = self.TEMP / 100  # Temperature updated
        self.PRES = self.PRES / 100  # Pressure updated

    def refreshPressure(self, OSR=0x48):
        self.bus.write_byte(self.address, OSR)

    def refreshTemperature(self, OSR=0x58):
        self.bus.write_byte(self.address, OSR)

    def readPressure(self):
        D1 = self.bus.read_i2c_block_data(self.address, self.0x00)
        self.D1 = D1[0] * 65536 + D1[1] * 256.0 + D1[2]

    def readTemperature(self):
        D2 = self.bus.read_i2c_block_data(self.address, self.0x00)
        self.D2 = D2[0] * 65536 + D2[1] * 256.0 + D2[2]

    def pres(self):
        if self.pressure:  # checking if we want to read the pressure system
#            bus = smbus.SMBus(1)  # setting which bus to read
#            addr = self.pressuren  # setting the i2c address
#            bus.write_byte(addr, 0x58)  # writing a new bite to the bus
#            time.sleep(0.05)  # pause to allow completion of previous step
#            tempadcbytes = bus.read_i2c_block_data(addr, 0x00)  # temperature ADC bytes
#            time.sleep(0.05)  # pause to allow completion of previous step
#            tempadc = (tempadcbytes[0] * 65536.0) + (tempadcbytes[1] * 256.0) + (tempadcbytes[2])  # temp reading convert
#            bus.write_byte(addr, 0x48)  # writing a new bite to the bus
#            time.sleep(0.05)  # pause to allow completion of previous step
#            presadcbytes = bus.read_i2c_block_data(addr, 0x00)  # pressure ADC bytes
#            time.sleep(0.05)  # pause to allow completion of previous step
#            presadc = (presadcbytes[0] << 16)+(presadcbytes[1] << 8)+(presadcbytes[2])  # pressure reading convert
            self.refreshPressure()
            self.refreshTemperature()
            self.readPressure()
            self.readTemperature()
            self.calculatePressureAndTemperature()
            logging.info('Pressure: %f', self.returnPressure())  # logging the pressure
#            logging.info('Temp (P): %f', tempadc)  # logging the temperature
            return presadc or None # returning the pressure data for the radioFunction() to use


if __name__ == "__main__":  # runs the below only when testing
	Sensor = sensor(True, True, True, True)  # sets the external reading, and none of the others.
	Sensor.measure()
