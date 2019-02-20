import requests

_BASE_URL = 'http://ec2-52-60-89-17.ca-central-1.compute.amazonaws.com/api/'


def send_anomaly(anomaly):
    requests.post(_BASE_URL + 'anomaly', anomaly)
