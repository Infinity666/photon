'''
.. |yaml_loaders| replace:: :func:`util.structures.yaml_str_join` and :func:`util.structures.yaml_loc_join`
'''

class Settings(object):
    '''
    Settings is a class which provides access to compiled settings loaded from YAML-files.

    The YAML-files will be read with specific loaders which enables certain logic within the configuration. It is possible to:

        * Insert references to existing fields via anchors and ``!str_join`` or ``!loc_join``
        * Insert keywords like **hostname** or **timestamp** using ``!str_join``
        * Combine path-segments using ``!loc_join``
        * Insert keywords like **home_dir** or **backup_dir** using ``!loc_join``

    It is also possible to import or merge further content.

    :param config: The initial configuration to load. |filelocate|

        * The common way is to use a short-filename to locate it next to the script using Photon.
        * Can also be a full path.
        * Bring your own initial config!  |appteardown| if not found.
        * Can also passed directly as a dict
    :param summary: Where to store the loaded output from the config. |filelocate|

        * File must already exist, will be created in 'conf_dir' from :func:`util.locations.get_locations` otherwise

            * so only use a short name if it is intended to be created

        .. note:: The last loaded file wins

            * The summary is intended to provide a editable config-file for the end-user
            * If a values differs from the values in `config`, the value in `summary` wins
            * Other values which not exist in `summary` will be set from `config`

                * If a value contains a loader call which expresses the same
                * If the end-user wants to completely reset the config to the shipped one he simply delete all lines within

        * Can be skipped by explicitly setting it to ``None``

    :param verbose: Sets the `verbose` flag for the underlying :ref:`util` functions

    .. seealso:: |yaml_loaders| as well as the :ref:`settings_file_example`
    '''

    def __init__(self, config='config.yaml', summary='summary.yaml', verbose=True):

        super().__init__()

        from .util.system import shell_notify
        from .util.locations import get_locations, search_location
        from .util.structures import yaml_str_join, yaml_loc_join

        self.__verbose = verbose
        self._s = {
            'locations': get_locations(),
            'files': dict()
        }

        loaders = [('!str_join', yaml_str_join,), ('!loc_join', yaml_loc_join,)]

        config, sdict = ('startup import', config) if isinstance(config, dict) else (search_location(config), None)

        if not self.load('config', config, sdict=sdict, loaders=loaders, merge=True):
            shell_notify('could not load config', state=True, more=dict(config=config, sdict=sdict))

        if summary:
            summary = search_location(summary, create_in='conf_dir')
            if self._s != self.load('summary', summary, loaders=loaders, merge=True, writeback=True):
                shell_notify('settings summary written', more=summary, verbose=verbose)

    def load(self, skey, sdesc, sdict=None, loaders=None, merge=False, writeback=False):
        '''
        Loads a dictionary into current settings

        :param skey: Type of data to load. Is be used to reference the data in the files sections within settings
        :param sdesc: Either filename of yaml-file to load or further description of imported data when `sdict` is used
        :param dict sdict: Directly pass data as dictionary instead of loading it from a yaml-file. Make sure to set `skey` and `sdesc` accordingly
        :param list loaders: Append custom loaders to the YAML-loader.
        :param merge: Merge received data into current settings or place it under `skey` within meta
        :param writeback: Write back loaded (and merged/imported) result back to the original file. This is used to generate the summary files
        :returns: The loaded (or directly passed) content

        .. seealso:: |yaml_loaders|
        '''

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
        '''
        :returns: Current settings
        '''

        return self._s
