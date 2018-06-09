#!/usr/bin/python3
"""
Main entrance point for Highlight.
@author Ilja Gubins
@copyright 2017, Ilja Gubins
@version 0.0.1
@status development
"""

import sys
import traceback
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from base.application import Application


if __name__ == '__main__':

    # PyQT debugging
    sys.excepthook = traceback.print_exception

    #
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

    # Application tags
    app = QApplication(sys.argv)

    # The main app
    win = Application()
    win.show()

    # Run the loop
    sys.exit(app.exec_())
