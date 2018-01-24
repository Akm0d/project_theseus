import sys
from PyQt4 import QtGui, QtCore
from VirtualDiffusingStation_ui import MainWindow


class VirtualDiffusingStation():
    '''
    Main control class for the GUI. It is made to interact with the VirtualDiffusingStation_ui.py file that has been
    generated from a .ui file that has been created by QtDesigner. If you find that you need to change something in
    the GUI, just open the .ui file in QtDesigner, make your changes, and then run the Makefile to regenerate the
    VirtualDiffusingStation_ui.py file.
    '''
    def __init__(self):
        # Cannot get MainWindow to work using inheritance.... DX
        self.mw = MainWindow()
        '''
        To connect a funtion to a particular GUI component, you will need to run the following command for every
        for each component, passing in the controlling function in as the parameter
        '''
        self.mw.RgbOnOffCheckbox.clicked.connect(self.example)

    def example(self):
        # example controlling function.
        pass


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main = VirtualDiffusingStation()
    main.mw.show()
    sys.exit(app.exec_())
