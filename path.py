import copy
import math
from enum import Enum

from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QPen, QBrush
from PyQt5.QtCore import (Qt)
from PyQt5.QtWidgets import QGraphicsItem

from parameters import TurnParameters
from robot_state import RobotState


class ProfileType(Enum):
    TRAPEZOID = 1
    SINUSOID = 2
    QUADRATIC = 3
    CUBIC = 4


class Path(QGraphicsItem):

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

    def boundingRect(self):
        return QRectF(-100.0, -100.0, 600.0, 600.0)

    def path_count(self):
        return len(self.path_points)

    def get_state_at(self, index):
        if index >= self.path_count():
            index = self.path_count() - 1
        if index < 0:
            index = 0
        return self.path_points[index]

    def get_pose_at(self, index):
        state = self.get_state_at(index)
        return state.get_pose()

    def get_max_acceleration(self):
        max_acc = 0
        for state in self.path_points[:self.turn_end]:
            if state.acceleration > max_acc:
                max_acc = state.acceleration
        return max_acc

    def get_max_alpha(self):
        max_alpha = 0
        for state in self.path_points[:self.turn_end]:
            if state.alpha > max_alpha:
                max_alpha = state.alpha
        return max_alpha

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
        pen = QPen(Qt.white)
        pen.setWidthF(2.0)
        painter.setPen(pen)
        for i in range(0, len(self.path_points), 5):
            state = self.path_points[i]
            pen.setColor(colors[state.phase])
            painter.setPen(pen)
            rect = QRectF(state.x, state.y, 1.0, 1.0)
            painter.drawEllipse(rect)

    def calculate_trapezoid(self, params: TurnParameters, startx, starty, loop_interval):
        self.path_points.clear()
        state = RobotState()
        state.set_interval(loop_interval)
        state.x = startx
        state.y = starty
        state.speed = params.speed
        state.theta = params.startAngle
        self.path_points.append(copy.copy(state))

        end_angle = params.startAngle + params.angle
        arc_omega = math.degrees(params.speed / params.radius)
        transition_angle = params.delta * arc_omega / (2.0 * params.speed)
        arc_angle = params.angle - 2 * transition_angle
        arc_length = params.speed * arc_angle / arc_omega
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
        state.omega = 0
        state.update()
        self.path_points.append(copy.copy(state))
        self.turn_end = len(self.path_points)
        for i in range(100):
            state.update()
            self.path_points.append(copy.copy(state))

        # self.calculate_leadout()
        self.update()

    def calculate_sinusoid(self, params: TurnParameters, startx, starty, loop_interval):
        self.path_points.clear()
        state = RobotState()
        state.set_interval(loop_interval)
        state.x = startx
        state.y = starty
        state.speed = params.speed
        state.theta = params.startAngle
        self.path_points.append(copy.copy(state))

        end_angle = params.startAngle + params.angle
        arc_omega = math.degrees(params.speed / params.radius)
        transition_angle = params.delta * 2 * arc_omega / (math.pi * params.speed)
        arc_angle = params.angle - 2 * transition_angle
        arc_length = params.speed * arc_angle / arc_omega
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
        state.omega = 0
        state.update()
        self.path_points.append(copy.copy(state))
        self.turn_end = len(self.path_points)
        for i in range(100):
            state.update()
            self.path_points.append(copy.copy(state))

        # self.calculate_leadout()
        self.update()
        pass

    def calculate_quadratic(self, params: TurnParameters, startx, starty, loop_interval):
        self.path_points.clear()
        state = RobotState()
        state.set_interval(loop_interval)
        state.x = startx
        state.y = starty
        state.speed = params.speed
        state.theta = params.startAngle
        self.path_points.append(copy.copy(state))

        end_angle = params.startAngle + params.angle
        arc_omega = math.degrees(params.speed / params.radius)
        transition_angle = params.delta * 2 * arc_omega / (3.0 * params.speed)
        arc_angle = params.angle - 2 * transition_angle
        arc_length = params.speed * arc_angle / arc_omega
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
        state.omega = 0
        state.update()
        self.path_points.append(copy.copy(state))
        self.turn_end = len(self.path_points)
        for i in range(100):
            state.update()
            self.path_points.append(copy.copy(state))

        # self.calculate_leadout()
        self.update()

    def calculate_cubic(self, params: TurnParameters, startx, starty, loop_interval):
        self.path_points.clear()
        state = RobotState()
        state.set_interval(loop_interval)
        state.x = startx
        state.y = starty
        state.speed = params.speed
        state.theta = params.startAngle
        state.phase = 0
        self.path_points.append(copy.copy(state))

        turn_distance = params.length
        turn_gamma = params.gamma
        turn_speed = params.speed
        turn_angle = params.angle
        k = 6.0 * turn_angle / (turn_distance * turn_distance * turn_distance)

        while state.distance < turn_distance:
            t = state.distance / turn_distance
            #  calculate the speed change if used
            q = 4.0 * turn_gamma * (t - 1) * t + turn_gamma + 1
            state.speed = turn_speed * q
            # now the angular velocity
            omega = state.speed * k * state.distance * (turn_distance - state.distance)
            state.omega = omega
            if t < 0.5:
                state.phase = 1
            else:
                state.phase = 3
            state.update()
            self.path_points.append(copy.copy(state))
        state.omega = 0
        state.update()
        self.path_points.append(copy.copy(state))
        self.turn_end = len(self.path_points)
        for i in range(100):
            state.update()
            self.path_points.append(copy.copy(state))

        # self.calculate_leadout()
        self.update()

    def calculate_leadout(self):
        print(self.turn_end)
        state = self.path_points[self.turn_end - 1]
        state.phase = 4
        target_distance = state.distance + 100.0
        while state.distance < target_distance:
            state.update()
            self.path_points.append(copy.copy(state))

    def calculate(self, profile_type: ProfileType, params: TurnParameters, startx, starty, loop_interval):
        if profile_type == ProfileType.QUADRATIC:
            self.calculate_quadratic(params, startx, starty, loop_interval)
        elif profile_type == ProfileType.SINUSOID:
            self.calculate_sinusoid(params, startx, starty, loop_interval)
        elif profile_type == ProfileType.CUBIC:
            self.calculate_cubic(params, startx, starty, loop_interval)
        else:
            self.calculate_trapezoid(params, startx, starty, loop_interval)
        return

    def get_turn_acceleration(self, profile_type: ProfileType, params: TurnParameters):
        acc = 0
        if profile_type == ProfileType.TRAPEZOID:
            acc = params.speed * params.speed / params.radius
        elif profile_type == ProfileType.QUADRATIC:
            acc = params.speed * params.speed / params.radius
        elif profile_type == ProfileType.SINUSOID:
            acc = params.speed * params.speed / params.radius
        elif profile_type == ProfileType.CUBIC:
            acc = 6 * params.speed * params.speed * math.radians(params.angle) / 4 / params.length

        return acc
