'''
.. |yaml_loader_returns| replace::
    with keywords extended. Used in :func:`settings.Settings.load`
.. |yaml_loader_seealso| replace::
    The YAML files mentioned in |allexamples|
'''
from copy import deepcopy as _deepcopy
from os import path as _path


def yaml_str_join(l, n):
    '''
    YAML loader to join strings

    The keywords are as following:

    * `hostname`: Your hostname (from :func:`util.system.get_hostname`)

    * `timestamp`: Current timestamp (from :func:`util.system.get_timestamp`)

    :returns:
        A `non character` joined string |yaml_loader_returns|

    .. note::
        Be careful with timestamps when using a `config` in :ref:`settings`.

    .. seealso:: |yaml_loader_seealso|
    '''

    from photon.util.system import get_hostname, get_timestamp

    s = l.construct_sequence(n)

    for num, seq in enumerate(s):
        if seq == 'hostname':
            s[num] = '%s' % (get_hostname())
        elif seq == 'timestamp':
            s[num] = '%s' % (get_timestamp())
    return ''.join([str(i) for i in s])


def yaml_loc_join(l, n):
    '''
    YAML loader to join paths

    The keywords come directly from :func:`util.locations.get_locations`.
    See there!

    :returns:
        A `path seperator` (``/``) joined string |yaml_loader_returns|

    .. seealso:: |yaml_loader_seealso|
    '''

    from photon.util.locations import get_locations

    locations = get_locations()
    s = l.construct_sequence(n)

    for num, seq in enumerate(s):
        if seq in locations:
            s[num] = '%s' % (locations[seq])
    return _path.join(*s)


def dict_merge(o, v):
    '''
    Recursively climbs through dictionaries and merges them together.

    :param o:
        The first dictionary
    :param v:
        The second dictionary
    :returns:
        A dictionary (who would have guessed?)

    .. note::
        Make sure `o` & `v` are indeed dictionaries,
        bad things will happen otherwise!
    '''

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
    '''
    Converts items to a list.

    :param i: Item to convert

        * If `i` is ``None``, the result is an empty list

        * If `i` is 'string', the result won't be \
        ``['s', 't', 'r',...]`` rather more like ``['string']``

        * If `i` is a nested dictionary, the result will be a flattened list.

    :param use_keys:
        If i is a dictionary, use the keys instead of values
    :returns:
        All items in i as list
    '''

    from photon.util.system import shell_notify

    if not i:
        return []
    if isinstance(i, str):
        return [i]
    if isinstance(i, list):
        return i
    if isinstance(i, dict):
        res = list()
        for e in i.keys() if use_keys else i.values():
            res.append(to_list(e)) if isinstance(e, dict) else res.append(e)
        return res
    shell_notify('type for %s uncovered' % (i), state=True, more=type(i))
