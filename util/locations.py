
from os import path, environ, makedirs

def get_locations():

    from photon import IDENT

    util_dir = path.abspath(path.dirname(__file__))
    base_dir = path.dirname(util_dir)
    home_dir = path.expanduser('~')

    config_dir = path.join(environ.get('XDG_CONFIG_HOME', path.join(home_dir, '.config')), IDENT)
    data_dir = path.join(environ.get('XDG_DATA_HOME', path.join(home_dir, '.local', 'share')), IDENT)

    return {
        'base_dir': base_dir,
        'core_dir': path.join(base_dir, 'core'),
        'home_dir': home_dir,
        'config_dir': config_dir,
        'data_dir': data_dir,
        'backup_dir': path.join(data_dir, 'backups')
    }

def make_locations(locations=None, warn=True):

    from photon import warn_me
    from util.structures import to_list

    if not locations: locations = get_locations().values()
    locations = to_list(locations)

    for p in reversed(sorted(locations)):
        if not path.exists(p):
            makedirs(p)
            if warn: warn_me('path created %s' %(p))
