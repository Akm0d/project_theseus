# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt_graphics.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        MainWindow.resize(372, 472)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.keypad = QtWidgets.QWidget(self.centralwidget)
        self.keypad.setGeometry(QtCore.QRect(0, 50, 361, 131))
        self.keypad.setFocusPolicy(QtCore.Qt.NoFocus)
        self.keypad.setObjectName("keypad")
        self.gridLayoutWidget = QtWidgets.QWidget(self.keypad)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 340, 112))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton4 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton4.setObjectName("pushButton4")
        self.gridLayout.addWidget(self.pushButton4, 1, 0, 1, 1)
        self.pushButton7 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton7.setObjectName("pushButton7")
        self.gridLayout.addWidget(self.pushButton7, 1, 3, 1, 1)
        self.pushButton0 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton0.setObjectName("pushButton0")
        self.gridLayout.addWidget(self.pushButton0, 0, 0, 1, 1)
        self.pushButton6 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton6.setObjectName("pushButton6")
        self.gridLayout.addWidget(self.pushButton6, 1, 2, 1, 1)
        self.pushButton8 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton8.setObjectName("pushButton8")
        self.gridLayout.addWidget(self.pushButton8, 2, 0, 1, 1)
        self.pushButton2 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton2.setObjectName("pushButton2")
        self.gridLayout.addWidget(self.pushButton2, 0, 2, 1, 1)
        self.pushButton3 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton3.setObjectName("pushButton3")
        self.gridLayout.addWidget(self.pushButton3, 0, 3, 1, 1)
        self.pushButton9 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton9.setObjectName("pushButton9")
        self.gridLayout.addWidget(self.pushButton9, 2, 1, 1, 1)
        self.pushButtona = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButtona.setObjectName("pushButtona")
        self.gridLayout.addWidget(self.pushButtona, 2, 2, 1, 1)
        self.pushButtonb = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButtonb.setObjectName("pushButtonb")
        self.gridLayout.addWidget(self.pushButtonb, 2, 3, 1, 1)
        self.pushButton1 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton1.setObjectName("pushButton1")
        self.gridLayout.addWidget(self.pushButton1, 0, 1, 1, 1)
        self.pushButton5 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton5.setObjectName("pushButton5")
        self.gridLayout.addWidget(self.pushButton5, 1, 1, 1, 1)
        self.pushButtonc = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButtonc.setObjectName("pushButtonc")
        self.gridLayout.addWidget(self.pushButtonc, 3, 0, 1, 1)
        self.pushButtond = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButtond.setObjectName("pushButtond")
        self.gridLayout.addWidget(self.pushButtond, 3, 1, 1, 1)
        self.pushButtone = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButtone.setObjectName("pushButtone")
        self.gridLayout.addWidget(self.pushButtone, 3, 2, 1, 1)
        self.pushButtonf = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButtonf.setObjectName("pushButtonf")
        self.gridLayout.addWidget(self.pushButtonf, 3, 3, 1, 1)
        self.puzzle = QtWidgets.QWidget(self.centralwidget)
        self.puzzle.setGeometry(QtCore.QRect(20, 310, 131, 51))
        self.puzzle.setObjectName("puzzle")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.puzzle)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 10, 121, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalSlider_1 = QtWidgets.QSlider(self.horizontalLayoutWidget)
        self.verticalSlider_1.setMaximum(1)
        self.verticalSlider_1.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_1.setObjectName("verticalSlider_1")
        self.horizontalLayout.addWidget(self.verticalSlider_1)
        self.verticalSlider_2 = QtWidgets.QSlider(self.horizontalLayoutWidget)
        self.verticalSlider_2.setMaximum(1)
        self.verticalSlider_2.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_2.setObjectName("verticalSlider_2")
        self.horizontalLayout.addWidget(self.verticalSlider_2)
        self.verticalSlider_3 = QtWidgets.QSlider(self.horizontalLayoutWidget)
        self.verticalSlider_3.setMaximum(1)
        self.verticalSlider_3.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_3.setObjectName("verticalSlider_3")
        self.horizontalLayout.addWidget(self.verticalSlider_3)
        self.verticalSlider_4 = QtWidgets.QSlider(self.horizontalLayoutWidget)
        self.verticalSlider_4.setMaximum(1)
        self.verticalSlider_4.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_4.setObjectName("verticalSlider_4")
        self.horizontalLayout.addWidget(self.verticalSlider_4)
        self.verticalSlider_5 = QtWidgets.QSlider(self.horizontalLayoutWidget)
        self.verticalSlider_5.setMaximum(1)
        self.verticalSlider_5.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_5.setObjectName("verticalSlider_5")
        self.horizontalLayout.addWidget(self.verticalSlider_5)
        self.LEDs = QtWidgets.QWidget(self.centralwidget)
        self.LEDs.setGeometry(QtCore.QRect(10, 180, 291, 51))
        self.LEDs.setFocusPolicy(QtCore.Qt.NoFocus)
        self.LEDs.setObjectName("LEDs")
        self.label_2 = QtWidgets.QLabel(self.LEDs)
        self.label_2.setGeometry(QtCore.QRect(0, -10, 110, 39))
        self.label_2.setObjectName("label_2")
        self.inner_box = QtWidgets.QWidget(self.centralwidget)
        self.inner_box.setGeometry(QtCore.QRect(0, 250, 251, 51))
        self.inner_box.setObjectName("inner_box")
        self.horizontalLayoutWidget_4 = QtWidgets.QWidget(self.inner_box)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(10, 10, 236, 31))
        self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.wire_red = QtWidgets.QCheckBox(self.horizontalLayoutWidget_4)
        self.wire_red.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.wire_red.setChecked(True)
        self.wire_red.setObjectName("wire_red")
        self.horizontalLayout_4.addWidget(self.wire_red)
        self.wire_green = QtWidgets.QCheckBox(self.horizontalLayoutWidget_4)
        self.wire_green.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.wire_green.setChecked(True)
        self.wire_green.setObjectName("wire_green")
        self.horizontalLayout_4.addWidget(self.wire_green)
        self.wire_blue = QtWidgets.QCheckBox(self.horizontalLayoutWidget_4)
        self.wire_blue.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.wire_blue.setChecked(True)
        self.wire_blue.setObjectName("wire_blue")
        self.horizontalLayout_4.addWidget(self.wire_blue)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.solenoid = QtWidgets.QCheckBox(self.horizontalLayoutWidget_4)
        self.solenoid.setFocusPolicy(QtCore.Qt.NoFocus)
        self.solenoid.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.solenoid.setCheckable(False)
        self.solenoid.setChecked(False)
        self.solenoid.setObjectName("solenoid")
        self.horizontalLayout_4.addWidget(self.solenoid)
        self.laser_tripwires = QtWidgets.QWidget(self.centralwidget)
        self.laser_tripwires.setGeometry(QtCore.QRect(260, 270, 91, 151))
        self.laser_tripwires.setObjectName("laser_tripwires")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.laser_tripwires)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(10, 10, 81, 138))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.laser_2 = QtWidgets.QCheckBox(self.gridLayoutWidget_2)
        self.laser_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.laser_2.setText("")
        self.laser_2.setCheckable(False)
        self.laser_2.setChecked(False)
        self.laser_2.setObjectName("laser_2")
        self.gridLayout_2.addWidget(self.laser_2, 2, 0, 1, 1)
        self.laser_0 = QtWidgets.QCheckBox(self.gridLayoutWidget_2)
        self.laser_0.setFocusPolicy(QtCore.Qt.NoFocus)
        self.laser_0.setText("")
        self.laser_0.setCheckable(False)
        self.laser_0.setChecked(False)
        self.laser_0.setObjectName("laser_0")
        self.gridLayout_2.addWidget(self.laser_0, 0, 0, 1, 1)
        self.laser_4 = QtWidgets.QCheckBox(self.gridLayoutWidget_2)
        self.laser_4.setFocusPolicy(QtCore.Qt.NoFocus)
        self.laser_4.setText("")
        self.laser_4.setCheckable(False)
        self.laser_4.setChecked(False)
        self.laser_4.setObjectName("laser_4")
        self.gridLayout_2.addWidget(self.laser_4, 4, 0, 1, 1)
        self.laser_3 = QtWidgets.QCheckBox(self.gridLayoutWidget_2)
        self.laser_3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.laser_3.setText("")
        self.laser_3.setCheckable(False)
        self.laser_3.setChecked(False)
        self.laser_3.setObjectName("laser_3")
        self.gridLayout_2.addWidget(self.laser_3, 3, 0, 1, 1)
        self.laser_1 = QtWidgets.QCheckBox(self.gridLayoutWidget_2)
        self.laser_1.setFocusPolicy(QtCore.Qt.NoFocus)
        self.laser_1.setText("")
        self.laser_1.setCheckable(False)
        self.laser_1.setChecked(False)
        self.laser_1.setObjectName("laser_1")
        self.gridLayout_2.addWidget(self.laser_1, 1, 0, 1, 1)
        self.laser_5 = QtWidgets.QCheckBox(self.gridLayoutWidget_2)
        self.laser_5.setFocusPolicy(QtCore.Qt.NoFocus)
        self.laser_5.setText("")
        self.laser_5.setCheckable(False)
        self.laser_5.setChecked(False)
        self.laser_5.setObjectName("laser_5")
        self.gridLayout_2.addWidget(self.laser_5, 5, 0, 1, 1)
        self.photodiode_0 = QtWidgets.QCheckBox(self.gridLayoutWidget_2)
        self.photodiode_0.setText("")
        self.photodiode_0.setChecked(True)
        self.photodiode_0.setObjectName("photodiode_0")
        self.gridLayout_2.addWidget(self.photodiode_0, 0, 1, 1, 1)
        self.photodiode_1 = QtWidgets.QCheckBox(self.gridLayoutWidget_2)
        self.photodiode_1.setText("")
        self.photodiode_1.setChecked(True)
        self.photodiode_1.setObjectName("photodiode_1")
        self.gridLayout_2.addWidget(self.photodiode_1, 1, 1, 1, 1)
        self.photodiode_2 = QtWidgets.QCheckBox(self.gridLayoutWidget_2)
        self.photodiode_2.setText("")
        self.photodiode_2.setChecked(True)
        self.photodiode_2.setObjectName("photodiode_2")
        self.gridLayout_2.addWidget(self.photodiode_2, 2, 1, 1, 1)
        self.photodiode_3 = QtWidgets.QCheckBox(self.gridLayoutWidget_2)
        self.photodiode_3.setText("")
        self.photodiode_3.setChecked(True)
        self.photodiode_3.setObjectName("photodiode_3")
        self.gridLayout_2.addWidget(self.photodiode_3, 3, 1, 1, 1)
        self.photodiode_4 = QtWidgets.QCheckBox(self.gridLayoutWidget_2)
        self.photodiode_4.setText("")
        self.photodiode_4.setChecked(True)
        self.photodiode_4.setObjectName("photodiode_4")
        self.gridLayout_2.addWidget(self.photodiode_4, 4, 1, 1, 1)
        self.photodiode_5 = QtWidgets.QCheckBox(self.gridLayoutWidget_2)
        self.photodiode_5.setText("")
        self.photodiode_5.setChecked(True)
        self.photodiode_5.setObjectName("photodiode_5")
        self.gridLayout_2.addWidget(self.photodiode_5, 5, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(270, 250, 121, 16))
        self.label.setObjectName("label")
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(10, 200, 284, 41))
        self.horizontalLayoutWidget_3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.led_0 = QtWidgets.QCheckBox(self.horizontalLayoutWidget_3)
        self.led_0.setFocusPolicy(QtCore.Qt.NoFocus)
        self.led_0.setText("")
        self.led_0.setCheckable(False)
        self.led_0.setChecked(False)
        self.led_0.setObjectName("led_0")
        self.horizontalLayout_3.addWidget(self.led_0)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.led_1 = QtWidgets.QCheckBox(self.horizontalLayoutWidget_3)
        self.led_1.setFocusPolicy(QtCore.Qt.NoFocus)
        self.led_1.setText("")
        self.led_1.setCheckable(False)
        self.led_1.setChecked(False)
        self.led_1.setObjectName("led_1")
        self.horizontalLayout_3.addWidget(self.led_1)
        self.led_2 = QtWidgets.QCheckBox(self.horizontalLayoutWidget_3)
        self.led_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.led_2.setText("")
        self.led_2.setCheckable(False)
        self.led_2.setChecked(False)
        self.led_2.setObjectName("led_2")
        self.horizontalLayout_3.addWidget(self.led_2)
        self.led_3 = QtWidgets.QCheckBox(self.horizontalLayoutWidget_3)
        self.led_3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.led_3.setText("")
        self.led_3.setCheckable(False)
        self.led_3.setChecked(False)
        self.led_3.setObjectName("led_3")
        self.horizontalLayout_3.addWidget(self.led_3)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.led_4 = QtWidgets.QCheckBox(self.horizontalLayoutWidget_3)
        self.led_4.setFocusPolicy(QtCore.Qt.NoFocus)
        self.led_4.setText("")
        self.led_4.setCheckable(False)
        self.led_4.setChecked(False)
        self.led_4.setObjectName("led_4")
        self.horizontalLayout_3.addWidget(self.led_4)
        self.led_5 = QtWidgets.QCheckBox(self.horizontalLayoutWidget_3)
        self.led_5.setFocusPolicy(QtCore.Qt.NoFocus)
        self.led_5.setText("")
        self.led_5.setCheckable(False)
        self.led_5.setChecked(False)
        self.led_5.setObjectName("led_5")
        self.horizontalLayout_3.addWidget(self.led_5)
        self.led_6 = QtWidgets.QCheckBox(self.horizontalLayoutWidget_3)
        self.led_6.setFocusPolicy(QtCore.Qt.NoFocus)
        self.led_6.setText("")
        self.led_6.setCheckable(False)
        self.led_6.setChecked(False)
        self.led_6.setObjectName("led_6")
        self.horizontalLayout_3.addWidget(self.led_6)
        self.led_7 = QtWidgets.QCheckBox(self.horizontalLayoutWidget_3)
        self.led_7.setFocusPolicy(QtCore.Qt.NoFocus)
        self.led_7.setText("")
        self.led_7.setCheckable(False)
        self.led_7.setChecked(False)
        self.led_7.setObjectName("led_7")
        self.horizontalLayout_3.addWidget(self.led_7)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(9, 199, 291, 41))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(10, 0, 301, 51))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.lid_display = QtWidgets.QWidget(self.frame_2)
        self.lid_display.setGeometry(QtCore.QRect(10, 10, 281, 31))
        self.lid_display.setObjectName("lid_display")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.lid_display)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 281, 31))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lcdMinutes = QtWidgets.QLCDNumber(self.horizontalLayoutWidget_2)
        self.lcdMinutes.setAutoFillBackground(False)
        self.lcdMinutes.setSmallDecimalPoint(True)
        self.lcdMinutes.setDigitCount(1)
        self.lcdMinutes.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdMinutes.setProperty("value", 3.0)
        self.lcdMinutes.setProperty("intValue", 3)
        self.lcdMinutes.setObjectName("lcdMinutes")
        self.horizontalLayout_2.addWidget(self.lcdMinutes)
        self.lcdSeconds = QtWidgets.QLCDNumber(self.horizontalLayoutWidget_2)
        self.lcdSeconds.setDigitCount(2)
        self.lcdSeconds.setObjectName("lcdSeconds")
        self.horizontalLayout_2.addWidget(self.lcdSeconds)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.RGB_red = QtWidgets.QRadioButton(self.horizontalLayoutWidget_2)
        self.RGB_red.setFocusPolicy(QtCore.Qt.NoFocus)
        self.RGB_red.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.RGB_red.setCheckable(False)
        self.RGB_red.setObjectName("RGB_red")
        self.horizontalLayout_2.addWidget(self.RGB_red)
        self.RGB_green = QtWidgets.QRadioButton(self.horizontalLayoutWidget_2)
        self.RGB_green.setFocusPolicy(QtCore.Qt.NoFocus)
        self.RGB_green.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.RGB_green.setCheckable(False)
        self.RGB_green.setObjectName("RGB_green")
        self.horizontalLayout_2.addWidget(self.RGB_green)
        self.RGB_blue = QtWidgets.QRadioButton(self.horizontalLayoutWidget_2)
        self.RGB_blue.setFocusPolicy(QtCore.Qt.NoFocus)
        self.RGB_blue.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.RGB_blue.setCheckable(False)
        self.RGB_blue.setObjectName("RGB_blue")
        self.horizontalLayout_2.addWidget(self.RGB_blue)
        self.start_reset = QtWidgets.QPushButton(self.centralwidget)
        self.start_reset.setGeometry(QtCore.QRect(20, 390, 108, 23))
        self.start_reset.setObjectName("start_reset")
        self.dial = QtWidgets.QDial(self.centralwidget)
        self.dial.setGeometry(QtCore.QRect(150, 310, 101, 111))
        self.dial.setMaximum(360)
        self.dial.setWrapping(True)
        self.dial.setObjectName("dial")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 372, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Mock Box"))
        self.pushButton4.setText(_translate("MainWindow", "4"))
        self.pushButton7.setText(_translate("MainWindow", "7"))
        self.pushButton0.setText(_translate("MainWindow", "0"))
        self.pushButton6.setText(_translate("MainWindow", "6"))
        self.pushButton8.setText(_translate("MainWindow", "8"))
        self.pushButton2.setText(_translate("MainWindow", "2"))
        self.pushButton3.setText(_translate("MainWindow", "3"))
        self.pushButton9.setText(_translate("MainWindow", "9"))
        self.pushButtona.setText(_translate("MainWindow", "a"))
        self.pushButtonb.setText(_translate("MainWindow", "b"))
        self.pushButton1.setText(_translate("MainWindow", "1"))
        self.pushButton5.setText(_translate("MainWindow", "5"))
        self.pushButtonc.setText(_translate("MainWindow", "c"))
        self.pushButtond.setText(_translate("MainWindow", "d"))
        self.pushButtone.setText(_translate("MainWindow", "e"))
        self.pushButtonf.setText(_translate("MainWindow", "f"))
        self.label_2.setText(_translate("MainWindow", "Puzzle LEDs"))
        self.wire_red.setText(_translate("MainWindow", "R"))
        self.wire_green.setText(_translate("MainWindow", "G"))
        self.wire_blue.setText(_translate("MainWindow", "B"))
        self.solenoid.setText(_translate("MainWindow", "Solenoid"))
        self.label.setText(_translate("MainWindow", "Tripwires"))
        self.RGB_red.setText(_translate("MainWindow", "R"))
        self.RGB_green.setText(_translate("MainWindow", "G"))
        self.RGB_blue.setText(_translate("MainWindow", "B"))
        self.start_reset.setText(_translate("MainWindow", "Start/Reset"))
