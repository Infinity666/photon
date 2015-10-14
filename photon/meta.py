from random import randint as _randint
from threading import Lock

from photon import IDENT

from .util.files import read_json, write_json
from .util.locations import search_location
from .util.structures import dict_merge
from .util.system import get_timestamp, shell_notify


class Meta(object):
    '''
    Meta is a class which bounds to an actual json-file on disk.
    It provides a logger storing the entries in that json-file.

    It is also possible to import contents.
    By staging out to a different directory meta-files are left behind
    for further debugging or to see what was going on.

    :param meta:
        Initial, clean meta file to use. See :meth:`stage` for more
    :param verbose:
        Sets the `verbose` flag for the underlying :ref:`util` functions
    '''
    def __init__(self, meta='meta.json', verbose=True):

        super().__init__()

        self.__verbose = verbose
        self.__meta = {
            'header': {
                'ident': '%s-%4X' % (IDENT, _randint(0x1000, 0xffff)),
                'initialized': get_timestamp(),
                'verbose': verbose
            },
            'import': dict(),
            'log': dict()
        }
        self.__lock = Lock()
        self.stage(meta, clean=True)

    def stage(self, name, clean=False):
        '''
        Switch stage

        :param name:
            Filename of new meta file. |filelocate|

            * File must not already exist, will be created in 'data_dir' \
            from :func:`util.locations.get_locations`

            * Can also be a full path to place it anywhere desired

        :param clean: What to do with preexisting meta files?

            * ``False``: Merge current meta with preexisting one
            * ``True``: Replace preexisting meta with current one
        '''

        name = search_location(name, create_in='data_dir')
        if not clean:
            self.load('stage', name, merge=True)

        self.__meta['header'].update({'stage': name})
        self.log = shell_notify(
            '%s stage' % ('new clean' if clean else 'loaded'),
            more=dict(meta=name, clean=clean),
            verbose=self.__verbose
        )

    def load(self, mkey, mdesc, mdict=None, merge=False):
        '''
        Loads a dictionary into current meta

        :param mkey:
            Type of data to load.
            Is be used to reference the data from the 'header' within meta
        :param mdesc:
            Either filename of json-file to load or further description
            of imported data when `mdict` is used
        :param dict mdict:
            Directly pass data as dictionary instead of
            loading it from a json-file.
            Make sure to set `mkey` and `mdesc` accordingly
        :param merge:
            Merge received data into current meta or place it
            under 'import' within meta
        :returns:
            The loaded (or directly passed) content
        '''

        j = mdict if mdict else read_json(mdesc)
        if j and isinstance(j, dict):
            self.__meta['header'].update({mkey: mdesc})
            if merge:
                self.__meta = dict_merge(self.__meta, j)
            else:
                self.__meta['import'][mkey] = j
            self.log = shell_notify(
                'load %s data and %s it into meta' % (
                    'got' if mdict else 'read',
                    'merged' if merge else 'imported'
                ),
                more=dict(mkey=mkey, mdesc=mdesc, merge=merge),
                verbose=self.__verbose
            )
        return j

    @property
    def log(self):
        '''
        :param elem: Add a new log entry to the meta.

            * Can be anything.

            * The log is a dictionary with keys \
            generated from the output of :func:`util.system.get_timestamp` \
            and `elem` as value

        :returns: Current meta
        '''

        return self.__meta

    @log.setter
    def log(self, elem):
        '''
        .. seealso:: :attr:`log`
        '''

        if elem:
            self.__meta['log'].update({get_timestamp(precice=True): elem})
        mfile = self.__meta['header']['stage']

        self.__lock.acquire()
        try:
            j = read_json(mfile)
            if j != self.__meta:
                write_json(mfile, self.__meta)
        finally:
            self.__lock.release()
