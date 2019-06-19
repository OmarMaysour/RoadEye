import os
import time

import cv2
from termcolor import colored

from DTOs.AnomalyDTO import AnomalyDTO
from DataManagment.CacheManager import get_cache_manager_instance
from Logics.ClassificationLogic import get_classification_logic_instance


class ClassificationService:
    def __init__(self):
        self._cacheManager = get_cache_manager_instance()
        self._classificationLogic = get_classification_logic_instance()

    def start_service(self):
        print(colored("classification service started on process " + str(os.getpid()), 'blue', 'on_grey', attrs=['bold']))
        while True:
            toClassifyAnomalyDTO = self._cacheManager.get_oldest_to_classify_anomaly_cache()
            if toClassifyAnomalyDTO is None:
                time.sleep(1)
                continue
            frame = cv2.imread('cache/' + toClassifyAnomalyDTO.image_uri)
            is_anomaly, confidences = self._classificationLogic.is_anomaly_and_confidences(frame)
            self._cacheManager.delete_to_classify_anomaly(toClassifyAnomalyDTO.id)
            if is_anomaly:
                print(colored("anomaly detected " + toClassifyAnomalyDTO.image_uri + " pothole: " + str(confidences[0]) + " bump " + str(confidences[1])
                              + " manhole " + str(confidences[2]) + " roadcrack " + str(confidences[3]), 'cyan', 'on_grey', attrs=['bold']))
                self._cacheManager.cache_anomaly(AnomalyDTO(0, confidences[0], confidences[1], confidences[2],
                                                confidences[3], toClassifyAnomalyDTO.lat, toClassifyAnomalyDTO.lng,
                                                toClassifyAnomalyDTO.image_uri, toClassifyAnomalyDTO.created_at))
            else:
                print(
                    colored("frame isn't a anomaly" + toClassifyAnomalyDTO.image_uri, 'blue', 'on_grey', attrs=['bold']))
                self._cacheManager.delete_image(toClassifyAnomalyDTO.image_uri)
