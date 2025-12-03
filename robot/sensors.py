"""
sensors.py
Wraps all physical sensors (ultrasonic, camera, etc.) into simple classes.
"""

import json
import time
from pathlib import Path

import RPi.GPIO as GPIO

CONFIG_PATH = Path(__file__).resolve().parent / "config.json"


def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)


class UltrasonicSensor:
    def __init__(self, trig_pin: int, echo_pin: int, timeout: float = 0.02):
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin
        self.timeout = timeout

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

    def get_distance_cm(self) -> float:
        """
        Returns distance in cm using HC-SR04.
        """
        # Send 10µs pulse
        GPIO.output(self.trig_pin, True)
        time.sleep(0.00001)
        GPIO.output(self.trig_pin, False)

        start = time.time()
        while GPIO.input(self.echo_pin) == 0:
            start = time.time()
            if time.time() - start > self.timeout:
                return float("inf")

        while GPIO.input(self.echo_pin) == 1:
            end = time.time()
            if end - start > self.timeout:
                return float("inf")

        duration = end - start
        distance = (duration * 34300) / 2  # speed of sound (cm/s)
        return distance

    def cleanup(self):
        GPIO.cleanup((self.trig_pin, self.echo_pin))


class SensorSuite:
    """
    High-level wrapper that groups all sensors together.
    """

    def __init__(self):
        cfg = load_config()
        us_cfg = cfg["ultrasonic"]

        self.ultrasonic = UltrasonicSensor(
            trig_pin=us_cfg["trig_pin"],
            echo_pin=us_cfg["echo_pin"],
            timeout=us_cfg["timeout_s"],
        )

        # Camera / other sensors can be added here later.
        self.camera = None  # placeholder

    def get_front_distance(self) -> float:
        return self.ultrasonic.get_distance_cm()

    def cleanup(self):
        self.ultrasonic.cleanup()
