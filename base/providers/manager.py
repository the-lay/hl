from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from yapsy.PluginManager import PluginManager
from fuzzywuzzy import fuzz

from ..helpers import settings
from .provider import *


class ProviderManager(QObject):

    resultsFound = pyqtSignal(list, Provider, int)
    finished = pyqtSignal()
    # Return results by: self.resultsFound.emit([])

    def __init__(self):
        QObject.__init__(self)

        self.searching = False

        # Populate with providers
        self.providers = []
        self.yap = PluginManager()
        self.yap.setPluginPlaces([str(settings.pluginsPath)])
        self.yap.collectPlugins()

        for plugin in self.yap.getAllPlugins():
            self.yap.activatePluginByName(plugin.name)
            plugin.plugin_object.result.connect(self.finished_searching)
            self.providers.append(plugin.plugin_object)

    # Emit results when received, return true when finished?
    # Should be on separate thread then I guess?
    def search(self, query: str):
        if self.searching:
            self.stop_searching()

        self.searching = True
        for provider in self.providers:
            provider.search(query)

    def finished_searching(self, results: list, provider: Provider):

        # determine confidence of received results
        confidence = 0

        # fuzzy partial search through keywords
        # TODO color recognized keywords?
        # https://stackoverflow.com/questions/14417333/how-can-i-change-color-of-part-of-the-text-in-qlineedit
        for keyword in provider.keywords():
            confidence = max(confidence, fuzz.partial_ratio(provider.query, keyword))

        # if query starts with module's defined starts_with, set confidence to max
        if provider.query.startswith(provider.starts_with()):
            confidence = 101

        # emit results to result list
        self.resultsFound.emit(results, provider, confidence)

        # Figure out if all threads finished
        for provider in self.providers:
            if not provider.isFinished():
                return

        # If so, set searching to False
        print('all threads finished searching')
        self.searching = False

    def stop_searching(self):
        print('stop_searching')
        for provider in self.providers:
            provider.stop_searching()



