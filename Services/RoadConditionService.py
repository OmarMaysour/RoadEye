from Modules.AccelerometerModule import get_accelerometer_module_instance
from Modules.GPSModule import get_gps_module_instance
from DataManagment.CacheManagerFactory import get_cache_manager_instance
import datetime
from DTOs.AccelerometerDTO import AccelerometerDTO
import time


class RoadConditionService:
    def __init__(self):
        self._accelerometer = get_accelerometer_module_instance()
        self._gps = get_gps_module_instance()
        self._cacheManager = get_cache_manager_instance('Accelerometer')

    def start_service(self):
        while True:
            accelerometer_read_x, accelerometer_read_y, accelerometer_read_z = self._accelerometer.get_accelerometer_read()

            gps_location_lat, gps_location_lng = self._gps.get_gps_location()

            current_datetime = datetime.datetime.now()
            current_datetime = current_datetime.strftime('%m/%d/%Y %I:%M:%S %p')

            accelerometer_create_dto = AccelerometerDTO(None, accelerometer_read_x, accelerometer_read_y
                                                        , accelerometer_read_z, gps_location_lat
                                                        , gps_location_lng, current_datetime)

            self._cacheManager.cache(accelerometer_create_dto)

            print("accelerometer value " + str(accelerometer_read_x) + " " + str(accelerometer_read_y) + " " + str(
                accelerometer_read_z) + " at location " + "lat " + str(gps_location_lat) + " lng " + str(
                gps_location_lng) + " at time " + str(current_datetime))
            time.sleep(1)
