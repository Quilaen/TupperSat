# sensor .py
# Some classes that may be useful for designing your own sensor classes
# Robert Jeffrey , University College Dublin , 2018 -03 -02
import threading
import logging
import time
class SensorError ( Exception ):
    """ An exception class to be raised if the sensor is missing ."""
# this is just a bit of sugar . I could raise RuntimeError or some other error
# if I wanted , but it is a little more elegant to define an error that tells
# me something about what has gone wrong .
class SensorThread( threading.Thread ):
    """
    A class to represent the thread that will listen to the sensor .
    The sensor interface that is exposed to the user is stored here as
    self . master and is an instance of the Sensor class .
    SensorThread just updates sensor_value , which is an attribute of the
    master instance of the Sensor class . The user accesses this value through
    Sensor , not through SensorThread .
    The thread is terminated by setting the stop_event attribute of the master
    Sensor .
    """
    def __init__( self , master ):
        """."""
        # master is the instance of Sensor that will control this thread .
        self . master = master
        # you may also want to check that self . master has the necessary
        # attributes . Something like this should work , raising an
        # AttributeError if the attribute is missing .
        for attr in (" sensor_value ", "log "," stop_event "):
            getattr( self .master , attr )
            # lastly , since we are subclassing threading .Thread , we also need to
            # run the appropriate initialisation on that .
            threading.Thread.__init__( self )
    def run( self ):
        """
        Method representing the sensor thread 's activity .
        """
        # set the thread loop running . This will keep going until either the
        # stop_event is triggered in the master instance of Sensor , or an
        # uncaught exception is raised in this thread . At each iteration , the
        # thread simply calls self . _read_sensor () and passes the result up to
        # the master where it is saved .
        while not self.master.stop_event.is_set ():
            try :
                self.master.sensor_value = self._read_sensor ()
            except Exception as e:
                errStr = "An error occured "
                self.master.log.exception( errStr , exc_info = True )
                raise
            # note that if any error is raised , this code doesn 't handle or catch

            # it. It just records it and reraises it. You will have to write
            # appropriate code to handle these errors .
    def _read_sensor( self ):
        """
        Method called at each loop of the thread , returning the sensor value
        at that time .
        """
        # put code here that will read from the sensor . This will be based on
        # the scripts that you wrote for the 1-wire , I2C , and serial inputs in
        # the earlier code exercises . This just needs to return the value that
        # it has read .
        # value = some_code_that_actually_gets_the_data ()
        # return value
        # for now , it just raises an error !
        raise NotImplementedError("You need to write some code here !!")
class Sensor():
    """
    A class to represent the user interface to the Sensor and its
    operations . This contains user methods to start and stop the sensor , and
    to return the most recent sensor values .
    """
    def __init__( self , log ):
        """
        Initialise the Sensor instance , including configuring the
        SensorThread .
        """
        # I've attached a logging object to the Sensor , to serve as a logger
        # for both the Sensor instance and the SensorThread instance .
        self.log = log
        # self . sensor_value will store the sensor 's value . While the thread is
        # running , this value is constantly updated .
        self.sensor_value = None
        # self . stop_event gives us the ability to terminate the SensorThread
        # through the Sensor . stop () method defined below .
        self.stop_event = threading.Event()
        # self . sensor_thread is an instance of the SensorThread class , and
        # contains the thread which listens to the sensor and updates
        # sensor_value
        self.sensor_thread = SensorThread( self )
    def get_value( self ):
        """ Return the current value of the sensor ."""
        # before we get the current value , check that the sensor thread is
        # actually alive . i.e., this stops us calling Sensor . get_value ()
        # before we call Sensor . start () or after we call Sensor . stop ()
        #
        # You might do a little extra error checking here . For example , if the
        # way you handle errors in your thread is by setting sensor_value to a
        # default value , then that might need to be caught here .
        #
        if not self.sensor_thread.is_alive():
            errStr = "The sensor thread has stopped or has not been started "
            raise SensorError( errStr )
            return self.sensor_value
    def start(self):
        """ Starts the SensorThread run method ."""
        self.sensor_thread.start()
    def stop( self ):
        """
        Sends the stop event to the SensorThread . This breaks out of the loop
        in SensorThread . run and then waits for SensorThread to finish .
        """
        self.stop_event.set()
        self.sensor_thread.join()
        # Lastly , here is a simple use example .
def main():
    # create a logging object -- YOU WILL HAVE TO CONFIGURE THIS YOURSELVES !
    log = logging.getLogger( __name__ )
    # create a Sensor object -- REMEMBERING THAT YOU SHOULD HAVE ALREADY
    # WRITTEN THE APPROPRIATE METHODS TO HANDLE DATA !
    sensor = Sensor( log= log) # initialise
    sensor.start() # start the sensor thread
    while True: # infinite loop
        try:
            val = sensor.get_value() # read the sensor
            log.info(" sensor val = {}". format (val )) # log its value
            time.sleep(1.0)
        except KeyboardInterrupt : # let user stop sensor
            sensor.stop()
            break
    log.info(" Appears to have ended successfully ")
    if __name__ ==" __main__ ":
        errStr = (" Have you set up all the methods correctly ? \n\n"
                    +"If not, time to write your own code ! \n\n"
                    +"If so, delete this line of code !\n\n\n" )
        raise NotImplementedError ( errStr )
        # main ()
