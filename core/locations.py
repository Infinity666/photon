
from os import path, environ, makedirs

def get_locations():

    from core.photon import IDENT

    core_dir = path.abspath(path.dirname(__file__))
    return {
        'base_dir': path.dirname(core_dir),
        'core_dir': core_dir,
        'home_dir': path.expanduser('~'),
        'config_dir': path.join(
            environ.get(
                'XDG_CONFIG_HOME',
                path.expanduser(path.join('~', '.config'))
            ), IDENT),
        'data_dir': path.join(
            environ.get(
                'XDG_DATA_HOME',
                path.expanduser(path.join('~', '.local', 'share'))
            ), IDENT)
    }

def locate_file(filename, locations=None, critical=True):

    from core.photon import stop_me, warn_me

    if not locations:
        locations = list(get_locations().values())
    if not isinstance(locations, list):
        locations = [locations]
    locations = [path.join(folder, filename) for folder in locations]
    if filename:
        for p in locations:
            if path.exists(p):
                return p
    err = 'file not found: %s\n\t%s' %(filename, '\n\t'.join(locations))
    stop_me(err) if critical else warn_me(err)

def make_dirs(locations=None):
    from core.photon import warn_me

    if not locations:
        locations = list(get_locations().values())
    if not isinstance(locations, list):
        locations = [locations]
    for p in locations:
        if not path.exists(p):
            makedirs(p)
            warn_me('path created %s' %(p))
