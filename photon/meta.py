
class Meta(object):
    def __init__(self, meta='meta.json'):
        super().__init__()

        from random import randint as _randint
        from photon import __ident__
        from .util.time import get_timestamp

        self._m = {
            'header': {
                'ident': '%s-%4X' %(__ident__, _randint(0x1000, 0xffff)),
                'initialized': get_timestamp(),
            },
            'import': dict(),
            'log': dict()
        }
        self.stage(meta, clean=True)

    def stage(self, s, clean=False):

        from .util.locations import locate_file

        s = locate_file(s, create_in='data_dir')
        if not clean: self.load('stage', s, merge=True)

        self._m['header'].update({'stage': s})
        self.log = {'stage': dict(meta=s, clean=clean)}

    def load(self, mkey, mdesc, mdict=None, merge=False):

        from .util.files import read_json
        from .util.structures import dict_merge

        j = mdict if mdict else read_json(mdesc)
        if j:
            self._m['header'].update({mkey: mdesc})
            if merge: self._m = dict_merge(self._m, j)
            else: self._m['import'][mkey] = j
            self.log = {'load': dict(mkey=mkey, mdesc=mdesc, merge=merge)}

    @property
    def log(self):

        return self._m

    @log.setter
    def log(self, elem):

        from .util.files import read_json, write_json
        from .util.time import get_timestamp

        if elem: self._m['log'].update({get_timestamp(precice=True): elem})
        mfile = self._m['header']['stage']
        j = read_json(mfile)
        if j != self._m: write_json(mfile, self._m)
