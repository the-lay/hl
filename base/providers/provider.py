from typing import List, Callable

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from fuzzywuzzy import fuzz

from ..helpers import settings


class ProviderSignals(QObject):
    result = pyqtSignal(list)


class Provider(QRunnable):

    details = {
        'name': '',
        'author': '',
        'description': '',
        'version': '',
    }
    icon = ''
    starts_with = ['']
    keywords = ['']
    greetings = ['']

    def __init__(self, manager):
        QRunnable.__init__(self)
        self.manager = manager
        self.signals = ProviderSignals()

        self.confidence = 0

    def calculate_confidence(self):

        for keyword in self.keywords:
            self.confidence = max(self.confidence, fuzz.partial_ratio(self.manager.search_query, keyword))

        for keyword in self.starts_with:
            if self.manager.search_query.startswith(keyword):
                self.confidence = max(self.confidence, 101)

    def run(self):
        raise NotImplementedError


class ProviderResult:

    def __init__(self, query: str,
                 title: str='', subtitle: str='',
                 icon: str='logo', confidence: int=0,
                 action: Callable=None):

        self.query = query
        self.title = title
        self.subtitle = subtitle
        self.icon = icon
        self.confidence = confidence
        self.action = action
