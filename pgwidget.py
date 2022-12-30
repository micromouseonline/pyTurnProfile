from PyQt5.QtWidgets import *

import pyqtgraph as pg


palette = ("#101418", "#c00000", "#c000c0", "#c06000", "#00c000", "#0072c3", "#6fdc8c", "#d2a106")

class PGWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        title_style = {'color': 'cyan', 'size': '12px'}
        label_styles = {'verSpacing':-10,'labelTextSize': '10px'}
        hline_style = {'border-style': 'solid', 'border-color': 'green', 'bottom_margin': '50px'}

        w = pg.GraphicsLayoutWidget()     
        p00 = w.addPlot(row=0, col=0)     
        p00.setTitle("wheel speed (m/s)",**title_style)
        p00.setYRange(0, 3.5)
        
        p01 = w.addPlot(row=0, col=1)     
        p01.setTitle("centr'l acc (m/s/s)",**title_style)
        p01.setYRange(0, 70)
        
        p10 = w.addPlot(row=1, col=0)     
        p10.setTitle("omega (deg/s)",**title_style)
        p10.setYRange(0,1500)
        

        p11 = w.addPlot(row=1, col=1)     
        p11.setTitle("alpha (m/s/s)",**title_style)
        p11.setYRange(-60, 60)
        
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(w)

        self.setLayout(vertical_layout)

        pg.setConfigOption('background', pg.mkColor(25, 50, 75))
        pg.setConfigOption('background', palette[0])
        pg.setConfigOption('foreground', 'y')
        pg.setConfigOptions(antialias=True)
        self.axes = [p00,p01,p10,p11]
        for ax in self.axes:
            # ax.addLegend(offset=(-2, 2),**label_styles)
            ax.showGrid(x=True, y=True)
        

