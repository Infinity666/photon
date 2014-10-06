
class Photon(object):
    def __init__(self, defaults='defaults.yaml', config='config.yaml', meta='meta.json'):

        super().__init__()

        from atexit import register as _register
        from photon import Settings, Meta, __ident__

        self.settings = Settings(defaults=defaults, config=config)
        self.meta = Meta(meta=meta)

        @_register
        def __copy_settings_to_meta():

            if self.meta and self.settings:
                self.meta.load('%s settings' %(__ident__), 'copy %s settings at exit' %(__ident__), mdict=self.settings.get)

        @_register
        def __goodby_message():

            from .util.system import shell_notif
            e = 'end of %s' %(__ident__)
            if self.meta: self.meta.log = e
            shell_notif(e)

        self.meta.log = '%s initialized' %(__ident__)
