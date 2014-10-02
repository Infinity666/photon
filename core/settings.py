
class Settings(object):

    def __init__(self, defaults='defaults.yaml', config='config.yaml'):
        super().__init__()

        from photon import stop_me, warn_me
        from util.locations import get_locations
        from util.structures import yaml_loc_join, yaml_str_join

        self._s = {
            'locations': get_locations(),
            'files': dict()
        }

        loaders = [
            ('!loc_join', yaml_loc_join,),
            ('!str_join', yaml_str_join,)
        ]

        if not self.load_file('defaults', defaults, loaders=loaders, merge=True): stop_me('could not load defaults: %s' %(defaults))
        if self._s != self.load_file('config', config, loaders=loaders[0], merge=True, writeback=True): warn_me('file written: %s' %(config))

    def load_file(self, skey, sfile, loaders=None, merge=False, writeback=False):

        from util.files import read_yaml, write_yaml
        from util.locations import locate_file
        from util.structures import dict_merge

        sfile = locate_file(sfile, create_in='config_dir' if writeback else None)

        y = read_yaml(sfile, add_constructor=loaders)
        if y:
            self._s['files'].update({skey: sfile})
            if merge: self._s = dict_merge(y, self._s)
            else: self._s[skey] = y
        if writeback and y != self._s: write_yaml(sfile, self._s)
        return y

    def get(self, lst=None):
        res = self._s
        if lst:
            for l in lst:
                if l in res: res = res[l]
                else: return False
        return res
