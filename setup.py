'''
Photon
------

Photon is a backend for developing freifunk related scripts

'''

from setuptools import setup
from photon import __version__, __url__, __author__, __email__

setup(
    name='photon_core',
    version=__version__,
    url=__url__,
    license='BSD',
    author=__author__,
    author_email=__email__,
    description='A backend for developing freifunk related scripts',
    long_description=__doc__,
    packages=['photon', 'photon.util'],
    include_package_data=True,
    zip_safe=False,
    platforms='posix',
    install_requires=['PyYAML'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Telecommunications Industry',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Networking',
        'Topic :: System :: Systems Administration',
    ],
)
