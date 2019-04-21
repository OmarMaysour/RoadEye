import logging
import sys
from Services.AnomalyDetectionService import AnomalyDetectionService
from Services.RoadConditionService import RoadConditionService
from Services.UploadDataService import UploadDataService
from DataManagment.CacheManagerFactory import initiate_cache_manager_factory_instance_creation
import multiprocessing


def excepthook(type_, value, traceback):
    logger.exception(value)
    sys.__excepthook__(type_, value, traceback)


def start_anomaly_detection_service():
    anomaly_detection_service = AnomalyDetectionService()
    anomaly_detection_service.start_service()


def start_road_condition_service():
    road_condition_service = RoadConditionService()
    road_condition_service.start_service()


def start_upload_data_service():
    upload_data_service = UploadDataService()
    upload_data_service.start_service()

if __name__ == '__main__':
    logging.basicConfig(filename='app.log', format='%(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    sys.excepthook = excepthook
    initiate_cache_manager_factory_instance_creation()
    multiprocessing.Process(target=start_anomaly_detection_service).start()
    multiprocessing.Process(target=start_road_condition_service).start()
    multiprocessing.Process(target=start_upload_data_service).start()



