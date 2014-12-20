
class Meta(object):
    '''
    Meta is a class which bounds to an actual json-file on disk. It provides a logger storing the entries in that json-file.

    It is also possible to import contents. By staging out to a different directory meta-files are left behind for further debugging or to see what was going on.

    :param meta: Initial, clean meta file to use. See :meth:`stage` for more
    :param verbose: Sets the `verbose` flag for the underlying :ref:`util` functions
    '''
    def __init__(self, meta='meta.json', verbose=True):

        super().__init__()

        from random import randint as _randint
        from photon import IDENT
        from .util.system import get_timestamp

        self.__verbose = verbose
        self._m = {
            'header': {
                'ident': '%s-%4X' %(IDENT, _randint(0x1000, 0xffff)),
                'initialized': get_timestamp(),
                'verbose': verbose
            },
            'import': dict(),
            'log': dict()
        }
        self.stage(meta, clean=True)

    def stage(self, s, clean=False):
        '''
        Switch stage

        :param s: Filename of new meta file. |filelocate|

            * File must not already exist, will be created in 'data_dir' from :func:`util.locations.get_locations`
            * Can also be a full path to place it anywhere desired

        :param clean: What to do with preexisting meta files?

            * ``False``: Merge current meta with preexisting one
            * ``True``: Replace preexisting meta with current one
        '''

        from .util.locations import search_location
        from .util.system import shell_notify

        s = search_location(s, create_in='data_dir')
        if not clean: self.load('stage', s, merge=True)

        self._m['header'].update({'stage': s})
        self.log = shell_notify(
            '%s stage' %('new clean' if clean else 'loaded'),
            more=dict(meta=s, clean=clean),
            verbose=self.__verbose
        )

    def load(self, mkey, mdesc, mdict=None, merge=False):
        '''
        Loads a dictionary into current meta

        :param mkey: Type of data to load. Is be used to reference the data from the 'header' within meta
        :param mdesc: Either filename of json-file to load or further description of imported data when `mdict` is used
        :param dict mdict: Directly pass data as dictionary instead of loading it from a json-file. Make sure to set `mkey` and `mdesc` accordingly
        :param merge: Merge received data into current meta or place it under 'import' within meta
        :returns: The loaded (or directly passed) content
        '''

        from .util.files import read_json
        from .util.structures import dict_merge
        from .util.system import shell_notify

        j = mdict if mdict else read_json(mdesc)
        if j and isinstance(j, dict):
            self._m['header'].update({mkey: mdesc})
            if merge: self._m = dict_merge(self._m, j)
            else: self._m['import'][mkey] = j
            self.log = shell_notify(
                'load %s data and %s it into meta' %('got' if mdict else 'read', 'merged' if merge else 'imported'),
                more=dict(mkey=mkey, mdesc=mdesc, merge=merge),
                verbose=self.__verbose
            )
        return j

    @property
    def log(self):
        '''
        :param elem: Add a new log entry to the meta.

            * Can be anything.
            * The log is a dictionary with keys generated from the output of :func:`util.system.get_timestamp` and `elem` as value

        :returns: Current meta
        '''

        return self._m

    @log.setter
    def log(self, elem):
        '''
        .. seealso:: :attr:`log`
        '''

        from threading import Lock
        from .util.files import read_json, write_json
        from .util.system import get_timestamp

        if elem: self._m['log'].update({get_timestamp(precice=True): elem})
        mfile = self._m['header']['stage']

        lock = Lock()
        with lock:
            j = read_json(mfile)
            if j != self._m: write_json(mfile, self._m)
