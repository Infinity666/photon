
from photon import __ident__

class Photon(object):
    def __init__(self, defaults='defaults.yaml', config='config.yaml', meta='meta.json'):
        super().__init__()

        from photon import Settings
        from photon import Meta

        self.settings = Settings(defaults=defaults, config=config)
        self.meta = Meta(meta=meta)

        self.meta.load('settings', __ident__, self.settings.get)

    def __del__(self):
        print('end of %s' %(__ident__))

