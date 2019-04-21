import os
from keras.models import load_model
import numpy as np
import cv2

def get_classification_logic_instance():
    if not _ClassificationLogic._ClassificationLogicInstance:
        _ClassificationLogic._ClassificationLogicInstance = _ClassificationLogic()
    return _ClassificationLogic._ClassificationLogicInstance

class _ClassificationLogic:
    _model = None
    _ClassificationLogicInstance = None

    def __init__(self, classification_frame_width=256, classification_frame_height=256):
        self._classification_frame_width = classification_frame_width
        self._classification_frame_height = classification_frame_height
        if not self._model:
            self._model = load_model(os.path.dirname(__file__) + '/../' + 'model.h5')

    def is_anomaly_and_confidences(self, frame):
        resized_frame = self._resize_frame(frame)
        classification_confidences = self._get_frame_classification_confidences(resized_frame)
        classification_confidences = self._round_and_type_correction_confidences(classification_confidences)
        is_frame_an_anomaly = self._is_frame_an_anomaly(classification_confidences)
        return is_frame_an_anomaly, classification_confidences

    def _resize_frame(self, frame):
        return cv2.resize(frame, (self._classification_frame_width, self._classification_frame_height))

    def _get_frame_classification_confidences(self, frame):
        return self._model.predict(np.expand_dims(frame, axis=0))[0]

    # noinspection PyMethodMayBeStatic
    def _round_and_type_correction_confidences(self, confidences):
        return [round(confidence.item(), 2) for confidence in confidences]

    # noinspection PyMethodMayBeStatic
    def _is_frame_an_anomaly(self, confidences):
        for confidence in confidences[:4]:
            if confidence > 0.5:
                return True
        return False
