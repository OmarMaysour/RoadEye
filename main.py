import logging
import sys
from Services.ClassificationService import ClassificationService
from Services.FrameRecordingService import FrameRecordingService
import multiprocessing

from Services.UploadDataService import UploadDataService


def excepthook(type_, value, traceback):
    logger.exception(value)
    sys.__excepthook__(type_, value, traceback)

def start_upload_data_service():
    upload_data_service = UploadDataService()
    upload_data_service.start_service()

def start_frame_recording_service():
    frame_recording_service = FrameRecordingService()
    frame_recording_service.start_service()

def start_classification_service():
    classification_service = ClassificationService()
    classification_service.start_service()

if __name__ == '__main__':
    logging.basicConfig(filename='app.log', format='%(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    sys.excepthook = excepthook
    multiprocessing.Process(target=start_frame_recording_service).start()
    multiprocessing.Process(target=start_classification_service).start()
    multiprocessing.Process(target=start_upload_data_service).start()