
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

def change_location(src, tgt, move=True, verbose=True):

    from os import path as _path
    from shutil import rmtree as _rmtree

    def cpy(s, t):

        from shutil import copy2 as _copy2, copytree as _copytree

        if not _path.isdir(s):
            return _copy2(s, search_location(t, create_in=_path.dirname(t), verbose=verbose))
        if _path.exists(t): t = _path.join(t, _path.basename(s))
        return _copytree(s, t)

    if tgt: res = cpy(src, tgt)
    if move: res = _rmtree(src)
    return res
