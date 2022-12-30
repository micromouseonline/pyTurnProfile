import math

from pose import Pose


class RobotState():
    '''
    Describes the instantaneous state of the robot.
    '''
    def __init__(self, interval=0.001):
        self.time = 0.0
        self.distance = 0.0
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self.alpha = 0.0
        self.omega = .00
        self.speed = 0.0
        self.acceleration = 0.0
        self.phase = 0
        self.m_old_omega = self.omega
        self.m_interval = interval

    def __repr__(self):
        s = ""
        s = s + f"{self.time:.3f}, "
        s = s + f"{self.distance:.3f}, "
        s = s + f"{self.x:.3f}, "
        s = s + f"{self.y:.3f}, "
        s = s + f"{self.theta:.3f}, "
        s = s + f"{self.alpha:.3f}, "
        s = s + f"{self.omega:.3f}, "
        s = s + f"{self.speed:.3f}, "
        s = s + f"{self.acceleration:.3f}, "
        s = s + f"{self.phase:.3f}, "
        s = s + f"{self.m_old_omega:.3f}, "
        s = s + f"{self.m_interval:.3f}, "
        return s

    def set_interval(self, interval):
        self.m_interval = interval

    def update(self,slip_coefficient = 0):
        delta = self.speed * self.m_interval
        self.time += self.m_interval
        self.distance += delta
        self.x += -delta * math.cos(math.pi / 2 + math.radians(self.theta))
        self.y += -delta * math.sin(math.pi / 2 + math.radians(self.theta))
        self.theta += self.omega * self.m_interval
        self.acceleration = self.speed * math.radians(self.omega)
        # this is a nasty hack
        if abs(self.omega) > 1:
            self.alpha = (self.omega - self.m_old_omega) / self.m_interval
        else:
            self.alpha=0
        self.m_old_omega = self.omega
        # print(f"{self.time} {self.x}  {self.y} ")

    def get_pose(self):
        return Pose(self.x, self.y, self.theta)
