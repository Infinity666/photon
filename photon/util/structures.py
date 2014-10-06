
def yaml_str_join(l, n):

    s = l.construct_sequence(n)
    return ''.join([str(i) for i in s])

def yaml_loc_join(l, n):

    from os import path as _path
    from .locations import get_locations

    locations = get_locations()
    s = l.construct_sequence(n)

    for num, seq in enumerate(s):
        if seq in locations: s[num] = '%s' %(locations[seq])
    return _path.join(*s)

def dict_merge(o, v):

    from copy import deepcopy as _deepcopy

    if not isinstance(v, dict):
        return v
    res = _deepcopy(o)
    for key in v.keys():
        if res.get(key) and isinstance(res[key], dict):
            res[key] = dict_merge(res[key], v[key])
        else:
            res[key] = _deepcopy(v[key])
    return res

def to_list(i, use_keys=False):

    from .system import notify

    if not i: return []
    if isinstance(i, str): return [i]
    if isinstance(i, list): return i
    if isinstance(i, dict):
        res = list()
        for e in i.keys() if use_keys else i.values():
            if isinstance(e, dict): res += to_list(e)
            else: res.append(e)
        return res
    notify('type for %s uncovered' %(i), state=True, more=type(i))
