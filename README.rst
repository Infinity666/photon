
Photon Intro
------------

It could be best described as a **shell backend as python module**

Contributions are highly welcome [#contributions]_, also feel free to use
the `issue tracker <http://github.com/spookey/photon/issues>`_ if you
encounter any problems.

:Repository: `github.com/spookey/photon <http://github.com/spookey/photon/>`_
:Documentation: `photon.readthedocs.org <http://photon.readthedocs.org/en/latest/>`_
:Package: `pypi.python.org/pypi/photon_core <https://pypi.python.org/pypi/photon_core/>`_

Examples
^^^^^^^^

The **/examples** directory contains some basic receipts on how to use Photon
in your scripts.

Photon helps at `Freifunk MWU <http://freifunk-mwu.de/>`_ to solve some tasks:

    * See our `collection of backend-scripts <https://github.com/freifunk-mwu/backend-scripts>`_ for some scripts using photon, running in production.
    * To automatically compile gluon firmware for routers, we wrote the `gluon builder <https://github.com/freifunk-mwu/gluon-builder-ffmwu>`_.

Installation
------------

Photon is available as package on pypi, it is called
``photon_core`` [#photon_core]_.

You can install/update the package via pip3 [#pip3]_:

.. code-block:: sh

    pip3 install photon_core

.. code-block:: sh

    pip3 install -U photon_core

.. topic:: Bleeding-Edge

    Development is still at an very early stage, expect anything to change
    any time.

    .. code-block:: sh

        pip3 install -U photon_core

    To update to some alpha or beta version (see *info* file)
    use *pip3* with the ``--pre`` switch.

.. topic:: Versions

    Tags in the git repository will be released as a new pypi package version.
    Versions of a pypi package has always it's git tag.
    And vice versa.

    Not every version increase will be tagged/released.
    I will only do so if I feel the urge to do so.

.. [#contributions] Teach me how to write good code, help me to improve.
.. [#photon_core] because photon itself was already taken :/
.. [#pip3] Photon is written in python3 ~ be careful with easy_install
