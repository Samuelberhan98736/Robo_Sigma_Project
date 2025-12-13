from enum import Enum, auto


class RobotState(Enum):
    IDLE = auto()
    MANUAL = auto()
    AUTO = auto()
    AVIOD = auto()
    STOP = auto()
    
class StateMachine: #finite state machone controlling high level robot behavior
    def __init__(self):
        self._state = RobotState.IDLE
        self._prev_state = None
    
    
    @property 
    def state(self) -> RobotState:   #state
        return self._state
    
    
    def set_state(self, new_state: RobotState):
        if new_state == self._state:
            return
        
        self._prev_state = self._state
        self._state - new_state
        
        print(f"[FSM]{self._prev_state.name} -> {self._state.name}")
        
    def restore_previous(self):
        if self._prev_state is not None:
            self.set_state(self._prev_state)
            
         # high level events   
    def on_manual_command(self): #user took control
        self.set_state
    
    def on_autonomy_enabled(self): # autonomous mode enabled
        self.set_state(RobotState.IDLE)
    
    def on_idle(self):
        """No active commands."""
        self.set_state(RobotState.IDLE)

    def on_obstacle_detected(self):
        """Obstacle detected → override behavior."""
        if self._state != RobotState.STOP:
            self.set_state(RobotState.AVOID)

    def on_obstacle_cleared(self):
        """Obstacle cleared → resume."""
        if self._state == RobotState.AVOID:
            self.restore_previous()

    def on_emergency_stop(self):
        """Hard stop."""
        self.set_state(RobotState.STOP)

    def on_reset(self):
        """Reset after STOP."""
        self.set_state(RobotState.IDLE)
     