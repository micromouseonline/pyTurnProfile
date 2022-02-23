from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QPen, QColor
from PyQt5.QtWidgets import QGraphicsItem


class Background(QGraphicsItem):
    def __init__(self):
        super().__init__()

    def boundingRect(self):
        return QRectF(0, 0, 360, 360)

    def paint(self, painter, option, widget):
        painter.fillRect(self.boundingRect(),Qt.black)
        wallPen = QPen(QColor(255, 0, 0, 90))
        postPen = QPen(QColor(255, 0, 0, 180))
        linePen = QPen(QColor(255, 0, 0, 90))
        originPen = QPen(QColor(255, 200, 0, 90))
        wallPen.setWidthF(12.0)
        wallPen.setJoinStyle(Qt.MiterJoin)
        wallPen.setStyle(Qt.SolidLine)
        postPen.setWidthF(12.0)
        postPen.setJoinStyle(Qt.MiterJoin)
        postPen.setStyle(Qt.SolidLine)
        linePen.setWidthF(2.0)
        linePen.setStyle(Qt.DotLine)
        originPen.setWidthF(2.0)
        originPen.setStyle(Qt.DotLine)

        painter.setPen(wallPen)
        painter.drawLine(-90, -90, -90, 270)
        painter.drawLine(-90, -90, 90, -90)
        painter.drawLine(-90, 270, 270, 270)

        # posts
        painter.setPen(postPen)
        painter.drawLine(270, 90, 270, 91)
        painter.drawLine(270, -90, 270, -91)
        painter.drawLine(90, 90, 90, 91)
        painter.drawLine(90, -90, 90, -91)

        painter.setPen(linePen)
        for i in range(5):
            painter.drawLine(-90 + 90 * i, -90, -90 + 90 * i, 270)
            painter.drawLine(-90, -90 + 90 * i, 270, -90 + 90 * i)

        # all the diagonals
        painter.drawLine(-90, 180, 0, 270)
        painter.drawLine(-90, 90, 90, 270)
        painter.drawLine(-90, 0, 180, 270)
        painter.drawLine(-90, -90, 270, 270)
        painter.drawLine(0, -90, 270, 180)
        painter.drawLine(90, -90, 270, 90)
        painter.drawLine(180, -90, 270, 0)
        painter.drawLine(0, -90, -90, 0)
        painter.drawLine(90, -90, -90, 90)
        painter.drawLine(180, -90, -90, 180)
        painter.drawLine(270, -90, -90, 270)
        painter.drawLine(270, 0, 0, 270)
        painter.drawLine(270, 90, 90, 270)
        painter.drawLine(270, 180, 180, 270)
        # origin
        painter.setPen(originPen)
        painter.drawLine(-90, 0, 270, 0)
        painter.drawLine(0, -90, 0, 270)
        pass