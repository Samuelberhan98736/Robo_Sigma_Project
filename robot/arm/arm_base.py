# arm/arm_base.py
from abc import ABC, abstractmethod


class ArmBase(ABC):
    """
    Abstract interface for a robotic manipulator.
    Navigation / FSM code should depend ONLY on this interface.
    """

    def __init__(self, config: dict):
        self.config = config

    # -------------------------
    # Core actions
    # -------------------------

    @abstractmethod
    def home(self):
        """Move arm to a safe home position."""
        raise NotImplementedError

    @abstractmethod
    def move_joint(self, joint: str, angle: float):
        """
        Move a single joint to an absolute angle (degrees).
        """
        raise NotImplementedError

    @abstractmethod
    def open_gripper(self):
        """Open gripper."""
        raise NotImplementedError

    @abstractmethod
    def close_gripper(self):
        """Close gripper."""
        raise NotImplementedError

    # -------------------------
    # Safety
    # -------------------------

    @abstractmethod
    def stop(self):
        """Stop arm motion safely."""
        raise NotImplementedError
