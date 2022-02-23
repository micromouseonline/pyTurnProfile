import math

from PyQt5.QtCore import QRectF, Qt, QPointF
from PyQt5.QtGui import QPen, QColor
from PyQt5.QtWidgets import QGraphicsItem

from pose import Pose


class Robot(QGraphicsItem):
    def __init__(self):
        super().__init__()
        self.pose = Pose()
        self.width = 80
        self.radius = 37
        self.side_sensor_angle = 35
        self.front_sensor_angle = 80

    def set_sensor_angle(self, angle):
        self.side_sensor_angle = angle
        self.update()
        pass

    def set_pose(self, pose):
        self.pose = pose
        self.setRotation(pose.theta)
        self.setPos(pose.x, pose.y)

    def set_heading(self, degrees):
        self.pose.theta = degrees
        self.set_heading(self.pose.x, self.pose.y)

    def boundingRect(self):
        return QRectF(-160, -160, 320, 200)

    def draw_wheels(self, painter):
        pen = QPen()
        pen.setWidthF(6)
        pen.setColor(QColor(255, 255, 255, 220))
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        painter.drawLine(-self.radius, -24, -self.radius, -6)
        painter.drawLine(-self.radius, 4, -self.radius, 22)
        painter.drawLine(self.radius, -24, self.radius, -6)
        painter.drawLine(self.radius, 4, self.radius, 22)

    def draw_sensor(self, painter, origin, angle, length):
        half_angle = 3
        cos_ray = length * math.cos(math.radians(angle - half_angle))
        sin_ray = length * math.sin(math.radians(angle - half_angle))
        painter.drawLine(origin, origin + QPointF(cos_ray, -sin_ray))

        cos_ray = length * math.cos(math.radians(angle))
        sin_ray = length * math.sin(math.radians(angle))
        painter.drawLine(origin, origin + QPointF(cos_ray, -sin_ray))

        cos_ray = length * math.cos(math.radians(angle + half_angle))
        sin_ray = length * math.sin(math.radians(angle + half_angle))
        painter.drawLine(origin, origin + QPointF(cos_ray, -sin_ray))
        pass

    def paint(self, painter, option, widget):
        pen = QPen()
        pen.setWidth(2)
        pen.setColor(Qt.cyan)
        painter.setPen(pen)
        painter.drawEllipse(-10, -10, 20, 20)
        painter.drawLine(0, 0, 0, -20)
        # BODY
        wheel_width = 8
        left_outer = -self.width // 2
        left_inner = left_outer + wheel_width + 2
        right_outer = self.width // 2
        right_inner = right_outer - wheel_width - 2
        recess_offs = 32
        # front arc
        painter.drawArc(left_outer, -recess_offs - self.width // 2, self.width, self.width, 0, 180 * 16)
        # wheel step left
        painter.drawLine(left_outer, -recess_offs, left_inner, -recess_offs)
        # wheel step right
        painter.drawLine(right_outer, -recess_offs, right_inner, -recess_offs)
        # wheel well left side
        painter.drawLine(left_inner, -recess_offs, left_inner, recess_offs)
        # wheel well right side
        painter.drawLine(right_inner, -recess_offs, right_inner, recess_offs)
        # rear edge
        painter.drawLine(left_inner, recess_offs, right_inner, recess_offs)
        # SENSORS
        pen.setColor(Qt.green)
        painter.setPen(pen)
        painter.setPen(QColor(0, 255, 0, 192))
        # side sensors
        sensor_origin = QPointF(12, -55)
        self.draw_sensor(painter, sensor_origin, self.side_sensor_angle, 160)
        sensor_origin = QPointF(-12, -55)
        self.draw_sensor(painter, sensor_origin, 180 - self.side_sensor_angle, 160)
        # front sensors
        sensor_origin = QPointF(30, -37)
        self.draw_sensor(painter, sensor_origin, self.front_sensor_angle, 120)
        sensor_origin = QPointF(-30, -37)
        self.draw_sensor(painter, sensor_origin, 180 - self.front_sensor_angle, 120)
        self.draw_wheels(painter)
