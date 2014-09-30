
IDENT = 'photon'

def stop_me(reason, exitcode=23):
    from sys import exit
    print('[FATAL] - %s' %(str(reason)))
    exit(exitcode)

def warn_me(reason):
    print('[WARNING] - %s' %(str(reason)))

if __name__ == '__main__':
    stop_me('hahaha... NEIN!', exitcode=0)

from core.settings import Settings

class Photon(object):
    def __init__(self):
        super().__init__()
        self.s = Settings()

    def __del__(self):
        pass

