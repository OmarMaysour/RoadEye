import os
from termcolor import colored
from DataManagment.CacheManager import get_cache_manager_instance
from Networking.NetworkManager import get_network_manager_instance
import time


class UploadDataService:
    def __init__(self):
        self._networkManager = get_network_manager_instance()
        self._cacheManager = get_cache_manager_instance()

    def start_service(self):
        print(colored("upload data service started on process " + str(os.getpid()), 'blue', 'on_grey', attrs=['bold']))
        while True:
            AnomalyDTO = self._cacheManager.get_oldest_anomaly_cache()
            if AnomalyDTO is None:
                print(colored("Upload data service: no anomalies has been found in db sleeping for 0.5s", 'blue', 'on_grey',attrs=['bold']))
                time.sleep(0.5)
                continue
            print(colored("Upload data service: posting anomaly", 'blue', 'on_grey',attrs=['bold']))
            status_code, _ = self._networkManager.post_anomaly(AnomalyDTO)
            print(colored("Upload data service: response received " + str(status_code), 'blue', 'on_grey',
                          attrs=['bold']))
            while status_code == 404 or status_code == 500:
                print(colored("failed to upload data with id: " + str(AnomalyDTO.id) + " with status code: "
                              + str(status_code), 'red', 'on_grey', attrs=['bold']))
                time.sleep(0.2)
                status_code, _ = self._networkManager.post_anomaly(AnomalyDTO)
            if status_code != 200 and status_code != 201 and str(status_code) != '200' and str(status_code) != '201':
                print(colored("failed to upload data with id: " + str(AnomalyDTO.id) + " with status code: "
                              + str(status_code), 'red', 'on_grey', attrs=['bold']))
            else:
                print(colored("successfully uploaded data with id: " + str(AnomalyDTO.id) + " with status code: "
                              + str(status_code), 'green', 'on_grey', attrs=['bold']))
            self._cacheManager.delete_cache(AnomalyDTO)
