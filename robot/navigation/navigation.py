"""
navigation.py
High-level navigation logic for the robot.
Uses GoPiGoController, SensorSuite, and ObjectDetector.
"""

import json
import time
from pathlib import Path
from typing import Optional

from robot.drive.gopigo_drive import GoPiGoController
from sensors import SensorSuite
from robot.preception.object_detection import ObjectDetector

CONFIG_PATH = Path(__file__).resolve().parent / "config.json"


def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)


class NavigationController:
    def __init__(
        self,
        controller: GoPiGoController,
        sensors: SensorSuite,
        detector: Optional[ObjectDetector] = None,
    ):
        cfg = load_config()
        self.safe_distance = cfg["navigation"]["safe_distance_cm"]
        self.scan_step = cfg["navigation"]["scan_step_degrees"]
        self.max_scan_angle = cfg["navigation"]["max_scan_angle"]

        self.controller = controller
        self.sensors = sensors
        self.detector = detector

    # ---------- Basic obstacle avoidance ----------

    def drive_forward_safe(self):
        """
        Drives forward until an obstacle is within safe_distance.
        """
        print("[NAV] Starting safe forward drive.")
        self.controller.forward()

        try:
            while True:
                d = self.sensors.get_front_distance()
                print(f"[NAV] Distance: {d:.1f} cm")

                if d < self.safe_distance:
                    print("[NAV] Obstacle detected! Stopping.")
                    self.controller.stop()
                    break

                time.sleep(0.1)
        finally:
            self.controller.stop()

    # ---------- Simple avoid-obstacle maneuver ----------

    def avoid_obstacle_simple(self):
        """
        When front is blocked, turn left/right to find a free direction.
        Very simple behavior for demo / testing.
        """
        print("[NAV] Avoiding obstacle...")
        # try turning right first
        for angle in range(self.scan_step, self.max_scan_angle + 1, self.scan_step):
            self.controller.right(self.scan_step)
            time.sleep(0.2)
            d = self.sensors.get_front_distance()
            print(f"[NAV] Scan right: angle={angle}, distance={d:.1f} cm")
            if d > self.safe_distance:
                print("[NAV] Path clear on the right. Driving forward.")
                self.drive_forward_safe()
                return

        # else, try left
        print("[NAV] Right side blocked, trying left.")
        for angle in range(self.scan_step, self.max_scan_angle + 1, self.scan_step):
            self.controller.left(self.scan_step)
            time.sleep(0.2)
            d = self.sensors.get_front_distance()
            print(f"[NAV] Scan left: angle={angle}, distance={d:.1f} cm")
            if d > self.safe_distance:
                print("[NAV] Path clear on the left. Driving forward.")
                self.drive_forward_safe()
                return

        print("[NAV] No free path found. Stopping.")
        self.controller.stop()

    # ---------- Example pill-search behavior (camera + detector later) ----------

    def search_for_pill(self):
        """
        Placeholder for pill search behavior.
        For now, only prints logs. Later: use camera + ObjectDetector.
        """
        print("[NAV] search_for_pill() called. (Implement later.)")
