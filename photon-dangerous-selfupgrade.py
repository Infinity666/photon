#!/usr/bin/env python3

from argparse import ArgumentParser
from os import path

from photon import Photon


def argparse():
    parser = ArgumentParser(
        prog='photon selfupgrade',
        description='Upgrade photon_core and one to many repositories',
        epilog='You really _want_ to see the world burn or what?! Be careful!',
        add_help=True
    )
    parser.add_argument(
        '--sudo', '-s',
        action='store_true',
        default=False,
        help='use sudo to upgrade photon_core'
    )
    parser.add_argument(
        '--repos', '-r',
        nargs='*',
        help='List to the basepath of additional git repositories to update'
    )
    return parser.parse_args()


def main(sudo, repos=None):
    photon = Photon(
        dict(sudo=sudo, repos=repos),
        config=None,
        meta='photon_selfupgrade.json'
    )
    settings = photon.settings.get
    if settings['repos']:
        for repo in settings['repos']:
            if path.exists(repo) and path.exists(path.join(repo, '.git')):
                photon.git_handler(repo)._pull()
            else:
                photon.m('skipping non repo', more=dict(repo=repo))

    upres = photon.m(
        'attempting selfupgrade',
        cmdd=dict(
            cmd='%s pip3 install -U --pre photon_core' % (
                'sudo' if sudo else ''
            )
        ),
        more=dict(sudo=sudo),
        critical=False
    )
    if upres.get('returncode') == 0:
        photon.m('all went well')
    else:
        photon.m('I am dead! ' * 23, state=True)

if __name__ == '__main__':
    args = argparse()

    main(args.sudo, args.repos)
