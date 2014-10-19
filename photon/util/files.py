
def read_file(filename):
    '''
    Reads files

    :param filename: The full path of the file to read
    :returns: The content of the file as string (if `filename` exists)
    '''
    from os import path as _path

    if filename and _path.exists(filename):
        with open(filename, 'r') as f:
            return f.read()

def read_yaml(filename, add_constructor=None):
    '''
    Reads YAML files

    :param filename: The full path to the YAML file
    :param add_constructor: A list of yaml constructors (loaders)
    :returns: Loaded YAML content as represented data structure

    .. seealso:: :func:`util.structures.yaml_str_join`, :func:`util.structures.yaml_loc_join`
    '''

    import yaml as _yaml

    y = read_file(filename)
    if add_constructor:
        if not isinstance(add_constructor, list):
            add_constructor = [add_constructor]
        for a in add_constructor:
            _yaml.add_constructor(*a)
    if y: return _yaml.load(y)

def read_json(filename):
    '''
    Reads json files

    :param filename: The full path to the json file
    :returns: Loaded json content as represented data structure
    '''

    from json import loads as _loads

    j = read_file(filename)
    if j: return _loads(j)

def write_file(filename, content):
    '''
    Writes files

    :param filename: The full path of the file to write (enclosing folder must already exist)
    :param content: The content to write
    :returns: The size of the data written
    '''

    from os import path as _path

    if filename and _path.exists(_path.dirname(filename)) and content:
        with open(filename, 'w') as f:
            return f.write(content)

def write_yaml(filename, content):
    '''
    Writes YAML files

    :param filename: The full path to the YAML file
    :param content: The content to dump
    :returns: The size written
    '''

    import yaml as _yaml

    y = _yaml.dump(content, indent=4, default_flow_style=False)
    if y: return write_file(filename, y)

def write_json(filename, content):
    '''
    Writes json files

    :param filename: The full path to the json file
    :param content: The content to dump
    :returns: The size written
    '''

    from json import dumps as _dumps

    j = _dumps(content, indent=4, sort_keys=True)
    if j: return write_file(filename, j)
