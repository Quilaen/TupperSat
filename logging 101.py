import logging
from datetime import datetime
logging.basicConfig(filename="Testfile.log", level=logging.INFO)
#logging.info(str(datetime.now()) + ": This is a test log, did it work")

#logging.warning("I probably didn't configure the logging correctly.")

# logging.info(str(datetime.now()) + ": GPS Coords: " + str(GPS())+ "\n| Ext Temp: " + str(ExtT()) + "\n| Int Temp: "
# + str(IntT())+ "\n| Pressure: " + str(Pressure()))

from datetime import datetime as dt
telemetry_dict = {
    'hhmmss'        : dt.now(),
    'lat_dec_deg'   : 53.3096,
    'lon_dec_deg'   : -6.3186,
    'lat_dil'       : 1.53,
    'alt'           : 121.4,
    'temp1'         : 21.062,
    'temp2'         : -7.562,
    'pressure'      : 980.0274,
}
message = ""
for i in telemetry_dict:
    message = message + "\n|" + i + ":  " + str(telemetry_dict[i])



print(message)

logging.info(message)