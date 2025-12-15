# arm/servo_arm.py
import time
from arm.arm_base import ArmBase
from arm.kinematics import ArmKinematics


class ServoArm(ArmBase):
    """
    Servo-driven robotic arm using PCA9685 + MG996R.
    Supports:
      - joint control
      - gripper control
      - inverse kinematics (x, y, z)
    """

    def __init__(self, config: dict):
        super().__init__(config)

        try:
            from adafruit_servokit import ServoKit
        except ImportError as e:
            raise ImportError(
                "adafruit-circuitpython-servokit is not installed"
            ) from e

        arm_cfg = config["arm"]

        # Required config
        self.channels = arm_cfg["servo_channels"]
        self.home_angles = arm_cfg["home_angles"]
        self.limits = arm_cfg["limits"]
        self.link_lengths = arm_cfg["link_lengths_cm"]

        # Servo controller
        self.kit = ServoKit(channels=16)

        # Kinematics engine
        self.kinematics = ArmKinematics(self.link_lengths)

        # Track current angles
        self._angles = {}

        # Initialize to home
        self.home()

    # -------------------------
    # Internal helpers
    # -------------------------

    def _clamp(self, joint: str, angle: float) -> float:
        lo, hi = self.limits[joint]
        return max(lo, min(hi, angle))

    def _set_servo(self, joint: str, angle: float):
        angle = self._clamp(joint, angle)
        channel = self.channels[joint]

        self.kit.servo[channel].angle = angle
        self._angles[joint] = angle
        time.sleep(0.02)  # small delay for stability

    # -------------------------
    # ArmBase implementation
    # -------------------------

    def home(self):
        """
        Move arm to a safe home position.
        """
        for joint, angle in self.home_angles.items():
            self._set_servo(joint, angle)

    def move_joint(self, joint: str, angle: float):
        """
        Move a single joint to an absolute angle (degrees).
        """
        if joint not in self.channels:
            raise ValueError(f"Unknown joint '{joint}'")
        self._set_servo(joint, angle)

    def open_gripper(self):
        """
        Fully open the gripper.
        """
        self.move_joint("gripper", self.limits["gripper"][1])

    def close_gripper(self):
        """
        Fully close the gripper.
        """
        self.move_joint("gripper", self.limits["gripper"][0])

    def stop(self):
        """
        Servos hold position by default.
        This exists for interface completeness.
        """
        pass

    # -------------------------
    # Task-space control (IK)
    # -------------------------

    def move_to_xyz(self, x: float, y: float, z: float):
        """
        Move end-effector to (x, y, z) in cm using inverse kinematics.
        """
        solution = self.kinematics.inverse(x, y, z)

        if solution is None:
            raise ValueError(
                f"Target ({x:.1f}, {y:.1f}, {z:.1f}) cm is unreachable"
            )

        base, shoulder, elbow = solution

        self.move_joint("base", base)
        self.move_joint("shoulder", shoulder)
        self.move_joint("elbow", elbow)

    # -------------------------
    # Forward kinematics (debug)
    # -------------------------

    def get_end_effector_position(self):
        """
        Return current (x, y, z) position using forward kinematics.
        """
        required = ["base", "shoulder", "elbow"]
        if not all(j in self._angles for j in required):
            return None

        return self.kinematics.forward(
            self._angles["base"],
            self._angles["shoulder"],
            self._angles["elbow"],
        )
