from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib as mpl


class MplWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)

        SMALL_SIZE = 8
        MEDIUM_SIZE = 10
        BIGGER_SIZE = 12

        mpl.rc('font', size=SMALL_SIZE)
        mpl.rc('axes', titlesize=SMALL_SIZE)
        mpl.rc('axes', labelsize=SMALL_SIZE)
        mpl.rc('xtick', labelsize=SMALL_SIZE)
        mpl.rc('ytick', labelsize=SMALL_SIZE)
        mpl.rc('legend', fontsize=SMALL_SIZE)
        mpl.rc('figure', titlesize=MEDIUM_SIZE)

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        # vertical_layout.addWidget(NavigationToolbar(self.canvas, self))

        self.canvas.axes = self.canvas.figure.add_subplot()
        # self.canvas.axes.grid('both')
        # self.canvas.axes.set_ylabel('left')
        # self.canvas.axes.set_ylim(-1, 1)
        self.canvas.axes.set_xlim(0, 10)
        self.canvas.axes.set_xlabel('Time (seconds)')
        #

        self.axes = [self.canvas.axes, self.canvas.axes.twinx()]

        # self.axes[0].tick_params(axis='y', colors='g')
        # self.axes[0].set_xlabel('Time (seconds)')
        self.decorate_plot()
        self.setLayout(vertical_layout)

    def decorate_plot(self):
        '''
        Pretties up the plot. Sets spines, ticks, labels
        :return: nothing
        '''
        self.figure.subplots_adjust(left=0.15)
        self.figure.subplots_adjust(right=0.85)
        self.figure.subplots_adjust(top=0.9)
        self.axes[0].set_xlabel('Time (seconds)')
        self.axes[0].spines['top'].set_visible(False)
        self.axes[1].spines['top'].set_visible(False)
        self.axes[1].set_frame_on(True)
        self.axes[1].patch.set_visible(False)
        self.axes[0].set_frame_on(True)
        self.axes[0].patch.set_visible(False)
        self.axes[0].set_ylim(0, 4000)
        self.axes[0].set_ylabel('speed (mm/s)', color='b')
        self.axes[1].set_ylim(0, 2000)
        self.axes[1].set_ylabel('Angular Velocity (deg/s)', color='g')
        self.axes[0].set_xlim(xmin=0, xmax=0.6, auto=False)
        self.canvas.axes.grid('both')