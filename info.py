'''

Photon as a Package
-------------------

Photon is available as *photon_core* from `pypi <https://pypi.python.org/pypi/photon_core/>`_.

(The package is called ``photon_core`` because photon was already taken :/ )

'''


def pkg_name():
    '''photon_core'''
    return pkg_name.__doc__

def version():
    '''0.1'''
    return version.__doc__

def release():
    '''a8'''
    return version.__doc__ + release.__doc__

def url():
    '''https://github.com/spookey/photon/'''
    return url.__doc__

def __contributors():
    '''
Max Mütze
Thomas Schneidereith
Gerlinde Girlande
& Frieder Griesshammer
    '''
    return __contributors.__doc__.strip().split('\n')

def __author():
    return __contributors()[-1].replace('& ', '')

def __email():
    '''frieder.griesshammer@der-beweis.de'''
    return __email.__doc__

def __contributors_str():
    return ', '.join(__contributors()).replace(', &', ' &')
