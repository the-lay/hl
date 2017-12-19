from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Provider(QObject):
    resultReady = pyqtSignal(list)

    def __init__(self):
        QObject.__init__(self)

    def search(self, query: str) -> None:
        print(self, 'search for', query)

        self.resultReady.emit(query.split())

