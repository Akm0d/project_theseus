#!/usr/bin/env python3
import logging
import sys
from functools import partial
from typing import Dict

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QCheckBox, QPushButton

from MockPi.MockSmbus import MockBus as Smbus
from game.constants import I2C

try:
    from qt.qt_graphics import Ui_MainWindow
except ModuleNotFoundError:
    from qt_graphics import Ui_MainWindow

log = logging.getLogger(__name__)


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.bus = Smbus(1)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Get easy access to UI elements
        self.rgb = self.ui.lid_display.layout()
        self.minutes = self.ui.lcdMinutes
        self.seconds = self.ui.lcdSeconds
        self.potentiometer = self.ui.dial

        # TODO Make connections to functions

        # TODO Listen on the SMBus for messages and then call the right functions

        # TODO connect clicked.connect from UI elements to functions
        log.debug("Connecting Buttons")
        for h, button in self.keypad.items():
            button.clicked.connect(partial(lambda x: self.bus.write_byte_data(0x1, I2C.LASERS, x), h))

        # TODO simulate sending SMBus messages when things are clicked

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
    def laser(self) -> Dict[int, QCheckBox]:
        return {
            0: self.ui.laser_0,
            1: self.ui.laser_1,
            2: self.ui.laser_2,
            3: self.ui.laser_3,
            4: self.ui.laser_4,
            5: self.ui.laser_5,
        }

    @property
    def photo_resistor(self) -> Dict[int, QCheckBox]:
        return {
            0: self.ui.photodiode_0,
            1: self.ui.photodiode_1,
            2: self.ui.photodiode_2,
            3: self.ui.photodiode_3,
            4: self.ui.photodiode_4,
            5: self.ui.photodiode_5,
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
