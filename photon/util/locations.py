'''
.. glossary::

    location
        Most functions do not treat files and folders different.
        This is why we use the expression `location` here.

.. |params_locations_dict| replace:: If `locations` is not a list, but a dictionary, all values in the dictionary will be used (as specified in :meth:`util.structures.to_list`)
.. |param_locations_none| replace:: If `locations` is set to ``None`` (by default), it will be filled with the output of :meth:`get_locations`.
'''

from os import path as _path

def get_locations():
    '''
    Compiles default locations

    :returns: A dictionary with folders as values.

    The keys are as following:

    * `home_dir`: Your home-directory (``~``)
    * `call_dir`: Where you called the first Python script from. (``argv[0]``)
        * Mostly used to locate the configuration within the same folder.
    * `conf_dir`: The `XDG_CONFIG_HOME`-directory + ``photon`` (``~/.config/photon``)
    * `data_dir`: The `XDG_DATA_HOME`-directory + ``photon`` (``~/.local/share/photon``)
    * `backup_dir`: The `data_dir` + ``backups``

    .. note::
        Both :meth:`search_location` and :meth:`make_locations` have the argument `locations`.

        |param_locations_none|
    '''

    from os import environ as _environ
    from sys import argv as _argv
    from photon import IDENT

    home_dir = _path.expanduser('~')
    conf_dir = _path.join(_environ.get('XDG_CONFIG_HOME', _path.join(home_dir, '.config')), IDENT)
    data_dir = _path.join(_environ.get('XDG_DATA_HOME', _path.join(home_dir, '.local', 'share')), IDENT)

    return {
        'home_dir': home_dir,
        'call_dir': _path.dirname(_path.abspath(_argv[0])),
        'conf_dir': conf_dir,
        'data_dir': data_dir,
        'backup_dir': _path.join(data_dir, 'backups')
    }

def make_locations(locations=None, verbose=True):
    '''
    Creates folders

    :param locations: A list of folders to create (can be a dictionary, see note below)
    :param verbose: Warn if any folders were created

    .. note::

        |params_locations_dict|

        |param_locations_none|
    '''

    from os import makedirs as _makedirs
    from .system import shell_notify
    from .structures import to_list

    if not locations: locations = get_locations().values()
    locations = to_list(locations)

    r = list()
    for p in reversed(sorted(locations)):
        if not _path.exists(p):
            _makedirs(p)
            r.append(p)
    if verbose and len(r) > 0: shell_notify('path created', state=None, more=r)
    return r

def search_location(loc, locations=None, critical=False, create_in=None, verbose=True):
    '''
    Locates files

    :param loc: Filename to search
    :param locations: A list of possible locations to search within (can be a dictionary, see note below)
    :param critical: Exit whole script if file was not found (see `state`-parameter in :meth:`util.system.shell_notify`)
    :param create_in: If `loc` was not found, the folder `create_in` is created. If `locations` is a dictionary, `create_in` can also specify a key of `locations`. The value will be used then.
    :param verbose: Pass verbose flag to :meth:`make_locations`

    .. note::

        |params_locations_dict|

        |param_locations_none|
    '''

    from .system import shell_notify
    from .structures import to_list

    if not locations: locations = get_locations()

    for p in reversed(sorted(to_list(locations))):
        f = _path.join(p, loc)
        if _path.exists(f): return f

    if _path.exists(_path.abspath(_path.expanduser(loc))): return _path.abspath(_path.expanduser(loc))

    if critical: shell_notify('could not locate' %(loc), state=True, more=dict(file=loc, locations=locations))
    if create_in:
        c = locations[create_in] if isinstance(locations, dict) and locations.get(create_in) else create_in
        make_locations(locations=[c], verbose=verbose)
        return _path.join(c, loc)

def change_location(src, tgt, move=False, verbose=True):
    '''
    Copies/moves/deletes locations

    :param src: source location where to copy from
    :param tgt: target location where to copy to
    :param move: deletes original after copy (a.k.a. move)
    :param verbose: show warnings

    .. note:: set `tgt` explicit to ``None`` and `move` to ``True`` to delete locations. (be careful!!1!)
    '''

    from os import path as _path, listdir as _listdir, remove as _remove
    from shutil import copy2 as _copy2, rmtree as _rmtree
    from .system import shell_notify

    if _path.exists(src):
        if _path.isfile(src):
            _copy2(src, search_location(tgt, create_in=_path.dirname(tgt), verbose=verbose))
        else:
            for l in _listdir(src): change_location(_path.abspath(_path.join(src, l)), _path.abspath(_path.join(tgt, l)))

        if move: _rmtree(src) if _path.isdir(src) else _remove(src)
        if verbose: shell_notify(
            '%s location' %('deleted' if not tgt and move else 'moved' if move else 'copied'),
            more=dict(src=src, tgt=tgt)
        )
