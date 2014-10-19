'''

.. topic:: The *info* file

    The *info* file is not vital to Photon, it just helps to share common values between documentation and the package builder (*setup* file).

'''

def pkg_name():
    '''
    :returns: The package name (on pypi)
    '''
    return 'photon_core'

def version():
    '''
    :returns: Current version string
    :current: |version|
    '''
    return '0.2'

def release():
    '''
    :returns: Current release string
    :current: |release|
    '''
    return version() + 'b0'

def url():
    '''
    :returns: The repo url (on github)
    '''
    return 'https://github.com/spookey/photon/'

def contributors():
    '''
    :returns: A list of all contributors
    '''
    return [
        '...',
        '& Frieder Griesshammer'
    ]

def author():
    ''':returns: The main author (last entry of :meth:`contributors`)'''
    return contributors()[-1].replace('& ', '')

def email():
    ''':returns: Main :meth:`author`'s mail'''
    return 'frieder.griesshammer@der-beweis.de'

def contributors_str():
    ''':returns: The :meth:`contributors` as comma joined string'''

    return ', '.join(contributors()).replace('..., &', '').replace(', &', ' &')
