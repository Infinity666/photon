.. include:: shared.rst

.. _core:

The core
========

All three modules depend on the :ref:`util`:

.. seealso:: |allutil|

:ref:`settings` and :ref:`meta` could be used independently or both together.

Bundling :ref:`Settings` and :ref:`Meta` together plus adding the :ref:`tools`, :ref:`photon` provides a interface to use in your scripts.

.. seealso:: |alltools|


.. _settings:

Settings
--------

.. automodule:: settings
    :members:
    :undoc-members:
    :private-members:


.. _settings_file_example:

Example Settings File
^^^^^^^^^^^^^^^^^^^^^

.. rubric:: config.sample.yaml

.. literalinclude:: ../examples/config.sample.yaml
    :linenos:
    :language: yaml

.. seealso:: The `wikipedia page on YAML <http://en.wikipedia.org/wiki/YAML>`_ for some syntax reference.

.. seealso::

    * `!loc_join`: :func:`util.structures.yaml_loc_join` (get locations by keyword and join paths)
    * `!str_join`: :func:`util.structures.yaml_str_join` (get variables by keyword and join strings)

.. seealso:: |allexamples|


.. _meta:

Meta
----

.. automodule:: meta
    :members:
    :undoc-members:
    :private-members:


.. _photon:

Photon
------

.. automodule:: photon
    :members:
    :undoc-members:
    :private-members:
