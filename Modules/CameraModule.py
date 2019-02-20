import cv2


def get_camera_module_instance():
    if not _CameraModule._CameraModuleInstance:
        _CameraModule._CameraModuleInstance = _CameraModule()
    return _CameraModule._CameraModuleInstance


class _CameraModule:
    _CameraModuleInstance = None

    def __init__(self, fps=5, frame_width=1280, frame_height=720):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CV_CAP_PROP_FRAME_WIDTH, frame_width);
        self.cap.set(cv2.CV_CAP_PROP_FRAME_HEIGHT, frame_height);
        self.cap.set(cv2.CAP_PROP_FPS, fps)
        self.check_video_source()

    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()

    def check_video_source(self):
        if not self.cap.isOpened():
            raise Exception("Unable to access camera")

    def get_frame(self):
        _, frame = self.cap.read()
        return frame
