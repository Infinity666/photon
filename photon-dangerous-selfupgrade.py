#!/usr/bin/env python3

def args():
    from argparse import ArgumentParser
    p = ArgumentParser(
        prog='photon selfupgrade',
        description='Upgrade photon_core and if chosen one to many repositories',
        epilog='You really _want_ to see the world burn or what?! Be careful!',
        add_help=True
    )
    p.add_argument('--sudo', '-s', action='store_true', default=False, help='use sudo to upgrade photon_core')
    p.add_argument('--repos', '-r', nargs='*', help='List to the basepath of additional git repositories to update')
    return p.parse_args()

def main(sudo, repos=None):
    from os import path
    from photon import Photon

    p = Photon(dict(sudo=sudo, repos=repos), config=None, meta='photon_selfupgrade.json')
    s = p.settings.get
    if s['repos']:
        for repo in s['repos']:
            if path.exists(repo) and path.exists(path.join(repo, '.git')):
                p.git_handler(repo)._pull
            else: p.m('skipping non repo', more=dict(repo=repo))

    p.m('attempting selfupgrade',
        cmdd=dict(cmd='%s pip3 install -U --pre photon_core' %('sudo' if sudo else '')),
        more=dict(sudo=sudo, cry='I could die now..'),
        critical=False
    )

if __name__ == '__main__':
    a = args()

    main(a.sudo, a.repos)
