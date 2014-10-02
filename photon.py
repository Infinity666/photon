
IDENT = 'photon'

def stop_me(reason, exitcode=23):
    from sys import exit
    print('[FATAL] - %s' %(str(reason)))
    exit(exitcode)

def warn_me(reason):
    print('[WARNING] - %s' %(str(reason)))

if __name__ == '__main__':
    stop_me('hahaha... NEIN!', exitcode=0)

from pprint import pprint

class Photon(object):
    def __init__(self):
        super().__init__()

        from core.settings import Settings
        self.settings = Settings()

        from core.meta import Meta
        self.meta = Meta()

    def __del__(self):
        print('end of %s' %(IDENT))

