import requests

def get_network_manager_instance():
    if not _NetworkManager._NetworkManagerInstance:
        _NetworkManager._NetworkManagerInstance = _NetworkManager()
    return _NetworkManager._NetworkManagerInstance

class _NetworkManager:
    _NetworkManagerInstance = None

    def __init__(self):
        self._base_url = 'http://localhost:5000/api/'
        self._anomaly_url = self._base_url + 'anomaly'
        self._road_condition_url = self._base_url + 'roadCondition'

    def post_anomaly(self, anomaly_dto):
        response = requests.post(self._anomaly_url
                                 , json=anomaly_dto.get_values_in_dictionary(), verify=False)
        return response.status_code, ""

    def post_road_condition(self, accelerometer_dto):
        response = requests.post(self._road_condition_url
                                 , json=accelerometer_dto.get_values_in_dictionary(), verify=False)
        return response.status_code, ""
