'''
Photon - a shell backend as python module
''' # do not use restructured text here!

from setuptools import setup
from os import path as _path
from info import pkg_name, release, url, author, email

__long_desc = __doc__
with open(_path.join(_path.dirname(_path.abspath(__file__)), 'README.rst'), 'r') as readme:
    __long_desc = readme.read()

setup(
    name=pkg_name(),
    version=release(),
    url=url(),
    download_url='%sarchive/%s.tar.gz' %(url(), release()),
    license='BSD',
    author=author(),
    author_email=email(),
    description=__doc__,
    long_description=__long_desc,
    packages=['photon', 'photon.util', 'photon.tools'],
    include_package_data=True,
    zip_safe=False,
    platforms='posix',
    scripts=['photon-settings-tool.py', 'photon-dangerous-selfupgrade.py'],
    provides=[pkg_name()],
    install_requires=['PyYAML'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Telecommunications Industry',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Networking',
        'Topic :: System :: Systems Administration',
    ],
)
