from GPS import gpsFunction

def Activation(delay):
    global gpsCheck
    gpsCheck = True
    gpsFunction(delay)
    global loggingCheck
    loggingCheck = True


def Deactivaion():
    global gpsCheck
    gpsCheck = False
    global loggingCheck
    loggingCheck = False
