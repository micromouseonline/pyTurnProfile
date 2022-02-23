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

        self.axes = [self.canvas.axes, self.canvas.axes.twinx()]

        self.setLayout(vertical_layout)
