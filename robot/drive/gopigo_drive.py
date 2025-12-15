from drive.drive_base import DriveBase


class GopiGoDrive(DriveBase):
    
    def __init__(self, config: dict):
        super().__init__(config)
        
        try:
            from easygogpigo3 import EasyGoPiGo3
        except ImportError as e:
            raise ImportError(" easygopigo3 not found") from e
        
        self.gpg = EasyGoPiGo3
        self._apply_default_speed()
        
        
        #internal helper
    
    def _apply_default_speed(self):
        self.gpg.set_speed(self.default_speed)
    
    def _resolve_speed(self, speed: int |None) -> int:
        if speed is None:
            return self.default_speed
        return max(0,min(100, int(speed)))
    
    def forward(self, speed: int | None = None):
        speed = self._resolve_speed(speed)
        self.gpg.set_speed(speed)
        self.gpg.forward()
        
    def backward(self, speed: int | None = None):
        speed = self._resolve_speed(speed)
        self.gpg.set_speed(speed)
        self.gpg.backward()
    
    def turn_left(self, speed: int | None = None):
        speed = self._resolve_speed(speed or self.turn_speed)
        self.gpg.set_speed(speed)
        self.gpg.left()

    def turn_right(self, speed: int | None = None):
        speed = self._resolve_speed(speed or self.turn_speed)
        self.gpg.set_speed(speed)
        self.gpg.right()

    def stop(self):
        """
        Immediately stop all motors.
        Safe to call repeatedly.
        """
        self.gpg.stop()
        