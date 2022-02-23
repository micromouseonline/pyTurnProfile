import math
import time
from background import Background
from parameters import TurnParameters, default_params
from pose import Pose
from robot import Robot
from path import Path, ProfileType
from ui_pyturnprofile import Ui_MainWindow

import random
import numpy as np
from mplwidget import MplWidget
from PyQt5.QtCore import (Qt, QObject)
from PyQt5.QtGui import QBrush, QPainter, QIcon
from PyQt5.QtWidgets import (QWidget, QApplication, QMainWindow, QGraphicsScene)

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

        self.loop_interval = 0.001

        # these will be needed as references to the plotted data
        self.plot_ref_omega = None
        self.plot_ref_speed = None
        self.plot_ref_left_wheel = None
        self.plot_ref_right_wheel = None

        # these get sensible values at te end of the initialisation
        self.current_params = -1
        self.current_profile = -1

        # connect everything up
        self.ui.deltaSpinBox.valueChanged.connect(self.set_delta)
        self.ui.cubicLengthSpinBox.valueChanged.connect(self.set_length)
        self.ui.gammaSpinBox.valueChanged.connect(self.set_gamma)
        self.ui.offsetSpinBox.valueChanged.connect(self.set_offset)

        self.ui.turnSpeedSpinBox.valueChanged.connect(self.set_speed)
        self.ui.radiusSpinBox.valueChanged.connect(self.set_radius)
        self.ui.accelerationSpinBox.valueChanged.connect(self.set_acceleration)

        # self.ui.progressSlider.valueChanged.connect(self.re_calculate)
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

        # path progress slider
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
        params = None
        if self.ui.rbSS90F.isChecked():
            params = default_params['SS90F']
        elif self.ui.rbSS180.isChecked():
            params = default_params['SS180']
        elif self.ui.rbSD45.isChecked():
            params = default_params['SD45']
        elif self.ui.rbSD135.isChecked():
            params = default_params['SD135']
        elif self.ui.rbDS45.isChecked():
            params = default_params['DS45']
        elif self.ui.rbDS135.isChecked():
            params = default_params['DS135']
        elif self.ui.rbDD90.isChecked():
            params = default_params['DD90']
        elif self.ui.rbSS90E.isChecked():
            params = default_params['SS90E']
        elif self.ui.rbDD90K.isChecked():
            params = default_params['DD90K']
        else:
            return
        self.set_parameters(params)
        self.set_safely(self.ui.progressSlider, 0)
        self.re_calculate()

    # another grouped radio button event
    def set_profile_type(self, checked):
        if not checked:
            return
        old_profile = self.current_profile
        if self.ui.rbTrapezoid.isChecked():
            self.current_profile = ProfileType.TRAPEZOID
            self.ui.deltaSpinBox.setEnabled(True)
            self.ui.radiusSpinBox.setEnabled(True)
            self.ui.cubicLengthSpinBox.setEnabled(False)
            self.ui.gammaSpinBox.setEnabled(False)
        elif self.ui.rbSinusoid.isChecked():
            self.current_profile = ProfileType.SINUSOID
            self.ui.deltaSpinBox.setEnabled(True)
            self.ui.radiusSpinBox.setEnabled(True)
            self.ui.cubicLengthSpinBox.setEnabled(False)
            self.ui.gammaSpinBox.setEnabled(False)
        elif self.ui.rbQuadratic.isChecked():
            self.current_profile = ProfileType.QUADRATIC
            self.ui.deltaSpinBox.setEnabled(True)
            self.ui.radiusSpinBox.setEnabled(True)
            self.ui.cubicLengthSpinBox.setEnabled(False)
            self.ui.gammaSpinBox.setEnabled(False)
        elif self.ui.rbCubic.isChecked():
            self.current_profile = ProfileType.CUBIC
            self.ui.deltaSpinBox.setEnabled(False)
            self.ui.radiusSpinBox.setEnabled(False)
            self.ui.cubicLengthSpinBox.setEnabled(True)
            self.ui.gammaSpinBox.setEnabled(True)
        if self.current_profile == old_profile:
            return

        # force recalculation of the spinners
        self.set_speed(self.current_params.speed)
        self.ui.progressSlider.setValue(0)
        self.re_calculate()

    def set_speed(self, speed):
        '''Available for all turn types. For segmented turns it uses the new
        value and the radius to set the turn acceleration. For the Cubic spiral
        turn it uses the length of the turn.

        :param speed: The speed throughout the turn
        :return: modifies acceleration
        '''
        self.current_params.speed = speed
        acceleration = self.path.get_turn_acceleration(self.current_profile, self.current_params)
        self.set_safely(self.ui.accelerationSpinBox, int(acceleration))
        self.re_calculate()

    def set_radius(self, radius):
        '''Only available for the segmented turn types. Uses the new value
        and the speed to set the turn acceleration

        :param radius: The radius of the central portion of the turn
        :return: modifies acceleration
        '''
        self.current_params.radius = radius
        acceleration = self.path.get_turn_acceleration(self.current_profile, self.current_params)
        self.set_safely(self.ui.accelerationSpinBox,int(acceleration))
        self.re_calculate()

    def set_length(self, length):
        '''Only available used for the cubic spiral turn.
        Uses the value and the speed to calculate the new max acceleration

        :param length: The length of the cubic spiral path
        :return: Nothing
        '''
        self.current_params.length = length
        acceleration = self.path.get_turn_acceleration(self.current_profile, self.current_params)
        self.set_safely(self.ui.accelerationSpinBox, int(acceleration))
        self.set_safely(self.ui.cubicLengthSpinBox, int(length))
        self.re_calculate()

    def set_gamma(self, gamma):
        self.current_params.gamma = gamma / 100.0
        self.re_calculate()

    def set_acceleration(self, acceleration):
        self.current_params.acceleration = acceleration
        radius = self.ui.radiusSpinBox.value()
        speed = math.sqrt(acceleration * radius)
        self.current_params.speed = speed
        self.set_safely(self.ui.turnSpeedSpinBox,int(speed))
        self.re_calculate()

    def set_delta(self, delta):
        self.current_params.delta = delta
        self.re_calculate()

    def set_offset(self, offset):
        self.current_params.offset = offset
        pivot_x = self.current_params.pivot_x
        pivot_y = self.current_params.pivot_y
        start_angle = self.current_params.startAngle
        start_x = pivot_x + offset * math.cos(math.pi / 2 + math.radians(start_angle))
        start_y = pivot_y + offset * math.sin(math.pi / 2 + math.radians(start_angle))
        self.robot.set_pose(Pose(start_x, start_y, start_angle))

        self.set_safely(self.ui.startYSpinBox, int(start_y))
        self.set_safely(self.ui.startXSpinBox, int(start_x))
        self.set_safely(self.ui.offsetSpinBox, int(offset))

        self.re_calculate()

    def set_safely(self, widget: QWidget, value):
        '''Locks a widget while updating its value
        '''
        widget.blockSignals(True)
        widget.setValue(value)
        widget.blockSignals(False)

    def set_parameters(self, params: TurnParameters):
        speed_now = self.ui.turnSpeedSpinBox.value()
        self.current_params = params
        self.set_safely(self.ui.radiusSpinBox, int(params.radius))
        self.set_safely(self.ui.deltaSpinBox, int(params.delta))
        self.set_safely(self.ui.cubicLengthSpinBox, int(params.length))
        self.set_safely(self.ui.gammaSpinBox, int(params.gamma))

        self.set_offset(params.offset)
        self.set_speed(speed_now)
        self.re_calculate()

    def set_path_position(self):
        i = self.ui.progressSlider.value()
        state = self.path.get_state_at(i)
        pose = self.path.get_pose_at(i)
        self.robot.set_pose(pose)
        str = f"{int(state.distance):4d} [{int(pose.x):4d},{int(pose.y):4d}] @ {pose.theta:4.1f} deg {state.omega:.2f} deg/s"
        self.ui.lblPathView.setText(str)

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

    def show_summary(self):
        max_alpha = self.path.get_max_alpha()
        wheel_acc = self.robot.radius * math.radians(max_alpha)
        exit_state = self.path.get_state_at(self.path.turn_end - 1)
        self.ui.textEdit.clear()
        self.ui.textEdit.append(f"   Min. Radius: {self.ui.radiusSpinBox.value():5.0f} mm")
        self.ui.textEdit.append(f"    Turn Speed: {self.ui.turnSpeedSpinBox.value():5.0f} mm/s")
        self.ui.textEdit.append(f"Cent'l Accel'n: {self.path.get_max_acceleration():5.0f} mm/s/s")
        self.ui.textEdit.append(f" Wheel Accel'n: {wheel_acc:5.0f} mm/s/s")
        self.ui.textEdit.append(f"         Alpha: {max_alpha:5.0f} deg/s/s")
        self.ui.textEdit.append(f"     Max omega: {self.path.get_max_omega():5.0f} deg/s")
        self.ui.textEdit.append(f"        Exit X: {exit_state.x:5.1f} mm")
        self.ui.textEdit.append(f"        Exit Y: {exit_state.y:5.1f} mm")
        self.ui.textEdit.append(f"    Exit Speed: {exit_state.speed:5.0f} mm/s")
        self.ui.textEdit.append(f"    Exit Angle: {exit_state.theta:5.1f} deg")
        self.ui.textEdit.append(f"      Distance: {exit_state.distance:5.0f} deg")
        self.ui.textEdit.append(f"          Time: {exit_state.time:5.3f} sec")
        self.ui.textEdit.append("")

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
        self.ui.mpl_widget.axes[0].set_ylim(0, 4000)
        self.ui.mpl_widget.axes[0].set_ylabel('speed (mm/s)', color='b')
        self.ui.mpl_widget.axes[1].set_ylim(0, 2000)
        self.ui.mpl_widget.axes[1].set_ylabel('Angular Velocity (deg/s)', color='g')
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

        # use the entire path including the leadout
        path = self.path.path_points[:-1]
        path_time = [s.time for s in path]
        omega = np.array([s.omega for s in path])
        speed = np.array([s.speed for s in path])
        left_speed = speed + self.robot.radius * np.radians(omega)
        right_speed = speed - self.robot.radius * np.radians(omega)

        self.ui.mpl_widget.canvas.axes.plot(path_time, omega * 2, 'g')
        self.ui.mpl_widget.canvas.axes.plot(path_time, speed, 'b', linestyle='dotted')
        self.ui.mpl_widget.canvas.axes.plot(path_time, left_speed, 'b', linestyle='solid')
        self.ui.mpl_widget.canvas.axes.plot(path_time, right_speed, 'b', linestyle='solid')

        #  this call is VERY slow. everything else takes about 3ms. This takes 30ms!
        ## consider using pyqtgraph
        self.ui.mpl_widget.canvas.draw()

    def re_calculate(self):

        start_x = self.ui.startXSpinBox.value()
        start_y = self.ui.startYSpinBox.value()

        # recalculate the path
        self.path.calculate(self.current_profile, self.current_params, start_x, start_y, self.loop_interval)
        self.ui.progressSlider.setMinimum(0)
        self.ui.progressSlider.setMaximum(self.path.turn_end)
        i = self.ui.progressSlider.value()
        self.robot.set_pose(self.path.get_pose_at(i))
        state = self.path.get_state_at(i)
        pose = self.path.get_pose_at(i)
        str = f"{int(state.distance):4d} [{int(pose.x):4d},{int(pose.y):4d}] @ {int(pose.theta):4d} deg {state.omega:.2f} deg/s"
        self.ui.lblPathView.setText(str)

        self.plot_data()
        self.show_summary()

        global calc_count
        calc_count += 1


# ============================================================================#

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('pyTurnProfiler.png'))
    window = AppWindow()
    window.setWindowTitle("PyQt Micromouse Turn Simulator")

    window.show()
    sys.exit(app.exec_())
