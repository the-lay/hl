import base.providers.provider as provider


class GoogleProvider(provider.Provider):

    def run(self):
        print('GoogleProvider: search for', self.query)
        self.result.emit(['Web search'], self)

    def icon(self):
        return 'google'

    def starts_with(self):
        return 'google'

    def keywords(self):
        return ['google', 'web']
