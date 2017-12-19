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
from PyQt5.QtWidgets import QApplication
from base.application import Application


if __name__ == '__main__':

    # PyQT debugging
    sys.excepthook = traceback.print_exception

    # Application tags
    app = QApplication(sys.argv)

    # The main app
    win = Application()
    win.show()

    # Run the loop
    sys.exit(app.exec_())
