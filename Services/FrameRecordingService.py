import datetime
import os
import cv2
from termcolor import colored
from DTOs.ToClassifyAnomalyDTO import ToClassifyAnomalyDTO
from DataManagment.CacheManager import get_cache_manager_instance
from Modules.CameraModule import get_camera_module_instance
from Modules.GPSModule import get_gps_module_instance

class FrameRecordingService:
    def __init__(self):
        self._camera = get_camera_module_instance()
        self._gps = get_gps_module_instance()
        self._cacheManager = get_cache_manager_instance()

    def start_service(self):
        print(colored("frame recording service started on process " + str(os.getpid()), 'blue', 'on_grey', attrs=['bold']))
        while True:
            frame = self._camera.get_frame()
            cv2.imshow('Frame', frame)

            lat, lng = self._gps.get_gps_location()
            current_datetime = datetime.datetime.now()
            current_datetime = current_datetime.strftime('%m/%d/%Y %I:%M:%S %p')

            self._cacheManager.cache_to_classify_anomaly(ToClassifyAnomalyDTO(0, lat, lng, "", current_datetime), frame)
            print(colored("a frame has been saved", 'cyan', 'on_grey', attrs=['bold']))

            for x in range(29):
                self._camera.get_frame()

            cv2.waitKey(1000)

