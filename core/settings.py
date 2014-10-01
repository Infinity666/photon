
class Settings(object):

    def __init__(self, defaults='defaults.yaml', config='config.yaml'):
        super().__init__()

        from util.locations import get_locations
        from util.files import locate_file
        from util.structures import yaml_loc_join, yaml_str_join

        self._s = {
            'locations': get_locations(),
            'files': {
                'defaults': locate_file(defaults, critical=True),
                'config': locate_file(config, create_in='config_dir')
            }
        }

        loaders = [
            ('!loc_join', yaml_loc_join,),
            ('!str_join', yaml_str_join,)
        ]

        [self.__y_load(*y) for y in [
            (self._s['files']['defaults'], loaders, True, False),
            (self._s['files']['config'], loaders[0], False, True)
        ]]

    def __y_load(self, filename, add_constructor=None, critical=True, writeback=False):

        from photon import stop_me, warn_me
        from util.files import read_yaml, write_yaml
        from util.structures import dict_merge

        y = read_yaml(filename, add_constructor=add_constructor)
        if not y and critical: stop_me('could not load %s' %(filename))
        if y: self._s = dict_merge(y, self._s)
        if y != self._s and writeback: warn_me('file written: %s (%s bytes)' %(filename, write_yaml(filename, self._s)))

    def get_settings(self, lst=None):
        res = self._s
        if not lst: return self._s
        for l in lst:
            if l in res: res = res[l]
            else: return False
        return res
