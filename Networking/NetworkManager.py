import requests
import json

def get_network_manager_instance():
    if not _NetworkManager._NetworkManagerInstance:
        _NetworkManager._NetworkManagerInstance = _NetworkManager()
    return _NetworkManager._NetworkManagerInstance

class _NetworkManager:
    _NetworkManagerInstance = None

    def __init__(self):
        self._base_url = 'http://localhost:5000/api/road/'
        self._anomaly_url = self._base_url + 'anomaly'

    def post_anomaly(self, anomaly_dto):
        frame = open('cache/' + anomaly_dto.image_uri, 'rb')

        response = requests.post(self._anomaly_url, data={'createAnomalyDto': json.dumps(anomaly_dto.get_values_to_payload())}
                                     , files={'AnomalyImage': frame}, verify=False)

        return response.status_code, ""
