
def yaml_str_join(loader, node):

    seq = loader.construct_sequence(node)
    return ''.join([str(i) for i in seq])

def yaml_loc_join(loader, node):

    from util.locations import get_locations
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
