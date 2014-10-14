
class Settings(object):

    def __init__(self, config='config.yaml', summary='summary.yaml', verbose=True):

        super().__init__()

        from .util.system import shell_notify
        from .util.locations import get_locations, locate_file
        from .util.structures import yaml_loc_join, yaml_str_join

        self.__verbose = verbose
        self._s = {
            'locations': get_locations(),
            'files': dict()
        }

        loaders = [('!loc_join', yaml_loc_join,), ('!str_join', yaml_str_join,)]

        config, sdict = ('startup import', config) if isinstance(config, dict) else (locate_file(config), None)

        if not self.load('config', config, sdict=sdict, loaders=loaders, merge=True):
            shell_notify('could not load config', state=True, more=dict(config=config, sdict=sdict))

        if summary:
            summary = locate_file(summary, create_in='conf_dir')
            if self._s != self.load('summary', summary, loaders=loaders, merge=True, writeback=True):
                shell_notify('settings summary written', more=summary, verbose=verbose)

    def load(self, skey, sdesc, sdict=None, loaders=None, merge=False, writeback=False):

        from .util.files import read_yaml, write_yaml
        from .util.structures import dict_merge
        from .util.system import shell_notify

        y = sdict if sdict else read_yaml(sdesc, add_constructor=loaders)
        if y and isinstance(y, dict):
            if not sdict: self._s['files'].update({skey: sdesc})
            if merge: self._s = dict_merge(self._s, y)
            else: self._s[skey] = y
            shell_notify(
                'load %s data and %s it into settings' %('got' if sdict else 'read', 'merged' if merge else 'imported'),
                more=dict(skey=skey, sdesc=sdesc, merge=merge, writeback=writeback),
                verbose=self.__verbose
            )
        if writeback and y != self._s: write_yaml(sdesc, self._s)
        return y

    @property
    def get(self):

        return self._s
