from satradio import SatRadio

myaddress = 0x53
myradio = SatRadio('/dev/ttyAMAO', myaddress, 'TestSat1', callback = mycallbackfunction)

myradio.start()
from datetime import datetime as dt
telemetry_dict = {
    'hhmmss'        : dt.now(),
    'lat_dec_deg'   : 53.3096 ,
    'lon_dec_deg'   : -6.3186 ,
    'lat_dil'       : 1.53,
    'alt'           : 121.4,
    'temp1'         : 21.062,
    'temp2'         : -7.562,
    'pressure'      : 980.0274,
}
datetime.datetime.now(),53.3096, -6.2186, 1.53, 121.4, 21.062, -7.562, 980.0274)
    myradio.send_telemetry()
myradio.stop()

