
def string_join(loader, node):

    seq = loader.construct_sequence(node)
    return ''.join([str(i) for i in seq])

def location_join(loader, node):

    from core.locations import get_locations
    from os import path

    locations = get_locations()
    seq = loader.construct_sequence(node)

    for num, s in enumerate(seq):
        if s in locations:
            seq[num] = '%s' %(locations[s])
    return path.join(*seq)

def dict_merge(o, v):

    from copy import deepcopy

    if not isinstance(v, dict):
        return v
    res = deepcopy(o)
    for key in v.keys():
        if key in res and isinstance(res[key], dict):
            res[key] = dict_merge(res[key], v[key])
        else:
            res[key] = deepcopy(v[key])
    return res

def load_settings(defaults='defaults.yaml', config='config.yaml'):

    from core.files import read_yaml
    from core.locations import get_locations, locate_file, make_dirs

    res = {'locations': get_locations()}
    d, c = None, None

    make_dirs()

    df = locate_file(defaults)
    if df: d = read_yaml(df, add_constructor=[('!location_join', location_join,), ('!string_join', string_join,),])
    if d: res = dict_merge(res, d)

    cf = locate_file(config, critical=False)
    if cf: c = read_yaml(cf, add_constructor=('!location_join', location_join,))
    if c: res = dict_merge(res, c)

    return res
