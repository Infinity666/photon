
class Meta(object):
    def __init__(self, meta='meta.json', verbose=True):

        super().__init__()

        from random import randint as _randint
        from photon import __ident__
        from .util.system import get_timestamp

        self.__verbose = verbose
        self._m = {
            'header': {
                'ident': '%s-%4X' %(__ident__, _randint(0x1000, 0xffff)),
                'initialized': get_timestamp(),
                'verbose': verbose
            },
            'import': dict(),
            'log': dict()
        }
        self.stage(meta, clean=True)

    def stage(self, s, clean=False):

        from .util.locations import search_location
        from .util.system import shell_notify

        s = search_location(s, create_in='data_dir')
        if not clean: self.load('stage', s, merge=True)

        self._m['header'].update({'stage': s})
        self.log = shell_notify(
            '%s stage' %('new clean' if clean else 'loaded'),
            more=dict(meta=s, clean=clean),
            verbose=self.__verbose
        )

    def load(self, mkey, mdesc, mdict=None, merge=False):

        from .util.files import read_json
        from .util.structures import dict_merge
        from .util.system import shell_notify

        j = mdict if mdict else read_json(mdesc)
        if j and isinstance(j, dict):
            self._m['header'].update({mkey: mdesc})
            if merge: self._m = dict_merge(self._m, j)
            else: self._m['import'][mkey] = j
            self.log = shell_notify(
                'load %s data and %s it into meta' %('got' if mdict else 'read', 'merged' if merge else 'imported'),
                more=dict(mkey=mkey, mdesc=mdesc, merge=merge),
                verbose=self.__verbose
            )
        return j

    @property
    def log(self):

        return self._m

    @log.setter
    def log(self, elem):

        from .util.files import read_json, write_json
        from .util.system import get_timestamp

        if elem: self._m['log'].update({get_timestamp(precice=True): elem})
        mfile = self._m['header']['stage']
        j = read_json(mfile)
        if j != self._m: write_json(mfile, self._m)
