'''
.. |yaml_loaders| replace:: :func:`util.structures.yaml_str_join`
    and :func:`util.structures.yaml_loc_join`
'''

from .util.files import read_yaml, write_yaml
from .util.locations import get_locations, search_location
from .util.structures import dict_merge, yaml_loc_join, yaml_str_join
from .util.system import shell_notify


class Settings(object):
    '''
    Settings is a class which provides access to
    compiled settings loaded from YAML-files.

    The YAML-files will be read with specific loaders which enables
    certain logic within the configuration.
    It is possible to:

        * Insert references to existing fields via \
        anchors and ``!str_join`` or ``!loc_join``

        * Insert keywords like **hostname** or \
        **timestamp** using ``!str_join``

        * Combine path-segments using ``!loc_join``

        * Insert keywords like **home_dir** or \
        **conf_dir** using ``!loc_join``

    It is also possible to import or merge further content.

    :param defaults: The initial configuration to load. |filelocate|

        * The common way is to use a short-filename to locate it next \
        to the script using Photon.

        * Can also be a full path.

        * Can also passed directly as a dict

        * Bring your own defaults!  |appteardown| if not found or none passed.

    :param config:
        Where to store the loaded output from the `defaults`. |filelocate|

        * File must already exist, will be created in 'conf_dir' \
        from :func:`util.locations.get_locations` otherwise

            * Therefore use a short name (or full path) if one \
            should be created

        .. note:: The last loaded file wins

            * The config is intended to provide a editable file \
            for the end-user

            * If a value differs from the original values in \
            `defaults`, the value in `config` wins

                * Other values which not exist in `config` \
                 will be set from `defaults`

                * If a value in `config` contains a loader call \
                which expresses the same as the value in `defaults` \
                it will be skipped.

            * Be careful using **timestamp** s in a config. \
            The timestamp of the first launch will always be used.

            * Simply delete all lines within the config to completely \
            reset it to the defaults

        * Can be skipped by explicitly setting it to ``None``

    :param verbose: Sets the `verbose` flag for \
    the underlying :ref:`util` functions

    .. seealso:: |yaml_loaders| as well as the :ref:`settings_file_example`
    '''

    def __init__(self, defaults, config='config.yaml', verbose=True):

        super().__init__()

        self.__verbose = verbose
        self.__settings = {
            'locations': get_locations(),
            'files': dict()
        }

        loaders = [
            ('!str_join', yaml_str_join,),
            ('!loc_join', yaml_loc_join,)
        ]

        defaults, sdict = (
            'startup import',
            defaults
        ) if isinstance(defaults, dict) else (
            search_location(defaults),
            None
        )

        if not self.load(
            'defaults',
            defaults,
            sdict=sdict,
            loaders=loaders,
            merge=True
        ):
            shell_notify(
                'could not load defaults',
                state=True,
                more=dict(defaults=defaults, sdict=sdict)
            )

        if config:
            config = search_location(config, create_in='conf_dir')
            if self.__settings != self.load(
                'config',
                config,
                loaders=loaders,
                merge=True,
                writeback=True
            ):
                shell_notify(
                    'settings config written',
                    more=config,
                    verbose=verbose
                )

    def load(self, skey, sdesc,
             sdict=None, loaders=None, merge=False, writeback=False):
        '''
        Loads a dictionary into current settings

        :param skey:
            Type of data to load. Is be used to reference the data \
            in the files sections within settings
        :param sdesc:
            Either filename of yaml-file to load or further description of \
            imported data when `sdict` is used
        :param dict sdict:
            Directly pass data as dictionary instead of loading \
            it from a yaml-file. \
            Make sure to set `skey` and `sdesc` accordingly
        :param list loaders:
            Append custom loaders to the YAML-loader.
        :param merge:
            Merge received data into current settings or \
            place it under `skey` within meta
        :param writeback:
            Write back loaded (and merged/imported) result back \
            to the original file. \
            This is used to generate the summary files
        :returns:
            The loaded (or directly passed) content

        .. seealso:: |yaml_loaders|
        '''

        y = sdict if sdict else read_yaml(sdesc, add_constructor=loaders)
        if y and isinstance(y, dict):
            if not sdict:
                self.__settings['files'].update({skey: sdesc})
            if merge:
                self.__settings = dict_merge(self.__settings, y)
            else:
                self.__settings[skey] = y
            shell_notify(
                'load %s data and %s it into settings' % (
                    'got' if sdict else 'read',
                    'merged' if merge else 'imported'
                ),
                more=dict(skey=skey, sdesc=sdesc,
                          merge=merge, writeback=writeback),
                verbose=self.__verbose
            )
        if writeback and y != self.__settings:
            write_yaml(sdesc, self.__settings)
        return y

    @property
    def get(self):
        '''
        :returns: Current settings
        '''

        return self.__settings
