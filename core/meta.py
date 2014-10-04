
class Meta(object):
    def __init__(self, meta='meta.json'):
        super().__init__()

        from random import randint
        from core.photon import IDENT
        from util.time import get_timestamp

        self._meta = {
            'header': {
                'ident': '%s-%4X' %(IDENT, randint(0x1000, 0xffff)),
                'initialized': get_timestamp(),
            },
            'import': dict(),
            'log': dict()
        }
        self.stage(meta, clean=True)

    def stage(self, s, clean=False):

        from util.locations import locate_file

        s = locate_file(s, create_in='data_dir')
        if not clean: self.load('stage', s, merge=True)

        self._meta['header'].update({'stage': s})
        self.log('stage %s (%s)' %(s, 'clean' if clean else 'switch'))

    def load(self, mkey, mdesc, mdict=None, merge=False):

        from util.files import read_json
        from util.structures import dict_merge

        j = mdict if mdict else read_json(mdesc)
        if j:
            self._meta['header'].update({mkey: mdesc})
            if merge: self._meta = dict_merge(self._meta, j)
            else: self._meta['import'][mkey] = j
            self.log('load %s (%s)' %(mkey, mdesc))

    def log(self, elem):

        from util.time import get_timestamp
        from util.files import read_json, write_json

        if elem: self._meta['log'].update({get_timestamp(precice=True): elem})
        mfile = self._meta['header']['stage']
        j = read_json(mfile)
        if j != self._meta: write_json(mfile, self._meta)

    def get(self):
        return self._meta
