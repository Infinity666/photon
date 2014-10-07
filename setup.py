'''
photon_core
-----------

``photon_core`` is the name of Photon on pypi.
Photon is a module which helps developing freifunk related scripts

'''

from setuptools import setup
from os import path as _path
from info import __pkg_name__, __release__, __url__, __author__, __email__

__long_desc = __doc__
with open(_path.join(_path.dirname(_path.abspath(__file__)), 'Readme.rst'), 'r') as readme:
    __long_desc = readme.read() + __doc__

setup(
    name=__pkg_name__,
    version=__release__,
    url=__url__,
    download_url='%s/archive/%s.tar.gz' %(__url__, __release__),
    license='BSD',
    author=__author__,
    author_email=__email__,
    description=__doc__,
    long_description=__long_desc,
    packages=['photon', 'photon.util', 'photon.tools'],
    include_package_data=True,
    zip_safe=False,
    platforms='posix',
    scripts=['photon_settings_shell.py'],
    provides=[__pkg_name__],
    requires=['PyYAML (>=3.11)'],
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
