from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from ..helpers.settings import *


class ProviderManager(QObject):
    resultsFound = pyqtSignal(list)

    def __init__(self):
        QObject.__init__(self)
        # search_thread =
        actions = dict()

    def search(self, query: str):
        self.resultsFound.emit(query.split())
