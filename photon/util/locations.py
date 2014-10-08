
from os import path as _path

def get_locations():

    from os import environ as _environ
    from sys import argv as _argv
    from photon import __ident__

    home_dir = _path.expanduser('~')
    call_dir = _path.dirname(_path.abspath(_argv[0]))

    config_dir = _path.join(_environ.get('XDG_CONFIG_HOME', _path.join(home_dir, '.config')), __ident__)
    data_dir = _path.join(_environ.get('XDG_DATA_HOME', _path.join(home_dir, '.local', 'share')), __ident__)

    return {
        'home_dir': home_dir,
        'call_dir': call_dir,
        'config_dir': config_dir,
        'data_dir': data_dir
    }

def make_locations(locations=None, warn=True):

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
    if warn: shell_notify('path created', state=None, more=r)
    return r

def locate_file(filename, locations=None, critical=False, create_in=None):

    from .system import shell_notify
    from .structures import to_list

    if _path.exists(filename): return _path.abspath(_path.expanduser(filename))

    if not locations: locations = get_locations()

    for p in reversed(sorted(to_list(locations))):
        f = _path.join(p, filename)
        if _path.exists(f): return f

    if critical: shell_notify('filename %s not found', state=True, more=locations)
    if create_in:
        c = locations[create_in] if isinstance(locations, dict) and locations.get(create_in) else create_in
        make_locations(locations=[c])
        return _path.join(c, filename)

