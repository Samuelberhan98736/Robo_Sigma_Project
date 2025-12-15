# navigation/state_machine.py
from enum import Enum, auto


class RobotState(Enum):
    IDLE = auto()
    MANUAL = auto()
    AUTO = auto()
    AVOID = auto()
    MANIPULATE = auto()
    STOP = auto()


class StateMachine:
    """
    Finite State Machine controlling high-level robot behavior.
    """

    def __init__(self):
        self._state = RobotState.IDLE
        self._prev_state = None

    # -------------------------
    # State access
    # -------------------------

    @property
    def state(self) -> RobotState:
        return self._state

    # -------------------------
    # State transitions
    # -------------------------

    def set_state(self, new_state: RobotState):
        if new_state == self._state:
            return

        self._prev_state = self._state
        self._state = new_state

        print(f"[FSM] {self._prev_state.name} → {self._state.name}")

    def restore_previous(self):
        """
        Return to previous state (used after AVOID).
        """
        if self._prev_state is not None:
            self.set_state(self._prev_state)

    # -------------------------
    # Events
    # -------------------------

    def on_manual_command(self):
        self.set_state(RobotState.MANUAL)

    def on_autonomy_enabled(self):
        self.set_state(RobotState.AUTO)

    def on_idle(self):
        self.set_state(RobotState.IDLE)

    def on_obstacle_detected(self):
        if self._state not in (RobotState.STOP, RobotState.MANIPULATE):
            self.set_state(RobotState.AVOID)

    def on_obstacle_cleared(self):
        if self._state == RobotState.AVOID:
            self.restore_previous()

    def on_manipulation_start(self):
        """
        Enter arm manipulation mode.
        """
        if self._state != RobotState.STOP:
            self.set_state(RobotState.MANIPULATE)

    def on_manipulation_done(self):
        """
        Exit manipulation → IDLE (safe default).
        """
        if self._state == RobotState.MANIPULATE:
            self.set_state(RobotState.IDLE)

    def on_emergency_stop(self):
        self.set_state(RobotState.STOP)

    def on_reset(self):
        self.set_state(RobotState.IDLE)
