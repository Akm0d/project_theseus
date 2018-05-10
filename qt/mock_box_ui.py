#!/usr/bin/env python3
import sys

from PyQt5 import QtWidgets

try:
    from qt.qt_graphics import Ui_MainWindow
except ModuleNotFoundError:
    from qt_graphics import Ui_MainWindow


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    @staticmethod
    def run():
        app = QtWidgets.QApplication(sys.argv)
        application = ApplicationWindow()
        application.show()
        return app.exec_()


if __name__ == "__main__":
    ApplicationWindow.run()
