import base.providers.provider as provider


class Plugin(provider.Provider):

    details = {
        'name': '',
        'author': '',
        'description': 'This plugin provides Google search results',
        'version': '',
    }
    icon = 'google'
    starts_with = 'google'
    keywords = ['google', 'web']
    greetings = ['anything on google']

    def run(self):
        self.calculate_confidence()

        item = provider.ProviderResult(self.manager.search_query,
                                       title='Web search', subtitle='Google',
                                       icon=self.icon, confidence=self.confidence,
                                       action=lambda: print('google woah'))
        self.signals.result.emit([item])
