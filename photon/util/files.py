
def read_file(filename):

    from os import path as _path

    if filename and _path.exists(filename):
        with open(filename, 'r') as f:
            return f.read()

def read_yaml(filename, add_constructor=None):

    import yaml as _yaml

    y = read_file(filename)
    if add_constructor:
        if not isinstance(add_constructor, list):
            add_constructor = [add_constructor]
        for a in add_constructor:
            _yaml.add_constructor(*a)
    if y: return _yaml.load(y)

def read_json(filename):

    from json import loads as _loads

    j = read_file(filename)
    if j: return _loads(j)

def write_file(filename, content):

    from os import path as _path

    if filename and _path.exists(_path.dirname(filename)) and content:
        with open(filename, 'w') as f:
            return f.write(content)

def write_yaml(filename, content):

    import yaml as _yaml

    y = _yaml.dump(content, indent=4, default_flow_style=False)
    if y: return write_file(filename, y)

def write_json(filename, content):

    from json import dumps as _dumps

    j = _dumps(content, indent=4, sort_keys=True)
    if j: return write_file(filename, j)

def copy_location(src, tgt, move=False, verbose=True):

    from os import path as _path
    from shutil import rmtree as _rmtree

    def cpy(s, t):

        from shutil import copy2 as _copy2, copytree as _copytree
        from .locations import locate_file

        if not _path.isdir(s):
            return _copy2(s, locate_file(t, create_in=_path.dirname(t), verbose=verbose))
        if _path.exists(t): t = _path.join(t, _path.basename(s))
        return _copytree(s, t)

    res = cpy(src, tgt)
    if move: res = _rmtree(src)
    return res
