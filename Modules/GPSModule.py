# import serial               #import serial pacakge
# from time import sleep
# import sys                  #import system package

def get_gps_module_instance():
    if not _GPSModule._GPSModuleInstance:
        _GPSModule._GPSModuleInstance = _GPSModule()
    return _GPSModule._GPSModuleInstance


class _GPSModule:
    _GPSModuleInstance = None

    def get_gps_location(self):
        # try:
        #     return self.GPS_Info()
        # except:
        #     return 0, 0
        return 1, 1

    # def GPS_Info(self):
    #     global NMEA_buff
    #     global lat_in_degrees
    #     global long_in_degrees
    #     nmea_time = []
    #     nmea_latitude = []
    #     nmea_longitude = []
    #     nmea_time = NMEA_buff[0]  # extract time from GPGGA string
    #     nmea_latitude = NMEA_buff[1]  # extract latitude from GPGGA string
    #     nmea_longitude = NMEA_buff[3]  # extract longitude from GPGGA string
    #
    #     print("NMEA Time: ", nmea_time, '\n')
    #     print("NMEA Latitude:", nmea_latitude, "NMEA Longitude:", nmea_longitude, '\n')
    #
    #     lat = float(nmea_latitude)  # convert string into float for calculation
    #     longi = float(nmea_longitude)  # convertr string into float for calculation
    #
    #     lat_in_degrees = self.convert_to_degrees(lat)  # get latitude in degree decimal format
    #     long_in_degrees = self.convert_to_degrees(longi)  # get longitude in degree decimal format
    #
    # # convert raw NMEA string into degree decimal format
    # def convert_to_degrees(self, raw_value):
    #     decimal_value = raw_value / 100.00
    #     degrees = int(decimal_value)
    #     mm_mmmm = (decimal_value - int(decimal_value)) / 0.6
    #     position = degrees + mm_mmmm
    #     position = "%.4f" % (position)
    #     return position
