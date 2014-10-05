
class Settings(object):

    def __init__(self, defaults='defaults.yaml', config='config.yaml'):
        super().__init__()

        from .util.system import stop_me, warn_me
        from .util.locations import get_locations, locate_file
        from .util.structures import yaml_loc_join, yaml_str_join

        self._s = {
            'locations': get_locations(),
            'files': dict()
        }

        loaders = [
            ('!loc_join', yaml_loc_join,),
            ('!str_join', yaml_str_join,)
        ]

        defaults = locate_file(defaults)
        if not self.load('defaults', defaults, loaders=loaders, merge=True):
            stop_me('could not load defaults: %s' %(defaults))

        config = locate_file(config, create_in='config_dir')
        if self._s != self.load('config', config, loaders=loaders[0], merge=True, writeback=True):
            warn_me('file written: %s' %(config))

    def load(self, skey, sdescr, loaders=None, merge=False, writeback=False):

        from .util.files import read_yaml, write_yaml
        from .util.structures import dict_merge

        y = read_yaml(sdescr, add_constructor=loaders)
        if y:
            self._s['files'].update({skey: sdescr})
            if merge: self._s = dict_merge(y, self._s)
            else: self._s[skey] = y
        if writeback and y != self._s: write_yaml(sdescr, self._s)
        return y

    @property
    def get(self):
        return self._s
