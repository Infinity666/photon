.. include:: shared.rst

.. _core:

The core
========

All three modules depend on the :ref:`backend`:

.. seealso:: |allutil|

:ref:`settings` and :ref:`meta` could be used independently or both together.

Bundling :ref:`Settings` and :ref:`Meta` together plus adding :ref:`frontend` handlers, :ref:`photon` provides a simple, yet powerful interface.

.. seealso:: |alltools|

.. note:: Rule of thumb - Always work through Photon itself.

.. _settings:

Settings
--------

.. automodule:: settings
    :members:
    :undoc-members:
    :private-members:
    :special-members: __init__

.. _settings file example:

Example Settings File
^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../config.sample.yaml
    :linenos:
    :language: yaml


.. seealso:: |allexamples|

.. _meta:

Meta
----

.. automodule:: meta
    :members:
    :undoc-members:
    :private-members:
    :special-members: __init__


.. _photon:

Photon
------

.. automodule:: photon
    :members:
    :undoc-members:
    :private-members:
    :special-members: __init__
