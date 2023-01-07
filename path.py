import copy
import math
from enum import Enum

from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5.QtCore import (Qt)
from PyQt5.QtWidgets import QGraphicsItem

from parameters import TurnParameters, default_params
from robot_state import RobotState
from trajectory import Trajectory
from profilers import *
from pose import Pose


class ProfileType(Enum):
    TRAPEZOID = 1
    SINUSOID = 2
    FULL_SINUSOID = 3
    QUADRATIC = 4
    CUBIC = 5


class Path(QGraphicsItem):
    '''
    Path is a visible representation of a trajectory?
    '''

    def __init__(self, parent=None):
        super().__init__(parent)
        self.path_points = []
        self.turnRadius = 0.0
        self.turnSpeed = 0.0
        self.turnAngle = 0.0
        self.start_angle = 0.0
        self.turn_end = 0
        self.min_x = 0
        self.min_y = 0
        self.max_x = 0
        self.max_y = 0
        self.trajectory = Trajectory()
        self.trajectory.set_profiler(Trapezoid())
        parameters = copy.copy(default_params["SS90F"])
        parameters.speed = 2000.1
        parameters.k_grip = 200.0
        self.trajectory.set_params(parameters)
        self.trajectory.set_start_xy(0,0)


    def boundingRect(self):
        return QRectF(-100.0, -100.0, 600.0, 600.0)

    def path_count(self):
        return self.trajectory.n_items

    def get_state_at(self, index):
        if index >= self.path_count():
            index = self.path_count() - 1
        if index < 0:
            index = 0
        return self.path_points[index]

    def get_pose_at(self, index):
        x = self.trajectory.x_actual[index]
        y = self.trajectory.y_actual[index]
        theta = self.trajectory.theta_ideal[index]
        return Pose(x,y,theta)


    def get_max_acceleration(self):
        return np.max(np.radians(self.trajectory.omega_ideal) * self.trajectory.speed)

    def get_max_alpha(self):
        return np.max(self.trajectory.alpha)


    def get_max_omega(self):
        return np.max(self.trajectory.omega_ideal)

    def paint(self, painter, option, widget):
        # if len(self.path_points) == 0:
        if self.trajectory.n_items == 0:
            return
        colors = [Qt.magenta, Qt.green, Qt.red, Qt.yellow, Qt.cyan, Qt.magenta]
        colors_ideal = [QColor('#909'),QColor('#909'),QColor('#900'),QColor('#990'),QColor('#099'),QColor('#909')]
        colors_actual= [QColor('#f0f'),QColor('#0f0'),QColor('#f00'),QColor('#ff0'),QColor('#0ff'),QColor('#f0f')]
        pen = QPen(Qt.white)
        pen.setWidthF(2.0)
        painter.setPen(pen)
        for i in range(0, self.trajectory.n_items, 2):
            phase = int(self.trajectory.phase[i])
            pen.setColor(colors_ideal[phase])
            painter.setPen(pen)
            rect = QRectF(self.trajectory.x_ideal[i], self.trajectory.y_ideal[i], 1.0, 1.0)
            painter.drawEllipse(rect)
            pen.setColor(colors_actual[phase])
            rect = QRectF(self.trajectory.x_actual[i], self.trajectory.y_actual[i], 2.0, 2.0)
            painter.setPen(pen)
            painter.drawEllipse(rect)
        xi,yi,xa,ya = self.calculate_leadout()
        pen.setColor(colors_ideal[5])
        painter.setPen(pen)
        for i,x_pos in enumerate(xi):
            rect = QRectF(xi[i], yi[i], 1.0, 1.0)
            painter.drawEllipse(rect)
        pen.setColor(colors_actual[5])
        painter.setPen(pen)
        for i,x_pos in enumerate(xi):
            rect = QRectF(xa[i], ya[i], 1.0, 1.0)
            painter.drawEllipse(rect)

    
    def calculate_leadout(self):
        distance = 100
        speed = self.trajectory.speed
        t0 = self.trajectory.time[-1]
        t1 = t0 + distance/speed
        time = np.arange(t0,t1,self.trajectory.delta_t)
        x_ideal = np.zeros(len(time))
        y_ideal = np.zeros(len(time))
        x_actual = np.zeros(len(time))
        y_actual = np.zeros(len(time))
        angle = self.trajectory.theta_ideal[-1] 
        x_i = self.trajectory.x_ideal[-1]
        y_i = self.trajectory.y_ideal[-1]
        x_a = self.trajectory.x_actual[-1]
        y_a = self.trajectory.y_actual[-1]
        for i,t in enumerate(time):
            x_ideal[i] = x_i
            y_ideal[i] = y_i
            x_actual[i] = x_a
            y_actual[i] = y_a
            dx = speed * np.cos(np.radians(angle)) * self.trajectory.delta_t
            dy = speed * np.sin(np.radians(angle)) * self.trajectory.delta_t
            x_i += dx
            y_i += dy
            x_a += dx
            y_a += dy
        x_ideal[-1] = x_i
        y_ideal[-1] = y_i
        x_actual[-1] = x_a
        y_actual[-1] = y_a
        return (x_ideal,y_ideal,x_actual,y_actual)

        # state.phase = 4
        # state.omega = 0
        # state.alpha=0
        # target_distance = state.distance + 100.0
        # while state.distance < target_distance:
        #     state.update()
        #     self.path_points.append(copy.copy(state))

    def calculate(self, profile_type: ProfileType, params: TurnParameters, startx, starty, loop_interval):
        profile = Trapezoid()
        if profile_type == ProfileType.QUADRATIC:
            profile = Quadratic()
        elif profile_type == ProfileType.SINUSOID:
            profile = Sinusoid()
        elif profile_type == ProfileType.FULL_SINUSOID:
            profile = FullSinusoid()
        elif profile_type == ProfileType.CUBIC:
            profile = Cubic()
        else:
            profile = Trapezoid()
        self.trajectory.set_profiler(profile)
        params.speed = params.max_speed
        self.trajectory.set_params(params)
        self.trajectory.set_start_xy(startx,starty)
        self.trajectory.calculate()
        # remember turn exit point
        self.calculate_leadout()
        self.update()
        return

    def get_turn_acceleration(self, profile_type: ProfileType, params: TurnParameters):
        acc = 0
        if profile_type == ProfileType.TRAPEZOID:
            acc = params.max_speed * params.max_speed / params.arc_radius
        elif profile_type == ProfileType.QUADRATIC:
            acc = params.max_speed * params.max_speed / params.arc_radius
        elif profile_type == ProfileType.SINUSOID:
            acc = params.max_speed * params.max_speed / params.arc_radius
        elif profile_type == ProfileType.CUBIC:
            acc = 6 * params.max_speed * params.max_speed * math.radians(params.angle) / 4 / params.cubic_length

        return acc
