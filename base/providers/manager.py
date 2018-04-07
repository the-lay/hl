import os
import sys
import re
import importlib

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from fuzzywuzzy import fuzz

from ..helpers import settings
from .provider import *


class ProviderManager(QObject):

    resultsFound = pyqtSignal(list)
    # finished = pyqtSignal()
    # Return results by: self.resultsFound.emit([])

    def __init__(self):
        QObject.__init__(self)

        # Searching flag
        self.searching = False
        self.search_query = ''

        # Thread pool
        self.thread_pool = QThreadPool.globalInstance()

        # Populate with providers
        self.providers = []
        self.load_plugins()
        print('done')

    def load_plugins(self, clean_start=False):

        importlib.import_module('plugins')

        if clean_start:
            self.providers = []

        for file in os.listdir(str(settings.PLUGINS_PATH)):
            if file.endswith('.py') and not file.startswith('__'):
                file = file.replace('.py', '')
                plugin = importlib.import_module('.' + file, 'plugins')
                self.providers.append(plugin)

        # for mod in modules:
        #     self.providers.append(mod.Plugin(self))

    # Emit results when received, return true when finished?
    # Should be on separate thread then I guess?
    def search(self, query: str):

        # Cancel previous search
        if self.searching:
            self.stop_searching()

        # Start new search
        self.searching = True
        self.search_query = query

        for provider in self.providers:
            plugin = provider.Plugin(self)
            plugin.signals.result.connect(self.finished_searching)
            self.thread_pool.start(plugin)

    def finished_searching(self, results: list):

        for res in results:

            # remove "too late" search results
            if res.query != self.search_query:
                results.remove(res)

        self.resultsFound.emit(results)

        # TODO add search progess bar
        # TODO update progress bar with self.thread_pool.activeThreadCount()

        # If all runnables finished, declare that searching is done
        if self.thread_pool.activeThreadCount() == 0:
            self.searching = False

        # TODO color recognized keywords?
        # https://stackoverflow.com/questions/14417333/how-can-i-change-color-of-part-of-the-text-in-qlineedit

    def stop_searching(self):
        print('stop_searching')
        # for provider in self.providers:
        #     provider.stop_searching()

    # TODO populate greetings from providers manager
    def generate_greetings(self) -> [str]:
        greetings = []

        for provider in self.providers:
            for greeting in provider.Plugin.greetings:
                greetings.append(greeting)

        return greetings

        # return ["wiki 'query'",
        #         "youtube 'query'",
        #         "calendar 'query'",
        #         "imdb 'query'",
        #         "lyrics 'query'",
        #         "any file on your PC",
        #         "help"]
