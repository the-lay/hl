from PyQt5.QtCore import *

import base.providers.provider as provider


class Plugin(provider.Provider):

    details = {
        'name': '',
        'author': '',
        'description': 'This plugin provides Wikipedia search results',
        'version': '',
    }
    icon = 'wiki'
    starts_with = ['wiki', 'wikipedia']
    keywords = ['wiki', 'wikipedia']
    greetings = ['wiki "query"', 'wikipedia']

    def run(self):
        self.calculate_confidence()

        item = provider.ProviderResult(self.manager.search_query,
                                       title='Wiki search', subtitle='Wikipedia',
                                       icon=self.icon, confidence=self.confidence,
                                       action=lambda: print('wiki woah'))

        # QThread.sleep(3)

        self.signals.result.emit([item])
