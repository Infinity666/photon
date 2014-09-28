
from os import path

def read_file(filename):
    if path.exists(filename):
        with open(filename, 'r') as f:
            return f.read()

def read_yaml(filename, add_constructor=None):
    import yaml
    y = read_file(filename)
    if add_constructor: yaml.add_constructor(*add_constructor)
    if y: return yaml.load(y)
