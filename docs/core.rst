.. include:: shared.rst

.. _core:

The core
========

All three modules depend on the :ref:`utility`:

.. seealso:: |allutil|

:ref:`settings` and :ref:`meta` could be used independently or both together.

Bundling :ref:`Settings` and :ref:`Meta` together plus adding :ref:`tools` handlers, :ref:`photon` provides a simple, yet powerful interface.

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

.. rubric:: config.sample.yaml

.. literalinclude:: ../examples/config.sample.yaml
    :linenos:
    :language: yaml

.. seealso:: The `wikipedia page on YAML <http://en.wikipedia.org/wiki/YAML>`_ for some syntax reference.

.. seealso::

    * `!loc_join`: :meth:`util.structures.yaml_loc_join` (get system locations and join paths)
    * `!str_join`: :meth:`util.structures.yaml_str_join` (join strings)

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
