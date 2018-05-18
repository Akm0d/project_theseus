#!/usr/bin/env python3
import logging
import sys
from functools import partial
from typing import Dict

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QCheckBox, QPushButton, QSlider

from MockPi.MockSmbus import MockBus as Smbus
from game.constants import I2C
from game.logic import Logic

try:
    from qt.qt_graphics import Ui_MainWindow
except ModuleNotFoundError:
    from qt_graphics import Ui_MainWindow

log = logging.getLogger(__name__)


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.bus = Smbus(Logic.bus_num)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Get easy access to UI elements
        self.rgb = self.ui.lid_display.layout()
        self.minutes = self.ui.lcdMinutes
        self.seconds = self.ui.lcdSeconds
        self.potentiometer = self.ui.dial

        # TODO Make connections to functions

        # TODO Listen on the SMBus for messages and then call the right functions

        for h, button in self.keypad.items():
            button.clicked.connect(partial(
                lambda x: self.bus.write_byte_data(Logic.bus_num, I2C.KEYPAD, x), h
            ))

        for _, checkbox in self.photo_resistor.items():
            checkbox.clicked.connect(partial(
                lambda: self.bus.write_byte_data(Logic.bus_num, I2C.LASERS, self.laser_mask)
            ))

        self.potentiometer.valueChanged.connect(
            lambda: self.bus.write_byte_data(Logic.bus_num, I2C.ROTARY, self.potentiometer.value()))

        for _, switch in self.switches.items():
            switch.valueChanged.connect(
                lambda: self.bus.write_byte_data(Logic.bus_num, I2C.SWITCHES, self.switch_mask)
            )

        self.ui.wire_red.clicked.connect(lambda: self.bus.write_byte_data(Logic.bus_num, I2C.WIRE, 0xd))
        self.ui.wire_blue.clicked.connect(lambda: self.bus.write_byte_data(Logic.bus_num, I2C.WIRE, 0xb))
        self.ui.wire_green.clicked.connect(lambda: self.bus.write_byte_data(Logic.bus_num, I2C.WIRE, 0xe))

        self.ui.start_reset.clicked.connect(lambda: print("ya"))

    @property
    def time(self) -> str:
        """
        :return: The current time shown on the lcd
        """

    @time.setter
    def time(self, value):
        """
        TODO set the value on the timer
        :param value:
        :return:
        """

    @property
    def switches(self) -> Dict[int, QSlider]:
        return {
            4: self.ui.verticalSlider_1,
            3: self.ui.verticalSlider_2,
            2: self.ui.verticalSlider_3,
            1: self.ui.verticalSlider_4,
            0: self.ui.verticalSlider_5,
        }

    @property
    def switch_mask(self) -> bin:
        result = 0b00000
        for offset, sw in self.switches.items():
            result ^= ((1 if sw.value() else 0) << offset)
        return result

    @property
    def laser_mask(self) -> bin:
        """
        :return: An integer that represents all the photo resistors that have a laser shining on them
        """
        result = 0b000000
        for offset, box in self.photo_resistor.items():
            result ^= ((1 if box.isChecked() else 0) << offset)
        return result

    @property
    def laser(self) -> Dict[int, QCheckBox]:
        return {
            5: self.ui.laser_0,
            4: self.ui.laser_1,
            3: self.ui.laser_2,
            2: self.ui.laser_3,
            1: self.ui.laser_4,
            0: self.ui.laser_5,
        }

    @property
    def photo_resistor(self) -> Dict[int, QCheckBox]:
        return {
            5: self.ui.photodiode_0,
            4: self.ui.photodiode_1,
            3: self.ui.photodiode_2,
            2: self.ui.photodiode_3,
            1: self.ui.photodiode_4,
            0: self.ui.photodiode_5,
        }

    @property
    def led(self) -> Dict[int, QCheckBox]:
        return {
            0: self.ui.led_0,
            1: self.ui.led_1,
            2: self.ui.led_2,
            3: self.ui.led_3,
            4: self.ui.led_4,
            5: self.ui.led_5,
            6: self.ui.led_6,
            7: self.ui.led_7,
        }

    @property
    def keypad(self) -> Dict[hex, QPushButton]:
        return {
            0x0: self.ui.pushButton0,
            0x1: self.ui.pushButton1,
            0x2: self.ui.pushButton2,
            0x3: self.ui.pushButton3,
            0x4: self.ui.pushButton4,
            0x5: self.ui.pushButton5,
            0x6: self.ui.pushButton6,
            0x7: self.ui.pushButton7,
            0x8: self.ui.pushButton8,
            0x9: self.ui.pushButton9,
            0xa: self.ui.pushButtona,
            0xb: self.ui.pushButtonb,
            0xc: self.ui.pushButtonc,
            0xd: self.ui.pushButtond,
            0xe: self.ui.pushButtone,
            0xf: self.ui.pushButtonf,
        }

    @staticmethod
    def run():
        app = QtWidgets.QApplication(sys.argv)
        application = ApplicationWindow()
        application.show()
        return app.exec_()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    ApplicationWindow.run()
