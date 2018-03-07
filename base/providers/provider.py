from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from yapsy.IPlugin import IPlugin


class Provider(QThread, IPlugin):
    result = pyqtSignal(list, IPlugin)

    def __init__(self):
        QThread.__init__(self)
        IPlugin.__init__(self)
        self.query = ''
        self.stop_requested = False

    def run(self):
        raise NotImplementedError

    def search(self, query: str):
        self.query = query
        self.start()

    def stop_searching(self):
        self.stop_requested = True

    def icon(self):
        raise NotImplementedError

    def keywords(self):
        raise NotImplementedError

    def starts_with(self):
        raise NotImplementedError