from parameters import TurnParameters
import numpy as np

class TurnProfile:
    def __init__(self, params = None):
        self.profile_length = 0
        self.params = params
        pass

    def setup(self, params : TurnParameters):
        self.params = params
        pass

    def set_speed(self, speed):
        self.params.speed = speed

    def get_omega(self,p): # 0 <= p <= 1.0 
        if self.params is None:
            return 0.0
        x = max(0.0,p)
        x = min(1.0,p)
        x = p * self.params.length
        return x

class Cubic(TurnProfile):
    def __init__(self):
        super().__init__()
        self.params = None

    def setup(self, params : TurnParameters):
        self.params = params
        self.length = self.params.cubic_length
        self.k = 6.0*self.params.angle/ self.params.cubic_length

    def get_omega(self,p):
        omega = self.params.speed * self.k * p * (1-p)
        phase = 1
        if p > 0.5:
            phase = 3
        return (omega,phase)

class Trapezoid(TurnProfile):
    def __init__(self):
        super().__init__()

    def setup(self, params : TurnParameters):
        self.params = params        
        self.arc_omega = np.degrees(self.params.speed / params.arc_radius)
        self.transition_angle = params.delta * self.arc_omega / (2.0 * self.params.speed)
        self.arc_angle = params.angle - 2 * self.transition_angle
        self.arc_length = self.params.speed * self.arc_angle / self.arc_omega
        self.length = 2 * params.delta + self.arc_length

    def get_omega(self,p):
        phase = 1
        distance = p*self.length
        if distance < self.params.delta:
            omega = self.arc_omega * distance/self.params.delta 
        elif distance < self.params.delta + self.arc_length:
            omega = self.arc_omega
            phase = 2
        else:
            distance = distance - self.params.delta - self.arc_length
            omega = self.arc_omega * (1.0 - distance/self.params.delta)
            phase = 3
        
        return (omega,phase)

class Quadratic(TurnProfile):
    def __init__(self):
        super().__init__()

    def setup(self, params : TurnParameters):
        self.params = params
        self.arc_omega = np.degrees(self.params.speed / params.arc_radius)
        self.transition_angle = params.delta * 2 * self.arc_omega / (3.0 * self.params.speed)
        self.arc_angle = params.angle - 2 * self.transition_angle
        self.arc_length = self.params.speed * self.arc_angle / self.arc_omega
        self.length = 2 * params.delta + self.arc_length

    def get_omega(self,p):
        phase = 1
        distance = p*self.length
        if distance < self.params.delta:
            q = distance / self.params.delta
            omega = self.arc_omega * q * (2.0 - q)
        elif distance < self.params.delta + self.arc_length:
            omega = self.arc_omega
            phase = 2
        else:
            q = (self.length - distance)/self.params.delta
            omega = self.arc_omega * q * (2.0 - q)
            phase = 3
        return (omega,phase)

class Sinusoid(TurnProfile):
    def __init__(self):
        super().__init__()

    def setup(self, params : TurnParameters):
        self.params = params
        
        self.arc_omega = np.degrees(self.params.speed / params.arc_radius)
        self.transition_angle = params.delta * 2 * self.arc_omega / (np.pi * self.params.speed)
        self.arc_angle = params.angle - 2 * self.transition_angle
        self.arc_length = self.params.speed * self.arc_angle / self.arc_omega
        self.length = 2 * params.delta + self.arc_length

    def get_omega(self,p):
        phase = 1
        distance = p*self.length
        if distance < self.params.delta:
            q = distance / self.params.delta
            omega = self.arc_omega * np.sin(q * np.pi/2) 
        elif distance < (self.params.delta + self.arc_length):
            omega = self.arc_omega
            phase = 2
        else:
            q = (self.length - distance) / self.params.delta
            distance = distance - self.params.delta - self.arc_length
            omega = self.arc_omega * (np.sin(q * np.pi/2))
            phase = 3
        return (omega, phase)

class FullSinusoid(TurnProfile):
    def __init__(self):
        super().__init__()

    def setup(self, params : TurnParameters):
        self.params = params
        radius = 4.0*params.delta/(np.pi*np.radians(params.angle))
        self.arc_omega = np.degrees(self.params.speed / radius)
        self.length = 2 * params.delta
        

    def get_omega(self,p):
        distance = p * self.length
        omega = self.arc_omega * np.sin(np.pi * p)
        phase = 1
        if p > 0.5:
            phase = 3
        return (omega, phase)
