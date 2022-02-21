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


class Track(QGraphicsItem):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.track_points = []
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
        return len(self.track_points)

    def get_state_at(self, index):
        if index >= self.path_count():
            index = self.path_count() - 1
        if index < 0:
            index = 0
        return self.track_points[index]

    def get_pose_at(self, index):
        state = self.get_state_at(index)
        return state.get_pose()

    def paint(self, painter, option, widget):
        if len(self.track_points) == 0:
            return
        colors = [Qt.magenta, Qt.green, Qt.red, Qt.yellow, Qt.cyan, Qt.magenta]
        pen = QPen(Qt.white)
        pen.setWidthF(2.0)
        painter.setPen(pen)
        rect = QRectF(self.min_x, self.min_y, self.max_x - self.min_x, self.max_y - self.min_y)
        # rect.adjust(5,5,-5,-5)
        # painter.drawRect(rect)
        for i in range(0, len(self.track_points), 5):
            state = self.track_points[i]
            pen.setColor(colors[state.phase])
            painter.setPen(pen)
            rect = QRectF(state.x, state.y, 1.0, 1.0)
            painter.drawEllipse(rect)
            # painter.drawEllipse(int(state.x - 1), int(state.y - 1), 1, 1)

    def calculate_trapezoid(self):
        self.turnRadius  # need to be able to pass in all the required parameters
        pass

    def calculate_sinusoid(self):
        pass

    def calculate_quadratic(self):
        pass

    def calculate_cubic(self):
        pass

    def calculate_leadout(self):
        print(self.turn_end)
        state = self.track_points[self.turn_end-1]
        state.phase = 4
        target_distance = state.distance + 100.0
        while state.distance < target_distance:
            state.update()
            self.track_points.append(copy.copy(state))

    def calculate(self, profile_type: ProfileType, params: TurnParameters, startx, starty):
        self.track_points.clear()
        state = RobotState()
        state.set_interval(0.001)
        state.x = startx
        state.y = starty
        state.speed = params.speed
        state.theta = params.startAngle
        self.track_points.append(copy.copy(state))

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
            self.track_points.append(copy.copy(state))
        state.omega = 0
        state.update()
        self.track_points.append(copy.copy(state))
        self.turn_end = len(self.track_points)
        for i in range(100):
            state.update()
            self.track_points.append(copy.copy(state))

        # self.calculate_leadout()
        self.update()
