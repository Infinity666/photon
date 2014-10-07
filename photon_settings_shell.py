#!/usr/bin/env python3

def args():
    from argparse import ArgumentParser
    p = ArgumentParser(
        prog='photon settings shell',
        description='read photon settings from the shell',
        epilog='-.-',
        add_help=True
    )
    p.add_argument('--config', '-c', action='store', default='config.yaml', help='specify config file to load')
    p.add_argument('--summary', '-s', action='store', default='summary.yaml', help='specify summary file to load and writeback')
    p.add_argument('--verbose', '-v', action='store_true', default=False, help='show info and warn messages')
    p.add_argument('setting', nargs='*', help='space seperated list into settings')
    return p.parse_args()

def main():
    from photon import Settings
    a = args()
    res = Settings(config=a.config, summary=a.summary, verbose=a.verbose).get
    for s in a.setting:
        if s in res: res = res[s]
        else: return False
    return res

if __name__ == '__main__':
    print(main())
