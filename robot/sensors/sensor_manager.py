# sensors/sensor_manager.py

class SensorManager:
    """
    Central access point for all sensors.
    """

    def __init__(self, ultrasonic=None, camera=None):
        self.ultrasonic = ultrasonic
        self.camera = camera

    # -------------------------
    # Distance sensing
    # -------------------------

    def get_front_distance_cm(self):
        if self.ultrasonic is None:
            return None
        try:
            return self.ultrasonic.read_cm()
        except Exception:
            return None

    # -------------------------
    # Vision
    # -------------------------

    def get_camera_frame(self):
        if self.camera is None:
            return None
        ret, frame = self.camera.read()
        if not ret:
            return None
        return frame
