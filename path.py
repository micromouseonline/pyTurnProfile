import copy
import math
from enum import Enum

from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QPen, QBrush
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
        x = self.trajectory.x_ideal[index]
        y = self.trajectory.y_ideal[index]
        theta = self.trajectory.theta_ideal[index]
        return Pose(x,y,theta)


    def get_max_acceleration(self):
        return np.max(np.radians(self.trajectory.omega_ideal) * self.trajectory.speed)

    def get_max_alpha(self):
        return np.max(self.trajectory.alpha)


    def get_max_omega(self):
        max_omega = 0
        for state in self.path_points[:self.turn_end]:
            if state.omega > max_omega:
                max_omega = state.omega
        return max_omega

    def paint(self, painter, option, widget):
        if len(self.path_points) == 0:
            return
        colors = [Qt.magenta, Qt.green, Qt.red, Qt.yellow, Qt.cyan, Qt.magenta]
        colors_ideal = [Qt.magenta, Qt.green, Qt.red, Qt.yellow, Qt.cyan, Qt.magenta]
        colors_actual = [Qt.magenta, Qt.green, Qt.red, Qt.yellow, Qt.cyan, Qt.magenta]
        pen = QPen(Qt.white)
        pen.setWidthF(2.0)
        painter.setPen(pen)
        for i in range(0, self.trajectory.n_items, 5):
            
            # state = self.path_points[i]
            phase = int(self.trajectory.phase[i])
            pen.setColor(colors[phase])
            painter.setPen(pen)
            rect = QRectF(self.trajectory.x_ideal[i], self.trajectory.y_ideal[i], 1.0, 1.0)
            painter.drawEllipse(rect)
            rect = QRectF(self.trajectory.x_actual[i], self.trajectory.y_actual[i], 1.0, 1.0)
            painter.drawEllipse(rect)
            # rect = QRectF(state.x, state.y, 1.0, 1.0)
            # painter.drawEllipse(rect)
    '''
    Tthe profilers get the entire set of omega, theta, phase for the turn
    '''
    def calculate_trapezoid(self, params: TurnParameters, startx, starty, loop_interval):
        self.path_points.clear()
        state = RobotState()
        state.set_interval(loop_interval)
        state.x = startx
        state.y = starty
        state.speed = params.max_speed
        state.theta = params.startAngle
        self.path_points.append(copy.copy(state))

        end_angle = params.startAngle + params.angle
        arc_omega = math.degrees(params.max_speed / params.arc_radius)
        transition_angle = params.delta * arc_omega / (2.0 * params.max_speed)
        arc_angle = params.angle - 2 * transition_angle
        arc_length = params.max_speed * arc_angle / arc_omega
        turn_distance = 2 * params.delta + arc_length

        while state.theta <= end_angle - 0.01:
            if state.theta < params.startAngle + transition_angle:
                state.omega = arc_omega * state.distance / params.delta
                state.phase = 1
            elif state.theta <= (end_angle - transition_angle):
                state.omega = arc_omega
                state.phase = 2
            else:
                state.omega = arc_omega * (turn_distance - state.distance) / params.delta
                state.phase = 3
            state.update()
            self.path_points.append(copy.copy(state))
        self.turn_end = len(self.path_points) - 1
        self.calculate_leadout(state)
        self.update()

    def calculate_sinusoid(self, params: TurnParameters, startx, starty, loop_interval):
        self.path_points.clear()
        state = RobotState()
        state.set_interval(loop_interval)
        state.x = startx
        state.y = starty
        state.speed = params.max_speed
        state.theta = params.startAngle
        self.path_points.append(copy.copy(state))

        end_angle = params.startAngle + params.angle
        arc_omega = math.degrees(params.max_speed / params.arc_radius)
        transition_angle = params.delta * 2 * arc_omega / (math.pi * params.max_speed)
        arc_angle = params.angle - 2 * transition_angle
        arc_length = params.max_speed * arc_angle / arc_omega
        turn_distance = 2 * params.delta + arc_length

        while state.theta <= end_angle - 0.01:
            if state.theta < params.startAngle + transition_angle:
                t = state.distance / params.delta
                state.omega = arc_omega * math.sin(math.pi / 2 * t)
                state.phase = 1
            elif state.theta <= (end_angle - transition_angle):
                state.omega = arc_omega
                state.phase = 2
            else:
                t = (turn_distance - state.distance) / params.delta
                state.omega = arc_omega * math.sin(math.pi / 2 * t)
                state.phase = 3
            state.update()
            self.path_points.append(copy.copy(state))
        self.turn_end = len(self.path_points) - 1
        self.calculate_leadout(state)
        self.update()

    def calculate_full_sinusoid(self, params: TurnParameters, startx, starty, loop_interval):
        self.path_points.clear()
        state = RobotState()
        state.set_interval(loop_interval)
        state.x = startx
        state.y = starty
        state.speed = params.max_speed
        state.theta = params.startAngle
        self.path_points.append(copy.copy(state))
        end_angle = params.startAngle + params.angle
        radius = 4.0*params.delta/(math.pi*math.radians(params.angle))
        arc_omega = math.degrees(params.max_speed / radius)
        turn_distance = 2 * params.delta
        # while state.distance < turn_distance:
        while abs(state.theta - end_angle) > 0.01:
            t = state.distance / turn_distance
            state.omega = arc_omega * math.sin(math.pi * t)
            if state.omega < math.radians(1):
                state.omega = math.radians(1)
            state.phase = 2
            state.update()
            self.path_points.append(copy.copy(state))
        self.turn_end = len(self.path_points) - 1
        self.calculate_leadout(state)
        self.update()

    def calculate_quadratic(self, params: TurnParameters, startx, starty, loop_interval):
        self.path_points.clear()
        state = RobotState()
        state.set_interval(loop_interval)
        state.x = startx
        state.y = starty
        state.speed = params.max_speed
        state.theta = params.startAngle
        self.path_points.append(copy.copy(state))

        end_angle = params.startAngle + params.angle
        arc_omega = math.degrees(params.max_speed / params.arc_radius)
        transition_angle = params.delta * 2 * arc_omega / (3.0 * params.max_speed)
        arc_angle = params.angle - 2 * transition_angle
        arc_length = params.max_speed * arc_angle / arc_omega
        turn_distance = 2 * params.delta + arc_length

        while state.theta <= end_angle - 0.01:
            if state.theta < params.startAngle + transition_angle:
                t = state.distance / params.delta
                state.omega = arc_omega * t * (2.0 - t)
                state.phase = 1
            elif state.theta <= (end_angle - transition_angle):
                state.omega = arc_omega
                state.phase = 2
            else:
                t = (turn_distance - state.distance) / params.delta
                state.omega = arc_omega * t * (2.0 - t)
                state.phase = 3
            state.update()
            self.path_points.append(copy.copy(state))
        self.turn_end = len(self.path_points) - 1
        self.calculate_leadout(state)
        self.update()

    def calculate_cubic(self, params: TurnParameters, startx, starty, loop_interval):
        self.path_points.clear()
        state = RobotState()
        state.set_interval(loop_interval)
        state.x = startx
        state.y = starty
        state.speed = params.max_speed
        state.theta = params.startAngle
        state.phase = 0
        self.path_points.append(copy.copy(state))

        turn_length = params.cubic_length
        turn_speed = params.max_speed
        turn_angle = params.angle
        k = 6.0 * turn_angle / (turn_length * turn_length * turn_length)

        while state.distance < turn_length:
            t = state.distance / turn_length
            # now the angular velocity
            omega = state.speed * k * state.distance * (turn_length - state.distance)
            state.omega = omega
            if t < 0.5:
                state.phase = 1
            else:
                state.phase = 3
            state.update()
            self.path_points.append(copy.copy(state))
        self.turn_end = len(self.path_points) - 1
        self.calculate_leadout(state)
        self.update()

    def calculate_leadout(self, state: RobotState):
        state.phase = 4
        state.omega = 0
        state.alpha=0
        target_distance = state.distance + 100.0
        while state.distance < target_distance:
            state.update()
            self.path_points.append(copy.copy(state))

    def calculate(self, profile_type: ProfileType, params: TurnParameters, startx, starty, loop_interval):
        if profile_type == ProfileType.QUADRATIC:
            self.calculate_quadratic(params, startx, starty, loop_interval)
        elif profile_type == ProfileType.SINUSOID:
            self.calculate_sinusoid(params, startx, starty, loop_interval)
        elif profile_type == ProfileType.FULL_SINUSOID:
            self.calculate_full_sinusoid(params, startx, starty, loop_interval)
        elif profile_type == ProfileType.CUBIC:
            self.calculate_cubic(params, startx, starty, loop_interval)
        else:
            self.calculate_trapezoid(params, startx, starty, loop_interval)   
        params.speed = params.max_speed
        params.k_grip = 200
        self.trajectory.set_params(params)
        self.trajectory.set_start_xy(startx,starty)
        self.trajectory.calculate()
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
