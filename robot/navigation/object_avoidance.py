# navigation/obstacle_avoidance.py
import time


class ObstacleAvoidance:
    """
    Reactive obstacle avoidance using distance sensors.
    """

    def __init__(
        self,
        drive,
        sensors,
        fsm,
        stop_distance_cm: float = 25.0,
        turn_duration: float = 0.6,
    ):
        """
        :param drive: DriveBase instance
        :param sensors: SensorManager instance
        :param fsm: StateMachine instance
        :param stop_distance_cm: threshold to trigger avoidance
        :param turn_duration: seconds to turn away
        """
        self.drive = drive
        self.sensors = sensors
        self.fsm = fsm

        self.stop_distance_cm = stop_distance_cm
        self.turn_duration = turn_duration

        self._avoiding = False

    # -------------------------
    # Public interface
    # -------------------------

    def step(self):
        """
        Called periodically from Navigator.
        Decides whether to trigger or clear avoidance.
        """
        distance = self.sensors.get_front_distance_cm()

        if distance is None:
            return

        if distance < self.stop_distance_cm:
            self._handle_obstacle(distance)
        else:
            self._handle_clear()

    # -------------------------
    # Internal logic
    # -------------------------

    def _handle_obstacle(self, distance: float):
        if not self._avoiding:
            print(f"[AVOID] Obstacle at {distance:.1f} cm")

            self._avoiding = True
            self.fsm.on_obstacle_detected()

            self.drive.stop()
            time.sleep(0.1)

            # Simple reactive behavior: rotate left
            self.drive.turn_left()
            time.sleep(self.turn_duration)

            self.drive.stop()

    def _handle_clear(self):
        if self._avoiding:
            print("[AVOID] Path clear")

            self._avoiding = False
            self.fsm.on_obstacle_cleared()
