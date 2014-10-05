
__ident__ = 'photon'

__version__ = '0.1a1'
__url__ = 'http://github.com/spookey/photon/'
__author__ = 'Frieder Griesshammer'
__email__ = 'frieder.griesshammer@der-beweis.de'
__contributors__ = [
    '%s (%s)' %(__author__, __email__),
]
from .settings import Settings
from .meta import Meta

from .photon import Photon
