.. include:: shared.rst

.. _frontend:

Frontend tools
==============

This are the tools for the user using Photon. You should not directly use them, instead they will get provided to you by :ref:`core` (most commonly by :ref:`photon`):

.. seealso:: |allcore|

Some functionality here is bought from the :ref:`backend`:

.. seealso:: |allutil|

.. _git tool:

Git Tool
--------

.. automodule:: tools.git
    :members:
    :undoc-members:
    :private-members:
    :special-members: __init__


.. _mail tool:

Mail Tool
---------

.. automodule:: tools.mail
    :members:
    :undoc-members:
    :private-members:
    :special-members: __init__

.. _mail tool example:

Mail Tool Example
^^^^^^^^^^^^^^^^^

.. rubric:: sending_mail.sample.yaml

.. literalinclude:: ../examples/sending_mail.sample.yaml
    :linenos:
    :language: yaml

.. rubric:: sending_mail.sample.py

.. literalinclude:: ../examples/sending_mail.sample.py
    :linenos:
    :language: python3

.. seealso:: |allexamples|
