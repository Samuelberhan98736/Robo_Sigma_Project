from abc import ABC, abstractmethod

# abstract base class for any robot drive system
# this class definesth e required interface that all drive implemntaions must follow
#nav and control code should only depen on this interface never on hardware
class DriveBase(ABC):
    def __init__(self, config:dict):
        self.config = config
        self.default_speed = config.get("default_speed", 50)
        self.turn_speed = config.get("turn_spped", 40)
        
    @abstractmethod   
    def forward(self, speed: int | None = None):
         raise NotImplementedError   
    
    @abstractmethod
    def backward(self, speed:int |None = None):
        raise NotImplementedError 
    
    @abstractmethod
    def turn_left(self, speed:int |None = None):
        raise NotImplementedError
    @abstractmethod
    def turn_right(self, speed:int | None = None):
        raise NotImplementedError
    @abstractmethod
    def stop(self):
        raise NotImplementedError
    
    
    
    def move(self, linear:float, angular: float):
       if abs(linear) < 1e-3 and abs(angular) < 1e-3:
           self.stop()
           return
       
       if abs (angular) > abs(linear):
           if angular > 0:
               self.turn_lef()
           else:
               self.turn_right()
       else:
            if linear > 0:
                self.forward()
            else:
                self.backward()
    
    def emergency_stop(self):
        self.stop
                   
    
    