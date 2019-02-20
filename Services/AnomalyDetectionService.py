from Modules.CameraModule import get_camera_module_instance
from Modules.GPSModule import get_gps_module_instance


class AnomalyDetectionService:
    def __init__(self):
        self.camera = get_camera_module_instance()
        self.gps = get_gps_module_instance()
