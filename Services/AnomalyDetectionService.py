from Modules.CameraModule import get_camera_module_instance
from Modules.GPSModule import get_gps_module_instance
from Logics.ClassificationLogic import get_classification_logic_instance
from DataManagment.CacheManagerFactory import get_cache_manager_instance
from DTOs.AnomalyDTO import AnomalyDTO
import datetime
import time


class AnomalyDetectionService:
    def __init__(self):
        self._camera = get_camera_module_instance()
        self._gps = get_gps_module_instance()
        self._classificationLogic = get_classification_logic_instance()
        self._cacheManager = get_cache_manager_instance('Anomaly')

    def start_service(self):
        while True:
            start_time = time.time()

            frame = self._camera.get_frame()

            is_anomaly, confidences = self._classificationLogic.is_anomaly_and_confidences(frame)
            if not is_anomaly:
                continue

            gps_location_lat, gps_location_lng = self._gps.get_gps_location()

            current_datetime = datetime.datetime.now()
            current_datetime = current_datetime.strftime('%m/%d/%Y %I:%M:%S %p')

            anomaly_create_dto = AnomalyDTO(None, confidences[0], confidences[1], confidences[2]
                                            , confidences[3], gps_location_lat, gps_location_lng
                                            , None, current_datetime)

            self._cacheManager.cache(anomaly_create_dto, frame)

            # elapsed_time = start_time - time.time()
            # if 0 < elapsed_time < 1:
            #     time.sleep(1 - elapsed_time)

            if is_anomaly:
                print(
                    "anomaly detected with confidences " + str(confidences[0]) + " " + str(confidences[1]) + " " + str(
                        confidences[2]) + " " + str(confidences[3])
                    + " at location " + "lat " + str(gps_location_lat) + " lng " + str(
                        gps_location_lng) + " at time " + str(current_datetime))

            for x in range(29):
                self._camera.get_frame()
