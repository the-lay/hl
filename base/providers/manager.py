from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from ..helpers.settings import *
from .provider import *


class ProviderManager(QObject):

    resultsFound = pyqtSignal(list)
    # Return results by: self.resultsFound.emit([])

    def __init__(self):
        QObject.__init__(self)

        # self.
        self.searching = False

    # Emit results when received, return true when finished?
    # Should be on separate thread then I guess?
    def search(self, query: str) -> bool:
        if self.searching:
            self.stop_searching()

        # fire up searching threads
        # threads should call self.resultsFound.emit(query.split())
        self.searching = True
        self.resultsFound.emit(query.split())
        self.searching = False
        return True

    def stop_searching(self) -> bool:
        # stop searching threads
        # return False if couldnt stop threads for some reason?
        self.searching = False
        return True


