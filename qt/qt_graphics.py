# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt_graphics.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        MainWindow.resize(376, 533)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.ultrasonicSlider = QtWidgets.QSlider(self.centralwidget)
        self.ultrasonicSlider.setOrientation(QtCore.Qt.Horizontal)
        self.ultrasonicSlider.setObjectName("ultrasonicSlider")
        self.gridLayout.addWidget(self.ultrasonicSlider, 1, 0, 1, 1)
        self.widget_2 = QtWidgets.QWidget(self.centralwidget)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.start_reset = QtWidgets.QPushButton(self.widget_2)
        self.start_reset.setObjectName("start_reset")
        self.horizontalLayout_5.addWidget(self.start_reset)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.solenoid = QtWidgets.QCheckBox(self.widget_2)
        self.solenoid.setFocusPolicy(QtCore.Qt.NoFocus)
        self.solenoid.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.solenoid.setCheckable(False)
        self.solenoid.setChecked(False)
        self.solenoid.setObjectName("solenoid")
        self.horizontalLayout_5.addWidget(self.solenoid)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem1)
        self.gridLayout.addWidget(self.widget_2, 5, 0, 1, 1)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridFrame_2 = QtWidgets.QFrame(self.frame)
        self.gridFrame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.gridFrame_2.setObjectName("gridFrame_2")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.gridFrame_2)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.laser_22 = QtWidgets.QCheckBox(self.gridFrame_2)
        self.laser_22.setFocusPolicy(QtCore.Qt.NoFocus)
        self.laser_22.setText("")
        self.laser_22.setCheckable(False)
        self.laser_22.setChecked(False)
        self.laser_22.setObjectName("laser_22")
        self.gridLayout_6.addWidget(self.laser_22, 1, 0, 1, 1)
        self.laser_21 = QtWidgets.QCheckBox(self.gridFrame_2)
        self.laser_21.setFocusPolicy(QtCore.Qt.NoFocus)
        self.laser_21.setText("")
        self.laser_21.setCheckable(False)
        self.laser_21.setChecked(False)
        self.laser_21.setObjectName("laser_21")
        self.gridLayout_6.addWidget(self.laser_21, 4, 0, 1, 1)
        self.photodiode_18 = QtWidgets.QCheckBox(self.gridFrame_2)
        self.photodiode_18.setText("")
        self.photodiode_18.setChecked(True)
        self.photodiode_18.setObjectName("photodiode_18")
        self.gridLayout_6.addWidget(self.photodiode_18, 0, 1, 1, 1)
        self.laser_23 = QtWidgets.QCheckBox(self.gridFrame_2)
        self.laser_23.setFocusPolicy(QtCore.Qt.NoFocus)
        self.laser_23.setText("")
        self.laser_23.setCheckable(False)
        self.laser_23.setChecked(False)
        self.laser_23.setObjectName("laser_23")
        self.gridLayout_6.addWidget(self.laser_23, 5, 0, 1, 1)
        self.laser_19 = QtWidgets.QCheckBox(self.gridFrame_2)
        self.laser_19.setFocusPolicy(QtCore.Qt.NoFocus)
        self.laser_19.setText("")
        self.laser_19.setCheckable(False)
        self.laser_19.setChecked(False)
        self.laser_19.setObjectName("laser_19")
        self.gridLayout_6.addWidget(self.laser_19, 2, 0, 1, 1)
        self.photodiode_20 = QtWidgets.QCheckBox(self.gridFrame_2)
        self.photodiode_20.setText("")
        self.photodiode_20.setChecked(True)
        self.photodiode_20.setObjectName("photodiode_20")
        self.gridLayout_6.addWidget(self.photodiode_20, 2, 1, 1, 1)
        self.photodiode_21 = QtWidgets.QCheckBox(self.gridFrame_2)
        self.photodiode_21.setText("")
        self.photodiode_21.setChecked(True)
        self.photodiode_21.setObjectName("photodiode_21")
        self.gridLayout_6.addWidget(self.photodiode_21, 3, 1, 1, 1)
        self.photodiode_22 = QtWidgets.QCheckBox(self.gridFrame_2)
        self.photodiode_22.setText("")
        self.photodiode_22.setChecked(True)
        self.photodiode_22.setObjectName("photodiode_22")
        self.gridLayout_6.addWidget(self.photodiode_22, 4, 1, 1, 1)
        self.photodiode_23 = QtWidgets.QCheckBox(self.gridFrame_2)
        self.photodiode_23.setText("")
        self.photodiode_23.setChecked(True)
        self.photodiode_23.setObjectName("photodiode_23")
        self.gridLayout_6.addWidget(self.photodiode_23, 5, 1, 1, 1)
        self.laser_18 = QtWidgets.QCheckBox(self.gridFrame_2)
        self.laser_18.setFocusPolicy(QtCore.Qt.NoFocus)
        self.laser_18.setText("")
        self.laser_18.setCheckable(False)
        self.laser_18.setChecked(False)
        self.laser_18.setObjectName("laser_18")
        self.gridLayout_6.addWidget(self.laser_18, 0, 0, 1, 1)
        self.photodiode_19 = QtWidgets.QCheckBox(self.gridFrame_2)
        self.photodiode_19.setText("")
        self.photodiode_19.setChecked(True)
        self.photodiode_19.setObjectName("photodiode_19")
        self.gridLayout_6.addWidget(self.photodiode_19, 1, 1, 1, 1)
        self.laser_20 = QtWidgets.QCheckBox(self.gridFrame_2)
        self.laser_20.setFocusPolicy(QtCore.Qt.NoFocus)
        self.laser_20.setText("")
        self.laser_20.setCheckable(False)
        self.laser_20.setChecked(False)
        self.laser_20.setObjectName("laser_20")
        self.gridLayout_6.addWidget(self.laser_20, 3, 0, 1, 1)
        self.gridLayout_2.addWidget(self.gridFrame_2, 0, 5, 2, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 0, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem3, 1, 1, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem4, 0, 4, 1, 1)
        self.frame_4 = QtWidgets.QFrame(self.frame)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.wire_red = QtWidgets.QCheckBox(self.frame_4)
        self.wire_red.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.wire_red.setChecked(True)
        self.wire_red.setObjectName("wire_red")
        self.horizontalLayout_3.addWidget(self.wire_red)
        self.wire_green = QtWidgets.QCheckBox(self.frame_4)
        self.wire_green.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.wire_green.setChecked(True)
        self.wire_green.setObjectName("wire_green")
        self.horizontalLayout_3.addWidget(self.wire_green)
        self.wire_blue = QtWidgets.QCheckBox(self.frame_4)
        self.wire_blue.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.wire_blue.setChecked(True)
        self.wire_blue.setObjectName("wire_blue")
        self.horizontalLayout_3.addWidget(self.wire_blue)
        self.gridLayout_2.addWidget(self.frame_4, 1, 0, 1, 1)
        self.frame_3 = QtWidgets.QFrame(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalSlider_1 = QtWidgets.QSlider(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.verticalSlider_1.sizePolicy().hasHeightForWidth())
        self.verticalSlider_1.setSizePolicy(sizePolicy)
        self.verticalSlider_1.setMaximum(1)
        self.verticalSlider_1.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_1.setObjectName("verticalSlider_1")
        self.horizontalLayout_4.addWidget(self.verticalSlider_1)
        self.verticalSlider_2 = QtWidgets.QSlider(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.verticalSlider_2.sizePolicy().hasHeightForWidth())
        self.verticalSlider_2.setSizePolicy(sizePolicy)
        self.verticalSlider_2.setMaximum(1)
        self.verticalSlider_2.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_2.setObjectName("verticalSlider_2")
        self.horizontalLayout_4.addWidget(self.verticalSlider_2)
        self.verticalSlider_3 = QtWidgets.QSlider(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.verticalSlider_3.sizePolicy().hasHeightForWidth())
        self.verticalSlider_3.setSizePolicy(sizePolicy)
        self.verticalSlider_3.setMaximum(1)
        self.verticalSlider_3.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_3.setObjectName("verticalSlider_3")
        self.horizontalLayout_4.addWidget(self.verticalSlider_3)
        self.verticalSlider_4 = QtWidgets.QSlider(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.verticalSlider_4.sizePolicy().hasHeightForWidth())
        self.verticalSlider_4.setSizePolicy(sizePolicy)
        self.verticalSlider_4.setMaximum(1)
        self.verticalSlider_4.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_4.setObjectName("verticalSlider_4")
        self.horizontalLayout_4.addWidget(self.verticalSlider_4)
        self.verticalSlider_5 = QtWidgets.QSlider(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.verticalSlider_5.sizePolicy().hasHeightForWidth())
        self.verticalSlider_5.setSizePolicy(sizePolicy)
        self.verticalSlider_5.setMaximum(1)
        self.verticalSlider_5.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_5.setObjectName("verticalSlider_5")
        self.horizontalLayout_4.addWidget(self.verticalSlider_5)
        self.gridLayout_2.addWidget(self.frame_3, 0, 0, 1, 1)
        self.dial = QtWidgets.QDial(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dial.sizePolicy().hasHeightForWidth())
        self.dial.setSizePolicy(sizePolicy)
        self.dial.setMaximum(360)
        self.dial.setWrapping(True)
        self.dial.setObjectName("dial")
        self.gridLayout_2.addWidget(self.dial, 0, 2, 2, 1)
        self.gridLayout.addWidget(self.frame, 4, 0, 1, 1)
        self.LEDs = QtWidgets.QFrame(self.centralwidget)
        self.LEDs.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.LEDs.setObjectName("LEDs")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.LEDs)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.led_0 = QtWidgets.QCheckBox(self.LEDs)
        self.led_0.setFocusPolicy(QtCore.Qt.NoFocus)
        self.led_0.setText("")
        self.led_0.setCheckable(False)
        self.led_0.setChecked(False)
        self.led_0.setObjectName("led_0")
        self.horizontalLayout_2.addWidget(self.led_0)
        spacerItem5 = QtWidgets.QSpacerItem(20, 36, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem5)
        self.led_1 = QtWidgets.QCheckBox(self.LEDs)
        self.led_1.setFocusPolicy(QtCore.Qt.NoFocus)
        self.led_1.setText("")
        self.led_1.setCheckable(False)
        self.led_1.setChecked(False)
        self.led_1.setObjectName("led_1")
        self.horizontalLayout_2.addWidget(self.led_1)
        self.led_2 = QtWidgets.QCheckBox(self.LEDs)
        self.led_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.led_2.setText("")
        self.led_2.setCheckable(False)
        self.led_2.setChecked(False)
        self.led_2.setObjectName("led_2")
        self.horizontalLayout_2.addWidget(self.led_2)
        self.led_3 = QtWidgets.QCheckBox(self.LEDs)
        self.led_3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.led_3.setText("")
        self.led_3.setCheckable(False)
        self.led_3.setChecked(False)
        self.led_3.setObjectName("led_3")
        self.horizontalLayout_2.addWidget(self.led_3)
        spacerItem6 = QtWidgets.QSpacerItem(20, 36, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem6)
        self.led_4 = QtWidgets.QCheckBox(self.LEDs)
        self.led_4.setFocusPolicy(QtCore.Qt.NoFocus)
        self.led_4.setText("")
        self.led_4.setCheckable(False)
        self.led_4.setChecked(False)
        self.led_4.setObjectName("led_4")
        self.horizontalLayout_2.addWidget(self.led_4)
        self.led_5 = QtWidgets.QCheckBox(self.LEDs)
        self.led_5.setFocusPolicy(QtCore.Qt.NoFocus)
        self.led_5.setText("")
        self.led_5.setCheckable(False)
        self.led_5.setChecked(False)
        self.led_5.setObjectName("led_5")
        self.horizontalLayout_2.addWidget(self.led_5)
        self.led_6 = QtWidgets.QCheckBox(self.LEDs)
        self.led_6.setFocusPolicy(QtCore.Qt.NoFocus)
        self.led_6.setText("")
        self.led_6.setCheckable(False)
        self.led_6.setChecked(False)
        self.led_6.setObjectName("led_6")
        self.horizontalLayout_2.addWidget(self.led_6)
        self.led_7 = QtWidgets.QCheckBox(self.LEDs)
        self.led_7.setFocusPolicy(QtCore.Qt.NoFocus)
        self.led_7.setText("")
        self.led_7.setCheckable(False)
        self.led_7.setChecked(False)
        self.led_7.setObjectName("led_7")
        self.horizontalLayout_2.addWidget(self.led_7)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem7)
        self.gridLayout.addWidget(self.LEDs, 3, 0, 1, 1)
        self.gridFrame = QtWidgets.QFrame(self.centralwidget)
        self.gridFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.gridFrame.setObjectName("gridFrame")
        self.keypad = QtWidgets.QGridLayout(self.gridFrame)
        self.keypad.setObjectName("keypad")
        self.pushButton4 = QtWidgets.QPushButton(self.gridFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton4.sizePolicy().hasHeightForWidth())
        self.pushButton4.setSizePolicy(sizePolicy)
        self.pushButton4.setObjectName("pushButton4")
        self.keypad.addWidget(self.pushButton4, 1, 0, 1, 1)
        self.pushButton7 = QtWidgets.QPushButton(self.gridFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton7.sizePolicy().hasHeightForWidth())
        self.pushButton7.setSizePolicy(sizePolicy)
        self.pushButton7.setObjectName("pushButton7")
        self.keypad.addWidget(self.pushButton7, 1, 3, 1, 1)
        self.pushButton0 = QtWidgets.QPushButton(self.gridFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton0.sizePolicy().hasHeightForWidth())
        self.pushButton0.setSizePolicy(sizePolicy)
        self.pushButton0.setObjectName("pushButton0")
        self.keypad.addWidget(self.pushButton0, 0, 0, 1, 1)
        self.pushButton6 = QtWidgets.QPushButton(self.gridFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton6.sizePolicy().hasHeightForWidth())
        self.pushButton6.setSizePolicy(sizePolicy)
        self.pushButton6.setObjectName("pushButton6")
        self.keypad.addWidget(self.pushButton6, 1, 2, 1, 1)
        self.pushButton8 = QtWidgets.QPushButton(self.gridFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton8.sizePolicy().hasHeightForWidth())
        self.pushButton8.setSizePolicy(sizePolicy)
        self.pushButton8.setObjectName("pushButton8")
        self.keypad.addWidget(self.pushButton8, 2, 0, 1, 1)
        self.pushButton2 = QtWidgets.QPushButton(self.gridFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton2.sizePolicy().hasHeightForWidth())
        self.pushButton2.setSizePolicy(sizePolicy)
        self.pushButton2.setObjectName("pushButton2")
        self.keypad.addWidget(self.pushButton2, 0, 2, 1, 1)
        self.pushButton3 = QtWidgets.QPushButton(self.gridFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton3.sizePolicy().hasHeightForWidth())
        self.pushButton3.setSizePolicy(sizePolicy)
        self.pushButton3.setObjectName("pushButton3")
        self.keypad.addWidget(self.pushButton3, 0, 3, 1, 1)
        self.pushButton9 = QtWidgets.QPushButton(self.gridFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton9.sizePolicy().hasHeightForWidth())
        self.pushButton9.setSizePolicy(sizePolicy)
        self.pushButton9.setObjectName("pushButton9")
        self.keypad.addWidget(self.pushButton9, 2, 1, 1, 1)
        self.pushButtona = QtWidgets.QPushButton(self.gridFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtona.sizePolicy().hasHeightForWidth())
        self.pushButtona.setSizePolicy(sizePolicy)
        self.pushButtona.setObjectName("pushButtona")
        self.keypad.addWidget(self.pushButtona, 2, 2, 1, 1)
        self.pushButtonb = QtWidgets.QPushButton(self.gridFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonb.sizePolicy().hasHeightForWidth())
        self.pushButtonb.setSizePolicy(sizePolicy)
        self.pushButtonb.setObjectName("pushButtonb")
        self.keypad.addWidget(self.pushButtonb, 2, 3, 1, 1)
        self.pushButton1 = QtWidgets.QPushButton(self.gridFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton1.sizePolicy().hasHeightForWidth())
        self.pushButton1.setSizePolicy(sizePolicy)
        self.pushButton1.setObjectName("pushButton1")
        self.keypad.addWidget(self.pushButton1, 0, 1, 1, 1)
        self.pushButton5 = QtWidgets.QPushButton(self.gridFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton5.sizePolicy().hasHeightForWidth())
        self.pushButton5.setSizePolicy(sizePolicy)
        self.pushButton5.setObjectName("pushButton5")
        self.keypad.addWidget(self.pushButton5, 1, 1, 1, 1)
        self.pushButtonc = QtWidgets.QPushButton(self.gridFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonc.sizePolicy().hasHeightForWidth())
        self.pushButtonc.setSizePolicy(sizePolicy)
        self.pushButtonc.setObjectName("pushButtonc")
        self.keypad.addWidget(self.pushButtonc, 3, 0, 1, 1)
        self.pushButtond = QtWidgets.QPushButton(self.gridFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtond.sizePolicy().hasHeightForWidth())
        self.pushButtond.setSizePolicy(sizePolicy)
        self.pushButtond.setObjectName("pushButtond")
        self.keypad.addWidget(self.pushButtond, 3, 1, 1, 1)
        self.pushButtone = QtWidgets.QPushButton(self.gridFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtone.sizePolicy().hasHeightForWidth())
        self.pushButtone.setSizePolicy(sizePolicy)
        self.pushButtone.setObjectName("pushButtone")
        self.keypad.addWidget(self.pushButtone, 3, 2, 1, 1)
        self.pushButtonf = QtWidgets.QPushButton(self.gridFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonf.sizePolicy().hasHeightForWidth())
        self.pushButtonf.setSizePolicy(sizePolicy)
        self.pushButtonf.setObjectName("pushButtonf")
        self.keypad.addWidget(self.pushButtonf, 3, 3, 1, 1)
        self.gridLayout.addWidget(self.gridFrame, 2, 0, 1, 1)
        self.lid_display = QtWidgets.QFrame(self.centralwidget)
        self.lid_display.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.lid_display.setObjectName("lid_display")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.lid_display)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lcdMinutes = QtWidgets.QLCDNumber(self.lid_display)
        self.lcdMinutes.setAutoFillBackground(False)
        self.lcdMinutes.setSmallDecimalPoint(True)
        self.lcdMinutes.setDigitCount(1)
        self.lcdMinutes.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdMinutes.setProperty("value", 3.0)
        self.lcdMinutes.setProperty("intValue", 3)
        self.lcdMinutes.setObjectName("lcdMinutes")
        self.horizontalLayout.addWidget(self.lcdMinutes)
        self.lcdSeconds = QtWidgets.QLCDNumber(self.lid_display)
        self.lcdSeconds.setDigitCount(2)
        self.lcdSeconds.setObjectName("lcdSeconds")
        self.horizontalLayout.addWidget(self.lcdSeconds)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem8)
        self.RGB_red = QtWidgets.QRadioButton(self.lid_display)
        self.RGB_red.setFocusPolicy(QtCore.Qt.NoFocus)
        self.RGB_red.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.RGB_red.setCheckable(False)
        self.RGB_red.setObjectName("RGB_red")
        self.horizontalLayout.addWidget(self.RGB_red)
        self.RGB_green = QtWidgets.QRadioButton(self.lid_display)
        self.RGB_green.setFocusPolicy(QtCore.Qt.NoFocus)
        self.RGB_green.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.RGB_green.setCheckable(False)
        self.RGB_green.setObjectName("RGB_green")
        self.horizontalLayout.addWidget(self.RGB_green)
        self.RGB_blue = QtWidgets.QRadioButton(self.lid_display)
        self.RGB_blue.setFocusPolicy(QtCore.Qt.NoFocus)
        self.RGB_blue.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.RGB_blue.setCheckable(False)
        self.RGB_blue.setObjectName("RGB_blue")
        self.horizontalLayout.addWidget(self.RGB_blue)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem9)
        self.gridLayout.addWidget(self.lid_display, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 376, 20))
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
        self.start_reset.setText(_translate("MainWindow", "Start/Reset"))
        self.solenoid.setText(_translate("MainWindow", "Solenoid"))
        self.wire_red.setText(_translate("MainWindow", "R"))
        self.wire_green.setText(_translate("MainWindow", "G"))
        self.wire_blue.setText(_translate("MainWindow", "B"))
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
        self.RGB_red.setText(_translate("MainWindow", "R"))
        self.RGB_green.setText(_translate("MainWindow", "G"))
        self.RGB_blue.setText(_translate("MainWindow", "B"))

