#!/usr/bin/env python3

from argparse import ArgumentParser
from json import dumps
from os import path, sep
from pprint import pformat

from photon import Settings
from yaml import dump


def _p(s):
    print(s)


def _pp(s):
    return _p(pformat(s))


def _j(s):
    return _p(dumps(s, indent=4, sort_keys=True))


def _y(s):
    return _p(dump(s, indent=4, default_flow_style=False))


def _t(s, p=0):
    if isinstance(s, (str, int, float)):
        return _p('%s%s' % ('\t'*p, s))

    if isinstance(s, list):
        return [_t(t, p) for t in s]

    if isinstance(s, dict):
        for t, u in sorted(s.items()):
            _t(t, p)
            _t(u, p+1)
        return

FTYPES = {'j': _j, 'p': _p, 'pp': _pp, 't': _t, 'y': _y}


def fmt(structure, ftype):
    if ftype in FTYPES.keys():
        FTYPES[ftype](structure)


def argparse():
    parser = ArgumentParser(
        prog='photon settings tool',
        description='Reads photon settings files to display \
            and/or save the output',
        epilog='-.-',
        add_help=True
    )
    parser.add_argument(
        '--defaults', '-d',
        action='store',
        default='defaults.yaml',
        help='Specify defaults file to load'
    )
    parser.add_argument(
        '--config', '-c',
        action='store',
        default=None,
        help='Specify config file to load and writeback'
    )
    parser.add_argument(
        '--formatter', '-f',
        action='store',
        default='pp',
        choices=sorted(FTYPES.keys()),
        help='Use a formatter to print. \
            Choose between p_rint p_retty_p_rint (default), \
            j_son, y_aml or nested t_abs'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        default=False,
        help='Show info and warn messages'
    )
    parser.add_argument(
        'settings',
        nargs='*',
        help='Space separated list into settings'
    )
    return parser.parse_args()


def main(defaults, settings, config=None, verbose=True):
    res = Settings(defaults, config=config, verbose=verbose).get
    for s in settings:
        if s in res:
            res = res[s]
        else:
            return False
    return res


if __name__ == '__main__':
    args = argparse()

    if args.config and sep in args.config:
        args.config = path.abspath(path.expanduser(args.config))

    fmt(
        main(
            args.defaults, args.settings,
            config=args.config, verbose=args.verbose
        ),
        args.formatter
    )
