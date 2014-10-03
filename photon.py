
IDENT = 'photon'

class Photon(object):
    def __init__(self):
        super().__init__()

        from core.settings import Settings
        from core.meta import Meta

        self.settings = Settings()
        self.meta = Meta()

        self.meta.load('settings', IDENT, self.settings.get())

    def __del__(self):
        print('end of %s' %(IDENT))

