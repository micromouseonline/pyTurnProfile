# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pyturnprofile.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from pgwidget import PGWidget


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(840, 820)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(840, 820))
        MainWindow.setMaximumSize(QtCore.QSize(840, 820))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pathView = QtWidgets.QGraphicsView(self.centralwidget)
        self.pathView.setGeometry(QtCore.QRect(420, 30, 400, 400))
        self.pathView.setAutoFillBackground(True)
        self.pathView.setObjectName("pathView")
        self.lblPathView = QtWidgets.QLabel(self.centralwidget)
        self.lblPathView.setGeometry(QtCore.QRect(420, 10, 400, 20))
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.lblPathView.setFont(font)
        self.lblPathView.setObjectName("lblPathView")
        self.lblDataView = QtWidgets.QLabel(self.centralwidget)
        self.lblDataView.setGeometry(QtCore.QRect(10, 10, 390, 20))
        self.lblDataView.setObjectName("lblDataView")
        self.lblStartY = QtWidgets.QLabel(self.centralwidget)
        self.lblStartY.setGeometry(QtCore.QRect(740, 460, 62, 16))
        self.lblStartY.setObjectName("lblStartY")
        self.lblStartX = QtWidgets.QLabel(self.centralwidget)
        self.lblStartX.setGeometry(QtCore.QRect(690, 460, 62, 16))
        self.lblStartX.setObjectName("lblStartX")
        self.btnRefresh = QtWidgets.QPushButton(self.centralwidget)
        self.btnRefresh.setGeometry(QtCore.QRect(690, 530, 60, 28))
        self.btnRefresh.setObjectName("btnRefresh")
        self.btnReset = QtWidgets.QPushButton(self.centralwidget)
        self.btnReset.setGeometry(QtCore.QRect(760, 530, 60, 28))
        self.btnReset.setObjectName("btnReset")
        self.startYSpinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.startYSpinBox.setGeometry(QtCore.QRect(760, 480, 60, 25))
        self.startYSpinBox.setMinimum(-270)
        self.startYSpinBox.setMaximum(270)
        self.startYSpinBox.setObjectName("startYSpinBox")
        self.startXSpinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.startXSpinBox.setGeometry(QtCore.QRect(690, 480, 60, 25))
        self.startXSpinBox.setMinimum(-90)
        self.startXSpinBox.setMaximum(90)
        self.startXSpinBox.setObjectName("startXSpinBox")
        self.progressSlider = QtWidgets.QSlider(self.centralwidget)
        self.progressSlider.setGeometry(QtCore.QRect(420, 440, 400, 10))
        self.progressSlider.setOrientation(QtCore.Qt.Horizontal)
        self.progressSlider.setObjectName("progressSlider")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(10, 480, 240, 321))
        font = QtGui.QFont()
        font.setFamily("Ubuntu Mono")
        font.setPointSize(11)
        self.textEdit.setFont(font)
        self.textEdit.setObjectName("textEdit")
        self.gbSpinners = QtWidgets.QGroupBox(self.centralwidget)
        self.gbSpinners.setGeometry(QtCore.QRect(260, 460, 144, 341))
        self.gbSpinners.setObjectName("gbSpinners")
        self.gridLayout = QtWidgets.QGridLayout(self.gbSpinners)
        self.gridLayout.setObjectName("gridLayout")
        self.lblSensors = QtWidgets.QLabel(self.gbSpinners)
        self.lblSensors.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblSensors.setObjectName("lblSensors")
        self.gridLayout.addWidget(self.lblSensors, 5, 0, 1, 1)
        self.lblDelta = QtWidgets.QLabel(self.gbSpinners)
        self.lblDelta.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblDelta.setObjectName("lblDelta")
        self.gridLayout.addWidget(self.lblDelta, 3, 0, 1, 1)
        self.accelerationSpinBox = QtWidgets.QSpinBox(self.gbSpinners)
        self.accelerationSpinBox.setFrame(True)
        self.accelerationSpinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.accelerationSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.accelerationSpinBox.setMinimum(1000)
        self.accelerationSpinBox.setMaximum(70000)
        self.accelerationSpinBox.setSingleStep(100)
        self.accelerationSpinBox.setProperty("value", 9800)
        self.accelerationSpinBox.setObjectName("accelerationSpinBox")
        self.gridLayout.addWidget(self.accelerationSpinBox, 1, 1, 1, 1)
        self.offsetSpinBox = QtWidgets.QSpinBox(self.gbSpinners)
        self.offsetSpinBox.setFrame(True)
        self.offsetSpinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.offsetSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.offsetSpinBox.setMinimum(-270)
        self.offsetSpinBox.setMaximum(270)
        self.offsetSpinBox.setObjectName("offsetSpinBox")
        self.gridLayout.addWidget(self.offsetSpinBox, 4, 1, 1, 1)
        self.lblSpeed = QtWidgets.QLabel(self.gbSpinners)
        self.lblSpeed.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblSpeed.setObjectName("lblSpeed")
        self.gridLayout.addWidget(self.lblSpeed, 0, 0, 1, 1)
        self.slipSpinBox = QtWidgets.QSpinBox(self.gbSpinners)
        self.slipSpinBox.setToolTip("")
        self.slipSpinBox.setFrame(True)
        self.slipSpinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.slipSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.slipSpinBox.setMinimum(0)
        self.slipSpinBox.setMaximum(50)
        self.slipSpinBox.setObjectName("slipSpinBox")
        self.gridLayout.addWidget(self.slipSpinBox, 7, 1, 1, 1)
        self.turnSpeedSpinBox = QtWidgets.QSpinBox(self.gbSpinners)
        self.turnSpeedSpinBox.setFrame(True)
        self.turnSpeedSpinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.turnSpeedSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.turnSpeedSpinBox.setMinimum(100)
        self.turnSpeedSpinBox.setMaximum(3000)
        self.turnSpeedSpinBox.setSingleStep(10)
        self.turnSpeedSpinBox.setProperty("value", 1000)
        self.turnSpeedSpinBox.setObjectName("turnSpeedSpinBox")
        self.gridLayout.addWidget(self.turnSpeedSpinBox, 0, 1, 1, 1)
        self.radiusSpinBox = QtWidgets.QSpinBox(self.gbSpinners)
        self.radiusSpinBox.setFrame(True)
        self.radiusSpinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.radiusSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.radiusSpinBox.setMinimum(15)
        self.radiusSpinBox.setMaximum(270)
        self.radiusSpinBox.setProperty("value", 90)
        self.radiusSpinBox.setObjectName("radiusSpinBox")
        self.gridLayout.addWidget(self.radiusSpinBox, 2, 1, 1, 1)
        self.deltaSpinBox = QtWidgets.QSpinBox(self.gbSpinners)
        self.deltaSpinBox.setFrame(True)
        self.deltaSpinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.deltaSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.deltaSpinBox.setMinimum(5)
        self.deltaSpinBox.setMaximum(200)
        self.deltaSpinBox.setProperty("value", 50)
        self.deltaSpinBox.setObjectName("deltaSpinBox")
        self.gridLayout.addWidget(self.deltaSpinBox, 3, 1, 1, 1)
        self.lblAcc = QtWidgets.QLabel(self.gbSpinners)
        self.lblAcc.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblAcc.setObjectName("lblAcc")
        self.gridLayout.addWidget(self.lblAcc, 1, 0, 1, 1)
        self.lblLength = QtWidgets.QLabel(self.gbSpinners)
        self.lblLength.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblLength.setObjectName("lblLength")
        self.gridLayout.addWidget(self.lblLength, 6, 0, 1, 1)
        self.cubicLengthSpinBox = QtWidgets.QSpinBox(self.gbSpinners)
        self.cubicLengthSpinBox.setFrame(True)
        self.cubicLengthSpinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.cubicLengthSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.cubicLengthSpinBox.setMinimum(50)
        self.cubicLengthSpinBox.setMaximum(500)
        self.cubicLengthSpinBox.setProperty("value", 100)
        self.cubicLengthSpinBox.setObjectName("cubicLengthSpinBox")
        self.gridLayout.addWidget(self.cubicLengthSpinBox, 6, 1, 1, 1)
        self.sensorAngleSpinBox = QtWidgets.QSpinBox(self.gbSpinners)
        self.sensorAngleSpinBox.setFrame(True)
        self.sensorAngleSpinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.sensorAngleSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.sensorAngleSpinBox.setMinimum(0)
        self.sensorAngleSpinBox.setMaximum(90)
        self.sensorAngleSpinBox.setProperty("value", 35)
        self.sensorAngleSpinBox.setObjectName("sensorAngleSpinBox")
        self.gridLayout.addWidget(self.sensorAngleSpinBox, 5, 1, 1, 1)
        self.lblRadius = QtWidgets.QLabel(self.gbSpinners)
        self.lblRadius.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblRadius.setObjectName("lblRadius")
        self.gridLayout.addWidget(self.lblRadius, 2, 0, 1, 1)
        self.lblOffset = QtWidgets.QLabel(self.gbSpinners)
        self.lblOffset.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblOffset.setObjectName("lblOffset")
        self.gridLayout.addWidget(self.lblOffset, 4, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 8, 0, 1, 1)
        self.lblSlip = QtWidgets.QLabel(self.gbSpinners)
        self.lblSlip.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblSlip.setObjectName("lblSlip")
        self.gridLayout.addWidget(self.lblSlip, 7, 0, 1, 1)
        self.gbTurnType = QtWidgets.QGroupBox(self.centralwidget)
        self.gbTurnType.setGeometry(QtCore.QRect(419, 460, 124, 341))
        self.gbTurnType.setObjectName("gbTurnType")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.gbTurnType)
        self.verticalLayout_2.setContentsMargins(15, -1, -1, -1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.rbSS90F = QtWidgets.QRadioButton(self.gbTurnType)
        self.rbSS90F.setObjectName("rbSS90F")
        self.verticalLayout_2.addWidget(self.rbSS90F)
        self.rbSS180 = QtWidgets.QRadioButton(self.gbTurnType)
        self.rbSS180.setObjectName("rbSS180")
        self.verticalLayout_2.addWidget(self.rbSS180)
        self.rbSD45 = QtWidgets.QRadioButton(self.gbTurnType)
        self.rbSD45.setObjectName("rbSD45")
        self.verticalLayout_2.addWidget(self.rbSD45)
        self.rbSD135 = QtWidgets.QRadioButton(self.gbTurnType)
        self.rbSD135.setObjectName("rbSD135")
        self.verticalLayout_2.addWidget(self.rbSD135)
        self.rbDS45 = QtWidgets.QRadioButton(self.gbTurnType)
        self.rbDS45.setObjectName("rbDS45")
        self.verticalLayout_2.addWidget(self.rbDS45)
        self.rbDS135 = QtWidgets.QRadioButton(self.gbTurnType)
        self.rbDS135.setObjectName("rbDS135")
        self.verticalLayout_2.addWidget(self.rbDS135)
        self.rbDD90 = QtWidgets.QRadioButton(self.gbTurnType)
        self.rbDD90.setObjectName("rbDD90")
        self.verticalLayout_2.addWidget(self.rbDD90)
        self.rbSS90E = QtWidgets.QRadioButton(self.gbTurnType)
        self.rbSS90E.setObjectName("rbSS90E")
        self.verticalLayout_2.addWidget(self.rbSS90E)
        self.rbDD90K = QtWidgets.QRadioButton(self.gbTurnType)
        self.rbDD90K.setObjectName("rbDD90K")
        self.verticalLayout_2.addWidget(self.rbDD90K)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.gbTurnProfile = QtWidgets.QGroupBox(self.centralwidget)
        self.gbTurnProfile.setGeometry(QtCore.QRect(550, 460, 131, 181))
        self.gbTurnProfile.setObjectName("gbTurnProfile")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.gbTurnProfile)
        self.verticalLayout.setObjectName("verticalLayout")
        self.rbTrapezoid = QtWidgets.QRadioButton(self.gbTurnProfile)
        self.rbTrapezoid.setObjectName("rbTrapezoid")
        self.verticalLayout.addWidget(self.rbTrapezoid)
        self.rbSinusoid = QtWidgets.QRadioButton(self.gbTurnProfile)
        self.rbSinusoid.setObjectName("rbSinusoid")
        self.verticalLayout.addWidget(self.rbSinusoid)
        self.rbFullSine = QtWidgets.QRadioButton(self.gbTurnProfile)
        self.rbFullSine.setObjectName("rbFullSine")
        self.verticalLayout.addWidget(self.rbFullSine)
        self.rbQuadratic = QtWidgets.QRadioButton(self.gbTurnProfile)
        self.rbQuadratic.setObjectName("rbQuadratic")
        self.verticalLayout.addWidget(self.rbQuadratic)
        self.rbCubic = QtWidgets.QRadioButton(self.gbTurnProfile)
        self.rbCubic.setObjectName("rbCubic")
        self.verticalLayout.addWidget(self.rbCubic)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 460, 131, 16))
        self.label.setObjectName("label")
        self.mpl_widget = PGWidget(self.centralwidget)
        self.mpl_widget.setGeometry(QtCore.QRect(10, 30, 401, 401))
        self.mpl_widget.setObjectName("mpl_widget")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lblPathView.setText(_translate("MainWindow", "Path"))
        self.lblDataView.setText(_translate("MainWindow", "Turn Profile"))
        self.lblStartY.setText(_translate("MainWindow", "Start Y"))
        self.lblStartX.setText(_translate("MainWindow", "Start X"))
        self.btnRefresh.setText(_translate("MainWindow", "Refresh"))
        self.btnReset.setText(_translate("MainWindow", "Reset"))
        self.textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu Mono\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.gbSpinners.setTitle(_translate("MainWindow", "Parameters"))
        self.lblSensors.setText(_translate("MainWindow", "Sensors:"))
        self.lblDelta.setText(_translate("MainWindow", "Delta"))
        self.lblSpeed.setText(_translate("MainWindow", "Speed:"))
        self.lblAcc.setText(_translate("MainWindow", "Acc:"))
        self.lblLength.setText(_translate("MainWindow", "Length:"))
        self.lblRadius.setText(_translate("MainWindow", "Radius:"))
        self.lblOffset.setText(_translate("MainWindow", "Offset:"))
        self.lblSlip.setText(_translate("MainWindow", "Slip"))
        self.gbTurnType.setTitle(_translate("MainWindow", "Turn Type"))
        self.rbSS90F.setText(_translate("MainWindow", "SS90F"))
        self.rbSS180.setText(_translate("MainWindow", "SS180"))
        self.rbSD45.setText(_translate("MainWindow", "SD45"))
        self.rbSD135.setText(_translate("MainWindow", "SD135"))
        self.rbDS45.setText(_translate("MainWindow", "DS45"))
        self.rbDS135.setText(_translate("MainWindow", "DS135"))
        self.rbDD90.setText(_translate("MainWindow", "DD90"))
        self.rbSS90E.setText(_translate("MainWindow", "SS90E"))
        self.rbDD90K.setText(_translate("MainWindow", "DD90K"))
        self.gbTurnProfile.setTitle(_translate("MainWindow", "Profile Type"))
        self.rbTrapezoid.setText(_translate("MainWindow", "Trapezoidal"))
        self.rbSinusoid.setText(_translate("MainWindow", "Sinusoidal"))
        self.rbFullSine.setText(_translate("MainWindow", "Full Sinusoid"))
        self.rbQuadratic.setText(_translate("MainWindow", "Quadratic"))
        self.rbCubic.setText(_translate("MainWindow", "Cubic Spiral"))
        self.label.setText(_translate("MainWindow", "Turn Summary"))
