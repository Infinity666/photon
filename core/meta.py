
class Meta(object):
    def __init__(self, defaults='defaults.yaml', config='config.yaml', meta='meta.json', clean=True):
        super().__init__()

        from util.files import locate_file

        self._meta = dict()
        self.stage(locate_file(meta, create_in='data_dir'), clean=clean)

    def stage(self, s, clean=False):

        from random import randint
        from photon import IDENT
        from util.files import read_json
        from util.time import get_timestamp
        from util.structures import dict_merge

        m = read_json(s)
        if not m or not isinstance(m, dict) or not 'header' in m or clean:
            m = {
                'header': {
                    'initialized': get_timestamp(),
                    'ident': '%s-%4X' %(IDENT, randint(0x1000,0xffff)),
                },
                'log': dict()
            }
        self._meta = dict_merge(self._meta, m)
        self._meta['header'].update({'stage': s})
        self.dump(warn='%s stage' %('clean' if clean else 'switched'))

    def get(self):
        m = self._meta
        return m

    def dump(self, warn=False):

        from photon import warn_me
        from util.files import read_json, write_json

        mfile = self._meta['header']['stage']
        m = read_json(mfile)
        if m != self._meta:
            b = write_json(mfile, self._meta)
            if warn: warn_me('meta written: %s (%s bytes)%s' %(mfile, b, '' if warn == True else ' - %s' %(warn)))

    def log(self, elem):

        from util.time import get_timestamp

        if elem: self._meta['log'][get_timestamp(precice=True)] = elem
        self.dump()


