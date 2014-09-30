
from os import path

def get_files():

    from util.locations import get_locations

    locations = get_locations()
    return {
        'config': path.join(locations['config_dir'], 'config.yaml'),
        'defaults': path.join(locations['core_dir'], 'defaults.yaml'),
        'meta': path.join(locations['data_dir'], 'meta.yaml')
    }

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

def write_file(filename, content):
    if path.exists(path.dirname(filename)) and content:
        with open(filename, 'w') as f:
            return f.write(content)

def write_yaml(filename, content):

    import yaml

    y = yaml.dump(content, indent=4, default_flow_style=False)
    if y:
        write_file(filename, y)
