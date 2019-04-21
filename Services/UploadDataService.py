from DataManagment.AccelerometerCacheManager import get_new_accelerometer_cache_manager_instance
from DataManagment.AnomalyCacheManager import get_new_anomaly_cache_manager_instance
from Networking.NetworkManager import get_network_manager_instance
import threading
import time
import sqlite3

class UploadDataService:
    def __init__(self):
        self.networkManager = get_network_manager_instance()

    def start_service(self):
        threading.Thread(target=self._upload_anomaly).start()
        threading.Thread(target=self._upload_road_condition).start()

    def _upload_anomaly(self):
        anomalyCacheManager = get_new_anomaly_cache_manager_instance(sqlite3.connect('roadeye_cache.db'))
        while True:
            cached_anomaly = anomalyCacheManager.get_oldest_cache()
            status_code, response_json = self.networkManager.post_anomaly(cached_anomaly)
            while status_code == 404 or status_code == 500:
                time.sleep(0.2)
                status_code, response_json = self.networkManager.post_anomaly(cached_anomaly)
            print("anomaly posted with status code " + str(status_code))
            self._delete_cached_anomaly(anomalyCacheManager, cached_anomaly)
            time.sleep(0.8)

    def _upload_road_condition(self):
        accelerometerCacheManager = get_new_accelerometer_cache_manager_instance(sqlite3.connect('roadeye_cache.db'))
        while True:
            cached_accelerometer_read = accelerometerCacheManager.get_oldest_cache()
            status_code, response_json = self.networkManager.post_road_condition(cached_accelerometer_read)
            while status_code == 404 or status_code == 408:
                time.sleep(0.2)
                status_code, response_json = self.networkManager.post_road_condition(cached_accelerometer_read)
            print("road condition posted with status code " + str(status_code))
            self._delete_cached_road_condition(accelerometerCacheManager, cached_accelerometer_read)
            time.sleep(0.8)

    def _delete_cached_anomaly(self, cacheManager, anomaly_dto):
        cacheManager.delete_cache(anomaly_dto)

    def _delete_cached_road_condition(self, cacheManager, accelerometer_dto):
        cacheManager.delete_cache(accelerometer_dto)
