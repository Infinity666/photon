
def join(loader, node):
    seq = loader.construct_sequence(node)
    return ''.join([str(i) for i in seq])

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
    from core.locations import LOCATIONS, locate_file

    res = {'common': LOCATIONS}
    d, c = None, None

    df = locate_file(defaults)
    if df: d = read_yaml(df, add_constructor=('!join', join,))
    if d: res = dict_merge(res, d)

    cf = locate_file(config, critical=False)
    if cf: c = read_yaml(cf)
    if c: res = dict_merge(res, c)

    return res
