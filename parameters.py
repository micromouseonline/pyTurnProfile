from dataclasses import dataclass


@dataclass
class TurnParameters:
    pivot_x: float = 0.0
    pivot_y: float = 0.0
    speed: float = 0.0
    arc_radius: float = 0.0
    delta: float = 0.0
    offset: float = 0.0
    startAngle: float = 0.0
    angle: float = 0.0
    cubic_length: float = 0.0

    # def __repr__(self):
    #     s  = f"      pivot : ({self.pivot_x:.0f},{self.pivot_y:.0f})\n"
    #     s += f"  max. speed: {self.speed:.0f}\n"
    #     s += f"  arc radius: {self.arc_radius:.0f}\n"
    #     s += f"       delta: {self.delta:.0f}\n"
    #     s += f"      offset: {self.offset:.0f}\n"
    #     s += f" start angle: {self.startAngle:.0f}\n"
    #     s += f"  turn angle: {self.angle:.0f}\n"
    #     s += f"cubic_length: {self.cubic_length:.0f}\n"
    #     return s


default_params = {
    "SS90F": TurnParameters(pivot_x=0, pivot_y=0, offset=150, delta=68, arc_radius=112, startAngle=0, angle=90, speed=2200, cubic_length=248),
    "SS180": TurnParameters(pivot_x=0, pivot_y=0, offset=160, delta=127, arc_radius=85, startAngle=0, angle=180, speed=2000, cubic_length=370),
    "SD45": TurnParameters(pivot_x=0, pivot_y=0, offset=160, delta=65, arc_radius=110, startAngle=0, angle=45, speed=2200, cubic_length=134),
    "SD135": TurnParameters(pivot_x=0, pivot_y=0, offset=150, delta=90, arc_radius=83, startAngle=0, angle=135, speed=1800, cubic_length=266),
    "DS45": TurnParameters(pivot_x=90, pivot_y=0, offset=75, delta=70, arc_radius=120, startAngle=45, angle=45, speed=2200, cubic_length=144),
    "DS135": TurnParameters(pivot_x=90, pivot_y=0, offset=105, delta=90, arc_radius=80, startAngle=45, angle=135, speed=1800, cubic_length=257),
    "DD90": TurnParameters(pivot_x=90, pivot_y=0, offset=105, delta=80, arc_radius=74, startAngle=45, angle=90, speed=1800, cubic_length=173),
    "SS90E": TurnParameters(pivot_x=0, pivot_y=0, offset=75, delta=50, arc_radius=56, startAngle=0, angle=90, speed=1000, cubic_length=124),
    "DD90K": TurnParameters(pivot_x=0, pivot_y=0, offset=100, delta=50, arc_radius=199, startAngle=45, angle=90, speed=1000, cubic_length=371),
}

working_params = {
    "SS90F": TurnParameters(),
    "SS180": TurnParameters(),
    "SD45": TurnParameters(),
    "SD135": TurnParameters(),
    "DS45": TurnParameters(),
    "DS135": TurnParameters(),
    "DD90": TurnParameters(),
    "SS90E": TurnParameters(),
    "DD90K": TurnParameters(),
}
