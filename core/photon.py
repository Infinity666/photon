
if __name__ == '__main__':
    from sys import exit
    print('hahaha... NEIN!')
    exit(23)

from core.settings import load_settings

class Photon(object):
    def __init__(self):
        super().__init__()
        self.s = load_settings()

    def __del__(self):
        pass
