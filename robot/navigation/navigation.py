# navigation/navigator.py
import time
from navigation.state_machine import RobotState
from navigation.obstacle_avoidance import ObstacleAvoidance


class Navigator:
    """
    High-level controller that:
    - runs obstacle avoidance checks
    - executes behavior based on FSM state
    - accepts manual commands (from Bluetooth)
    """

    def __init__(self, drive, sensors, fsm, config: dict):
        """
        :param drive: DriveBase implementation (e.g., GoPiGoDrive)
        :param sensors: SensorManager
        :param fsm: StateMachine
        :param config: full config dict loaded from config.json
        """
        self.drive = drive
        self.sensors = sensors
        self.fsm = fsm

        nav_cfg = config.get("navigation", {})
        avoid_cfg = nav_cfg.get("avoidance", {})

        self.avoidance = ObstacleAvoidance(
            drive=self.drive,
            sensors=self.sensors,
            fsm=self.fsm,
            stop_distance_cm=avoid_cfg.get("stop_distance_cm", 25.0),
            turn_duration=avoid_cfg.get("turn_duration_sec", 0.6),
        )

        # Manual control state (set by handle_manual_command)
        self._manual_linear = 0.0   # [-1..1]
        self._manual_angular = 0.0  # [-1..1]
        self._manual_last_update = 0.0
        self._manual_timeout_sec = nav_cfg.get("manual_timeout_sec", 0.6)

        # Auto mode behavior (simple for now)
        self._auto_speed = nav_cfg.get("auto_speed", drive.default_speed)

    # -------------------------
    # Manual command entrypoint
    # -------------------------

    def handle_manual_command(self, linear: float, angular: float):
        """
        Called by Bluetooth/server layer.
        linear, angular in [-1.0, 1.0] (ROS-style).
        """
        self._manual_linear = max(-1.0, min(1.0, float(linear)))
        self._manual_angular = max(-1.0, min(1.0, float(angular)))
        self._manual_last_update = time.time()

        # Put robot into MANUAL mode immediately
        self.fsm.on_manual_command()

        # If command is "stop-ish", allow IDLE fallback
        if abs(self._manual_linear) < 1e-3 and abs(self._manual_angular) < 1e-3:
            self.fsm.on_idle()

    def enable_autonomy(self):
        """Switch to AUTO mode."""
        self.fsm.on_autonomy_enabled()

    def emergency_stop(self):
        """Hard stop."""
        self.fsm.on_emergency_stop()
        self.drive.emergency_stop()

    def reset_from_stop(self):
        """Reset STOP -> IDLE."""
        self.fsm.on_reset()

    # -------------------------
    # Main control loop
    # -------------------------

    def step(self):
        """
        Call this repeatedly (e.g., 10–30 Hz).
        """

        # STOP overrides everything
        if self.fsm.state == RobotState.STOP:
            self.drive.emergency_stop()
            return

        # Always run avoidance check (it will push FSM into AVOID)
        self.avoidance.step()

        # If in AVOID, do nothing else this cycle (avoidance already acted)
        if self.fsm.state == RobotState.AVOID:
            return

        # Behavior by state
        if self.fsm.state == RobotState.IDLE:
            self.drive.stop()
            return

        if self.fsm.state == RobotState.MANUAL:
            self._manual_step()
            return

        if self.fsm.state == RobotState.AUTO:
            self._auto_step()
            return

    # -------------------------
    # Internal behaviors
    # -------------------------

    def _manual_step(self):
        # If manual commands stop coming in, drop to IDLE for safety
        if (time.time() - self._manual_last_update) > self._manual_timeout_sec:
            self.drive.stop()
            self.fsm.on_idle()
            return

        # Use ROS-style drive.move(linear, angular)
        self.drive.move(self._manual_linear, self._manual_angular)

    def _auto_step(self):
        """
        Simple AUTO behavior for MVP:
        - Drive forward at auto_speed
        - ObstacleAvoidance will interrupt if needed
        """
        # If path is clear, just go forward.
        # You can replace this later with waypoint following / vision approach.
        self.drive.forward(self._auto_speed)
