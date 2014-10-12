'''

.. topic:: The *info* file

    The *info* file is not vital to Photon, it just helps to share common values between documentation and the package builder (*setup* file).

'''


def pkg_name():
    '''photon_core'''
    return pkg_name.__doc__

def version():
    '''0.1'''
    return version.__doc__

def release():
    '''b1'''
    return version.__doc__ + release.__doc__

def url():
    '''https://github.com/spookey/photon/'''
    return url.__doc__

def __contributors():
    '''
...
& Frieder Griesshammer
    '''
    return __contributors.__doc__.strip().split('\n')

def __author():
    return __contributors()[-1].replace('& ', '')

def __email():
    '''frieder.griesshammer@der-beweis.de'''
    return __email.__doc__

def __contributors_str():
    return ', '.join(__contributors()).replace('..., &', '').replace(', &', ' &')
