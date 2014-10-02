
def yaml_str_join(l, n):

    s = l.construct_sequence(n)
    return ''.join([str(i) for i in s])

def yaml_loc_join(l, n):

    from util.locations import get_locations
    from os import path

    locations = get_locations()
    s = l.construct_sequence(n)

    for num, seq in enumerate(s):
        if seq in locations: s[num] = '%s' %(locations[seq])
    return path.join(*s)

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

def to_list(i, the_keys=False):

    from photon import warn_me

    if isinstance(i, list): return i
    if isinstance(i, dict):
        res = list()
        for e in i.keys() if the_keys else i.values():
            if isinstance(e, dict): res += to_list(e)
            else: res.append(e)
        return res
    if isinstance(i, str): return [i]
    warn_me('type for %s uncovered: %s' %(i, type(i)))
