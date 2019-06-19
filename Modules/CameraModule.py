import cv2


def get_camera_module_instance():
    if not _CameraModule._CameraModuleInstance:
        _CameraModule._CameraModuleInstance = _CameraModule()
    return _CameraModule._CameraModuleInstance


class _CameraModule:
    _CameraModuleInstance = None

    def __init__(self):
        self._cap = cv2.VideoCapture('video.mp4')
        # self._check_video_source()


    def __del__(self):
        if self._cap.isOpened():
            self._cap.release()

    def _check_video_source(self):
        if not self._cap.isOpened():
            raise Exception("Unable to access camera")

    def get_frame(self):
        _, frame = self._cap.read()
        return frame
