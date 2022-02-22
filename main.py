import math

from background import Background
from parameters import TurnParameters, default_params
from pose import Pose
from robot import Robot
from path import Path, ProfileType
from ui_pyturnprofile import Ui_MainWindow

import random
import numpy as np
from mplwidget import MplWidget
from PyQt5.QtCore import (Qt)
from PyQt5.QtGui import QBrush, QPainter, QIcon
from PyQt5.QtWidgets import (QApplication, QMainWindow, QGraphicsScene)

draw_count = 0
calc_count = 0


# ============================================================================#

class AppWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.do_not_repaint = True
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.path_scene = QGraphicsScene()
        self.path_scene.setSceneRect(-100, -100, 380, 380)
        self.path_scene.setBackgroundBrush(QBrush(Qt.black, Qt.SolidPattern))
        self.ui.pathView.setRenderHint(QPainter.Antialiasing)
        self.ui.pathView.setScene(self.path_scene)
        self.path_scene.addItem(Background())
        self.robot = Robot()
        self.path_scene.addItem(self.robot)
        self.path = Path()
        self.path_scene.addItem(self.path)

        # these get sensible values at te end of the initialisation
        self.current_params = -1
        self.current_profile = -1

        # connect everything up
        self.ui.deltaSpinBox.valueChanged.connect(self.set_delta)
        self.ui.cubicLengthSpinBox.valueChanged.connect(self.re_calculate)
        self.ui.gammaSpinBox.valueChanged.connect(self.re_calculate)
        self.ui.offsetSpinBox.valueChanged.connect(self.set_offset)

        self.ui.turnSpeedSpinBox.valueChanged.connect(self.set_speed)
        self.ui.radiusSpinBox.valueChanged.connect(self.set_radius)
        self.ui.accelerationSpinBox.valueChanged.connect(self.set_acceleration)

        self.ui.progressSlider.valueChanged.connect(self.re_calculate)
        # # turn type selectors
        self.ui.rbSS90F.toggled.connect(self.set_turn_type)
        self.ui.rbSS180.toggled.connect(self.set_turn_type)
        self.ui.rbSD45.toggled.connect(self.set_turn_type)
        self.ui.rbSD135.toggled.connect(self.set_turn_type)
        self.ui.rbDS45.toggled.connect(self.set_turn_type)
        self.ui.rbDS135.toggled.connect(self.set_turn_type)
        self.ui.rbDD90.toggled.connect(self.set_turn_type)
        self.ui.rbSS90E.toggled.connect(self.set_turn_type)
        self.ui.rbDD90K.toggled.connect(self.set_turn_type)

        # # profile type selectors
        self.ui.rbTrapezoid.toggled.connect(self.set_profile_type)
        self.ui.rbSinusoid.toggled.connect(self.set_profile_type)
        self.ui.rbQuadratic.toggled.connect(self.set_profile_type)
        self.ui.rbCubic.toggled.connect(self.set_profile_type)

        self.ui.startXSpinBox.valueChanged.connect(self.set_xy)
        self.ui.startYSpinBox.valueChanged.connect(self.set_xy)

        # path rogress slider
        self.ui.progressSlider.valueChanged.connect(self.set_path_position)

        # robot sensor geometry
        self.ui.sensorAngleSpinBox.valueChanged.connect(self.set_robot_sensors)

        # preselect the turn type
        self.ui.rbSS90F.click()
        self.current_params.speed = self.ui.turnSpeedSpinBox.value()
        # and the profile
        self.ui.rbTrapezoid.blockSignals(False)
        self.ui.rbTrapezoid.click()
        self.ui.rbTrapezoid.blockSignals(False)

    # called from toggle event for a radio button in
    # a group so there will be two calls - one for the button
    # that is being unchecked and one for the button that is
    # being checked. We only care about the one that is now checked
    def set_turn_type(self, checked):
        if not checked:
            return
        if self.ui.rbSS90F.isChecked():
            self.current_params = default_params['SS90F']
        elif self.ui.rbSS180.isChecked():
            self.current_params = default_params['SS180']
        elif self.ui.rbSD45.isChecked():
            self.current_params = default_params['SD45']
        elif self.ui.rbSD135.isChecked():
            self.current_params = default_params['SD135']
        elif self.ui.rbDS45.isChecked():
            self.current_params = default_params['DS45']
        elif self.ui.rbDS135.isChecked():
            self.current_params = default_params['DS135']
        elif self.ui.rbDD90.isChecked():
            self.current_params = default_params['DD90']
        elif self.ui.rbSS90E.isChecked():
            self.current_params = default_params['SS90E']
        elif self.ui.rbDD90K.isChecked():
            self.current_params = default_params['DD90K']
        self.set_parameters(self.current_params)
        self.current_params.speed = self.ui.turnSpeedSpinBox.value()
        self.ui.progressSlider.blockSignals(True)
        self.ui.progressSlider.setValue(0)
        self.ui.progressSlider.blockSignals(False)
        self.re_calculate()

    # another grouped radio button event
    def set_profile_type(self, checked):
        if not checked:
            return
        old_profile = self.current_profile
        if self.ui.rbTrapezoid.isChecked():
            self.current_profile = ProfileType.TRAPEZOID
            self.ui.cubicLengthSpinBox.setEnabled(False)
            self.ui.gammaSpinBox.setEnabled(False)
        elif self.ui.rbSinusoid.isChecked():
            self.current_profile = ProfileType.SINUSOID
            self.ui.cubicLengthSpinBox.setEnabled(False)
            self.ui.gammaSpinBox.setEnabled(False)
        elif self.ui.rbQuadratic.isChecked():
            self.current_profile = ProfileType.QUADRATIC
            self.ui.cubicLengthSpinBox.setEnabled(False)
            self.ui.gammaSpinBox.setEnabled(False)
        elif self.ui.rbCubic.isChecked():
            self.current_profile = ProfileType.CUBIC
            self.ui.cubicLengthSpinBox.setEnabled(True)
            self.ui.gammaSpinBox.setEnabled(True)
        if self.current_profile == old_profile:
            return
        # print(self.current_profile)
        self.ui.progressSlider.setValue(0)
        self.re_calculate()

    def set_speed(self, speed):
        self.current_params.speed = speed
        acceleration = speed * speed / self.ui.radiusSpinBox.value()
        self.ui.accelerationSpinBox.blockSignals(True)
        self.ui.accelerationSpinBox.setValue(int(acceleration))
        self.ui.accelerationSpinBox.blockSignals(False)
        self.re_calculate()

    def set_radius(self, radius):
        self.current_params.radius = radius
        speed = self.ui.turnSpeedSpinBox.value()
        acceleration = speed * speed / radius
        self.ui.accelerationSpinBox.blockSignals(True)
        self.ui.accelerationSpinBox.setValue(int(acceleration))
        self.ui.accelerationSpinBox.blockSignals(False)
        self.re_calculate()

    def set_acceleration(self, acceleration):
        self.current_params.acceleration = acceleration
        radius = self.ui.radiusSpinBox.value()
        speed = math.sqrt(acceleration * radius)
        self.current_params.speed = speed
        self.ui.turnSpeedSpinBox.blockSignals(True)
        self.ui.turnSpeedSpinBox.setValue(int(speed))
        self.ui.turnSpeedSpinBox.blockSignals(False)
        self.re_calculate()

    def set_delta(self, delta):
        self.current_params.delta = delta
        self.re_calculate()

    def set_offset(self, offset):
        self.current_params.offs = offset
        pivot_x = self.current_params.pivot_x
        pivot_y = self.current_params.pivot_y
        start_angle = self.current_params.startAngle
        start_x = pivot_x + offset * math.cos(math.pi / 2 + math.radians(start_angle))
        start_y = pivot_y + offset * math.sin(math.pi / 2 + math.radians(start_angle))
        self.robot.set_pose(Pose(start_x, start_y, start_angle))

        self.ui.startXSpinBox.blockSignals(True)
        self.ui.startXSpinBox.setValue(int(start_x))
        self.ui.startXSpinBox.blockSignals(False)

        self.ui.startYSpinBox.blockSignals(True)
        self.ui.startYSpinBox.setValue(int(start_y))
        self.ui.startYSpinBox.blockSignals(False)

        self.re_calculate()

    def set_parameters(self, params: TurnParameters):
        self.ui.radiusSpinBox.blockSignals(True)
        self.ui.radiusSpinBox.setValue(params.radius)
        self.ui.radiusSpinBox.blockSignals(False)

        self.ui.deltaSpinBox.blockSignals(True)
        self.ui.deltaSpinBox.setValue(params.delta)
        self.ui.deltaSpinBox.blockSignals(False)

        self.ui.cubicLengthSpinBox.blockSignals(True)
        self.ui.cubicLengthSpinBox.setValue(params.length)
        self.ui.cubicLengthSpinBox.blockSignals(False)

        self.ui.offsetSpinBox.setValue(params.offs)
        self.re_calculate()

    # this is probably redundant
    def set_path_position(self):
        self.re_calculate()
        i = self.ui.progressSlider.value()
        state = self.path.get_state_at(i)
        print(i, state)

    def set_xy(self):
        start_x = self.ui.startXSpinBox.value()
        start_y = self.ui.startYSpinBox.value()
        angle = self.robot.pose.theta
        self.robot.set_pose(Pose(start_x, start_y, angle))
        self.re_calculate()
        pass

    def set_robot_sensors(self):
        angle = self.ui.sensorAngleSpinBox.value()
        self.robot.set_sensor_angle(angle)

    def decorate_plot(self):
        '''
        Pretties up the plot. Sets spines, ticks, labels
        :return: nothing
        '''
        self.ui.mpl_widget.figure.subplots_adjust(left=0.15)
        self.ui.mpl_widget.figure.subplots_adjust(right=0.85)
        self.ui.mpl_widget.figure.subplots_adjust(top=0.9)
        self.ui.mpl_widget.axes[0].set_xlabel('Time (seconds)')
        self.ui.mpl_widget.axes[0].spines['top'].set_visible(False)
        self.ui.mpl_widget.axes[1].spines['top'].set_visible(False)
        self.ui.mpl_widget.axes[1].set_frame_on(True)
        self.ui.mpl_widget.axes[1].patch.set_visible(False)
        self.ui.mpl_widget.axes[0].set_frame_on(True)
        self.ui.mpl_widget.axes[0].patch.set_visible(False)
        self.ui.mpl_widget.axes[0].set_ylim(0, 3000)
        self.ui.mpl_widget.axes[0].set_ylabel('speed (mm/s)', color='b')
        self.ui.mpl_widget.axes[1].set_ylim(0, 1500)
        self.ui.mpl_widget.axes[1].set_ylabel('Angle (deg) and Angular Velocity (deg/s)', color='g')
        self.ui.mpl_widget.axes[0].set_xlim(xmin=0, xmax=0.6, auto=False)
        self.ui.mpl_widget.canvas.axes.grid('both')

    def plot_data(self):
        '''
        Plot the angular velocity and wheel speeds. Uses a brute-force, redraw
        everything approach just because it is easier to write.
        If better performance is needed, consider preparing the plot once
        and just updating the data used.
        :return: Nothing
        '''
        self.ui.mpl_widget.canvas.axes.clear()
        self.decorate_plot()

        path = self.path.path_points[:-1]
        time = [s.time for s in path]
        angular_velocity = np.array([s.omega for s in path])
        self.ui.mpl_widget.canvas.axes.plot(time, angular_velocity * 2, 'b')
        v = np.array([s.speed for s in path])
        self.ui.mpl_widget.canvas.axes.plot(time, v, 'g-.')

        np_omega = np.array([math.radians(s.omega) for s in path])
        np_speed = np.array([s.speed for s in path])
        np_left_speed = np_speed + 37 * np_omega
        np_right_speed = np_speed - 37 * np_omega
        self.ui.mpl_widget.canvas.axes.plot(time, np_left_speed, 'b', linestyle='dotted')
        self.ui.mpl_widget.canvas.axes.plot(time, np_right_speed, 'b', linestyle='dotted')

        self.ui.mpl_widget.canvas.draw()

    def re_calculate(self):
        start_x = self.ui.startXSpinBox.value()
        start_y = self.ui.startYSpinBox.value()
        # self.set_offset(self.current_params.offs)

        # recalculate the path
        self.path.calculate(self.current_profile, self.current_params, start_x, start_y)
        self.ui.progressSlider.setMinimum(0)
        self.ui.progressSlider.setMaximum(self.path.turn_end)
        i = self.ui.progressSlider.value()
        self.robot.set_pose(self.path.get_pose_at(i))
        state = self.path.get_state_at(i)
        pose = self.path.get_pose_at(i)
        str = f"{int(state.distance):4d} [{int(pose.x):4d},{int(pose.y):4d}] @ {int(pose.theta):4d} deg {state.omega:.2f} deg/s"
        self.ui.lblPathView.setText(str)

        self.plot_data()

        global calc_count
        calc_count += 1
        self.ui.textEdit.append(f"recalc - {self.path.path_count():4d} [{calc_count}] {int(state.x)},{int(state.y)} @ {state.theta:.1f}")


# ============================================================================#

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('pyTurnProfiler.png'))
    window = AppWindow()
    window.setWindowTitle("PyQt Micromouse Turn Simulator")

    window.show()
    sys.exit(app.exec_())
