# sensors/ultrasonic.py
from gpiozero import DistanceSensor


class UltrasonicSensor:
    """
    HC-SR04 ultrasonic distance sensor.
    Returns distance in centimeters.
    """

    def __init__(
        self,
        trigger_pin: int,
        echo_pin: int,
        max_distance_cm: float = 200.0,
    ):
        self.sensor = DistanceSensor(
            trigger=trigger_pin,
            echo=echo_pin,
            max_distance=max_distance_cm / 100.0,
        )

    def read_cm(self) -> float:
        """
        Returns distance in cm.
        """
        return round(self.sensor.distance * 100.0, 2)
