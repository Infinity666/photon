
from os import path

def read_file(filename):
    if path.exists(filename):
        with open(filename, 'r') as f:
            return f.read()

def read_yaml(filename, add_constructor=None):

    import yaml

    y = read_file(filename)
    if add_constructor:
        if not isinstance(add_constructor, list):
            add_constructor = [add_constructor]
        for a in add_constructor:
            yaml.add_constructor(*a)
    if y: return yaml.load(y)

def read_json(filename):

    from json import loads

    j = read_file(filename)
    if j: return loads(j)

def write_file(filename, content):
    if path.exists(path.dirname(filename)) and content:
        with open(filename, 'w') as f:
            return f.write(content)

def write_yaml(filename, content):

    import yaml

    y = yaml.dump(content, indent=4, default_flow_style=False)
    if y: return write_file(filename, y)

def write_json(filename, content):

    from json import dumps

    j = dumps(content, indent=4, sort_keys=True)
    if j: return write_file(filename, j)

def locate_file(filename, locations=None, critical=False, create_in=None):

    from photon import stop_me
    from util.locations import get_locations, make_locations
    from util.structures import to_list

    if path.exists(filename): return filename

    if not locations: locations = get_locations()
    locations = to_list(locations)

    for p in reversed(sorted(locations)):
        f = path.join(p, filename)
        if path.exists(f): return f

    if critical: stop_me('filename %s not found\n\t%s' %('\n\t'.join(locations)))
    if create_in:
        l = get_locations()
        c = l[create_in] if create_in in l else create_in
        make_locations(locations=[c])
        return path.join(c, filename)

