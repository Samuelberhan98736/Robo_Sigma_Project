# sensors/camera.py
import cv2


class Camera:
    """
    Camera wrapper (PiCam or USB).
    """

    def __init__(self, device_index: int = 0):
        self.cap = cv2.VideoCapture(device_index)
        if not self.cap.isOpened():
            raise RuntimeError("Camera could not be opened")

    def read(self):
        """
        Returns (ret, frame).
        """
        return self.cap.read()

    def release(self):
        self.cap.release()
