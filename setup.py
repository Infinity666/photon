'''
photon_core
-----------

Photon is a backend utility for freifunk related gateway scripts

'''

from setuptools import setup
from os import path as _path
from info import __release__, __url__, __author__, __email__

__long_desc = __doc__
with open(_path.join(_path.dirname(_path.abspath(__file__)), 'Readme.rst'), 'r') as readme:
    __long_desc = readme.read()

setup(
    name='photon_core',
    version=__release__,
    url=__url__,
    license='BSD',
    author=__author__,
    author_email=__email__,
    description=__doc__,
    long_description=__long_desc,
    packages=['photon', 'photon.util', 'photon.tools'],
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
