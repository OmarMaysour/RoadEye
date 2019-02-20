import os
from keras.models import load_model
import numpy as np
from PIL import Image


class ClassificationLogic:
    _model = None

    def __init__(self, classification_frame_width=299, classification_frame_height=299):
        self.classification_frame_width = classification_frame_width
        self.classification_frame_height = classification_frame_height

        if not self._model:
            self._model = load_model(os.path.dirname(__file__) + '/' + 'model.h5')

    def is_anomaly_and_confidence(self, frame):
        resized_frame = self.resize_frame(frame)
        classification_confidence = self.get_frame_classification_confidence(resized_frame)
        is_frame_an_anomaly = self.is_frame_an_anomaly(classification_confidence)
        return is_frame_an_anomaly, classification_confidence

    def resize_frame(self, frame):
        return frame.resize((self.classification_frame_width, self.classification_frame_height), Image.ANTIALIAS)

    def get_frame_classification_confidence(self, frame):
        return self._model.predict(np.expand_dims(frame), axis=0)[0]

    # noinspection PyMethodMayBeStatic
    def is_frame_an_anomaly(self, confidence):
        if confidence > 0.5:
            return True
        else:
            return False
