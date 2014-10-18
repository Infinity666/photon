
from os import path as _path

def get_locations():

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
        :param src: source location where to copy/move from
        :param tgt: target location where to copy/move to
        :param move: deletes original after copy
        :param verbose: show warnings

        .. note:: set `tgt` explicit to ``None`` and `move` to ``True`` to delete locations

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
