from PyQt5.QtCore import QT_VERSION_STR
import math
import os
import cProfile
import time
from background import Background
from parameters import TurnParameters, default_params
from pose import Pose
from robot import Robot
from path import Path, ProfileType
from trajectory import Trajectory
import profilers
from ui_pyturnprofile import Ui_MainWindow
from time import perf_counter

import random
import numpy as np
from pgwidget import PGWidget
from PyQt5.QtCore import (Qt, QObject)
from PyQt5.QtGui import QBrush, QPainter, QIcon, QFont
from PyQt5.QtWidgets import (
    QWidget, QApplication, QMainWindow, QGraphicsScene)

import pyqtgraph as pg

# this may or may not help with high DPI screen
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

version = list(map(int, QT_VERSION_STR.split('.')))

if version[1] >= 14:
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
if hasattr(Qt, "AA_EnableHighDpiScaling"):
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

if hasattr(Qt, "AA_UseHighDpiPixmaps"):
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

palette = ("#101418", "#c00000", "#c000c0", "#c06000",
           "#00c000", "#0072c3", "#6fdc8c", "#d2a106")

draw_count = 0
calc_count = 0

fps = None
last_time = perf_counter()


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

        # fix up the font in the textEdit box
        font = QFont()
        font.setFamily("Monospace")
        font.setFamily("none")
        font.setPointSizeF(10.0)
        font.setStyleHint(QFont.TypeWriter)
        self.ui.lblPathView.setFont(font)
        self.ui.textEdit.setFont(font)

        # these will be needed as references to the plotted data
        self.plot_ref_omega = None
        self.plot_ref_speed = None
        self.plot_ref_left_wheel = None
        self.plot_ref_right_wheel = None

        # these get sensible values at the end of the initialisation
        self.current_params = None
        self.current_profile = None

        # connect everything up
        self.ui.deltaSpinBox.valueChanged.connect(self.set_delta)
        self.ui.cubicLengthSpinBox.valueChanged.connect(self.set_length)
        self.ui.offsetSpinBox.valueChanged.connect(self.set_offset)

        self.ui.turnSpeedSpinBox.valueChanged.connect(self.set_speed)
        self.ui.radiusSpinBox.valueChanged.connect(self.set_radius)
        self.ui.accelerationSpinBox.valueChanged.connect(self.set_acceleration)
        self.ui.gripSpinBox.valueChanged.connect(self.set_slip)

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
        self.ui.rbFullSine.toggled.connect(self.set_profile_type)
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
        elif self.ui.rbSinusoid.isChecked():
            self.current_profile = ProfileType.SINUSOID
            self.ui.deltaSpinBox.setEnabled(True)
            self.ui.radiusSpinBox.setEnabled(True)
            self.ui.cubicLengthSpinBox.setEnabled(False)
        elif self.ui.rbFullSine.isChecked():
            self.current_profile = ProfileType.FULL_SINUSOID
            self.ui.deltaSpinBox.setEnabled(False)
            self.ui.radiusSpinBox.setEnabled(True)
            self.ui.cubicLengthSpinBox.setEnabled(False)
        elif self.ui.rbQuadratic.isChecked():
            self.current_profile = ProfileType.QUADRATIC
            self.ui.deltaSpinBox.setEnabled(True)
            self.ui.radiusSpinBox.setEnabled(True)
            self.ui.cubicLengthSpinBox.setEnabled(False)
        elif self.ui.rbCubic.isChecked():
            self.current_profile = ProfileType.CUBIC
            self.ui.deltaSpinBox.setEnabled(False)
            self.ui.radiusSpinBox.setEnabled(False)
            self.ui.cubicLengthSpinBox.setEnabled(True)
        if self.current_profile == old_profile:
            return

        # force recalculation of the spinners
        self.set_speed(self.current_params.speed)
        self.set_radius(self.current_params.arc_radius)
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
        self.current_params.arc_radius = radius
        acceleration = self.path.get_turn_acceleration(self.current_profile, self.current_params)
        self.set_safely(self.ui.accelerationSpinBox, int(acceleration))
        if self.ui.rbFullSine.isChecked():
            delta = math.pi * math.radians(self.current_params.angle) * radius / 4.0
            self.ui.deltaSpinBox.setValue(int(delta))
            # self.set(self.ui.deltaSpinBox,int(delta))
        self.re_calculate()

    def set_length(self, length):
        '''Only available used for the cubic spiral turn.
        Uses the value and the speed to calculate the new max acceleration

        :param length: The length of the cubic spiral path
        :return: Nothing
        '''
        self.current_params.cubic_length = length
        acceleration = self.path.get_turn_acceleration(self.current_profile, self.current_params)
        self.set_safely(self.ui.accelerationSpinBox, int(acceleration))
        self.set_safely(self.ui.cubicLengthSpinBox, int(length))
        self.re_calculate()

    def set_slip(self, slip):
        self.current_params.k_grip = slip
        self.re_calculate()

    def set_acceleration(self, acceleration):
        self.current_params.acceleration = acceleration
        radius = self.ui.radiusSpinBox.value()
        speed = math.sqrt(acceleration * radius)
        self.current_params.speed = speed
        self.set_safely(self.ui.turnSpeedSpinBox, int(speed))
        self.re_calculate()

    def set_delta(self, delta):
        self.current_params.delta = delta
        if self.ui.rbFullSine.isChecked():
            radius = int(
                delta * 4.0 / (math.pi * math.radians(self.current_params.angle)))
            self.set_safely(self.ui.radiusSpinBox, radius)
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
        self.set_safely(self.ui.radiusSpinBox, int(params.arc_radius))
        self.set_safely(self.ui.deltaSpinBox, int(params.delta))
        self.set_safely(self.ui.cubicLengthSpinBox, int(params.cubic_length))
        self.set_safely(self.ui.gripSpinBox, int(params.k_grip))

        self.set_offset(params.offset)
        self.set_speed(speed_now)
        self.re_calculate()

    def set_path_position(self):
        i = self.ui.progressSlider.value()
        pose = self.path.get_pose_at(i)
        self.robot.set_pose(pose)
        distance = self.path.trajectory.distance[i]
        omega = self.path.trajectory.omega_ideal[i]
        str = f"{int(distance):4d} [{int(pose.x):4d},{int(pose.y):4d}] @ θ={int(pose.theta):4d} deg ω={omega:.2f} deg/s"
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
        end_x = self.path.trajectory.x_ideal[-1]
        end_y = self.path.trajectory.y_ideal[-1]
        end_theta = self.path.trajectory.theta_ideal[-1]
        end_time = self.path.trajectory.time[-1]
        distance = self.path.trajectory.distance[-1]
        slip_comp_x = self.path.trajectory.x_actual[-1] - self.path.trajectory.x_ideal[-1]
        slip_comp_y = self.path.trajectory.y_actual[-1] - self.path.trajectory.y_ideal[-1]
        self.ui.textEdit.clear()
        self.ui.textEdit.append(f"   Min. Radius: {self.ui.radiusSpinBox.value():5.0f} mm")
        self.ui.textEdit.append(f"    Turn Speed: {self.ui.turnSpeedSpinBox.value():5.0f} mm/s")
        self.ui.textEdit.append(f"Cent'l Accel'n: {self.path.get_max_acceleration():5.0f} mm/s/s")
        self.ui.textEdit.append(f" Wheel Accel'n: {wheel_acc:5.0f} mm/s/s")
        self.ui.textEdit.append(f"     Max alpha: {max_alpha:5.0f} deg/s/s")
        self.ui.textEdit.append(f"     Max omega: {self.path.get_max_omega():5.0f} deg/s")
        self.ui.textEdit.append(f"Profile Exit X: {end_x:5.1f} mm")
        self.ui.textEdit.append(f"Profile Exit Y: {end_y:5.1f} mm")
        self.ui.textEdit.append(f"   Overshoot X: {slip_comp_x:5.1f} mm")
        self.ui.textEdit.append(f"  Undershoot Y: {slip_comp_y:5.1f} mm")
        self.ui.textEdit.append(f"    Exit Speed: {self.path.trajectory.speed:5.0f} mm/s")
        self.ui.textEdit.append(f"    Exit Angle: {end_theta:5.1f} deg")
        self.ui.textEdit.append(f"      Distance: {distance:5.0f} mm")
        self.ui.textEdit.append(f"          Time: {end_time:5.3f} sec")
        self.ui.textEdit.append("")

    def plot(self, x, y, plot_item, plotname, color, line_style=Qt.SolidLine):
        pen = pg.mkPen(color=color, width=3, style=line_style)
        plot_item.plot(x, y, name=plotname, pen=pen)

    def plot_data(self):
        '''
        Plot the angular velocity and wheel speeds. Uses a brute-force, redraw
        everything approach just because it is easier to write.
        If better performance is needed, consider preparing the plot once
        and just updating the data used.
        :return: Nothing

        This is really slow and accounts for most of the time taken and a
        lot of that is just clearing the axes
        '''
        now = perf_counter()
        axes = self.ui.pg_widget.axes
        title_style = {'color': 'cyan', 'size': '12px'}
        interval = self.path.trajectory.delta_t
        path_time = self.path.trajectory.time
        omega = self.path.trajectory.omega_ideal
        beta = self.path.trajectory.beta
        speed = self.path.trajectory.speed
        alpha = self.path.trajectory.alpha
        left_speed = speed + self.robot.radius * np.radians(omega)
        right_speed = speed - self.robot.radius * np.radians(omega)

        # It is more efficient to update the data rather than re-create all the plots
        for p in axes:
            p.clear()

        self.plot(path_time, interval * left_speed, axes[0], "L", palette[3])
        self.plot(path_time, interval * right_speed, axes[0], "R", palette[4])
        # self.plot(path_time, interval * speed * np.radians(omega), axes[1], "R", palette[2])
        self.plot(path_time, beta, axes[1], "R", palette[2])
        self.plot(path_time, interval * alpha, axes[3], 'q', palette[6])
        self.plot(path_time, omega, axes[2], '', palette[5])

        elapsed = perf_counter() - now
        global fps
        if fps is None:
            fps = 1.0 / elapsed
        else:
            f = 1.0 / elapsed
            fps = fps + 0.1 * (f - fps)
        self.setWindowTitle('%0.2f fps' % fps)

    def re_calculate(self):
        start_x = self.ui.startXSpinBox.value()
        start_y = self.ui.startYSpinBox.value()

        # recalculate the path
        self.path.calculate(self.current_profile, self.current_params,
                            start_x, start_y, self.loop_interval)
        self.ui.progressSlider.setMinimum(0)
        self.ui.progressSlider.setMaximum(self.path.trajectory.n_items-1)
        i = self.ui.progressSlider.value()
        self.robot.set_pose(self.path.get_pose_at(i))
        pose = self.path.get_pose_at(i)
        distance = self.path.trajectory.distance[i]
        omega = self.path.trajectory.omega_ideal[i]
        str = f"{int(distance):4d} [{int(pose.x):4d},{int(pose.y):4d}] @ θ={int(pose.theta):4d} deg ω={omega:.2f} deg/s"
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
    # for screen in app.screens():
    #     screen_dpi = screen.logicalDotsPerInch()
    #     print(screen_dpi)
    window.show()
    sys.exit(app.exec_())
