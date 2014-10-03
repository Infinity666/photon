
from os import path

def read_file(filename):
    if filename and path.exists(filename):
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
    if filename and path.exists(path.dirname(filename)) and content:
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
