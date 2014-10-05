
from photon import IDENT

class Photon(object):
    def __init__(self, defaults='defaults.yaml', config='config.yaml', meta='meta.json'):
        super().__init__()

        from photon import Settings
        from photon import Meta

        self.settings = Settings(defaults=defaults, config=config)
        self.meta = Meta(meta=meta)

        self.meta.load('settings', IDENT, self.settings.get)

    def __del__(self):
        print('end of %s' %(IDENT))

