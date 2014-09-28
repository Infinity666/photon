
from os import path

LOCATIONS = {
    'coredir': path.abspath(path.dirname(__file__)),
    'basedir': path.abspath(path.dirname(path.dirname(__file__)))
}

def locate_file(filename, critical=True):
    from sys import exit

    if filename:
        for p in [path.join(folder, filename) for folder in LOCATIONS.values()]:
            if path.exists(p):
                return p

    print('warning - file not found: %s' %(filename))
    return exit(2) if critical else None

