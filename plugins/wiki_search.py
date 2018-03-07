import base.providers.provider as provider


class WikiProvider(provider.Provider):

    def run(self):
        print('WikiProvider: search for', self.query)
        self.sleep(1)
        self.result.emit(['Wikipedia'], self)

    def icon(self):
        return 'wiki'

    def starts_with(self):
        return 'wiki'

    def keywords(self):
        return ['wiki']
