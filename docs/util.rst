.. include:: shared.rst

.. _util:

Utility
=======

This is the toolbox used by :ref:`core`:

.. seealso:: |allcore|

As well as used by the :ref:`tools`:

.. seealso:: |alltools|

.. note:: If you have no explicit reason to do so do not use them directly. You

.. _util_files:

Files
-----

.. automodule:: util.files
    :members:
    :undoc-members:


.. _util_locations:

Locations
---------

.. automodule:: util.locations
    :members:
    :undoc-members:


.. _util_structures:

Structures
----------

.. automodule:: util.structures
    :members:
    :undoc-members:


.. _util_system:

System
------

.. automodule:: util.system
    :members:
    :undoc-members:

.. _util_system_shell_run_example:

shell_run Example
^^^^^^^^^^^^^^^^^

You can check the output of an potentionally unsafe `cmd` as following::

    r = shell_run('git log -n 10', critical=False, cwd='/my/repo')

    if not r.get('returncode'):
        print('exception occured: %s' %(r.get('exception')))
    else:
        if r.get('returncode') != 0:
            print('error occured (maybe not in git repo?): %s' %(r.get('stderr')))
        else:
            print('here is your log: %s' %(r.get('stdout')))

You can also directly compare against not equal zero, and use ``r.get('out')`` for the errormessage
(because the returncode is ``None`` on exception. ``None`` != 0 == ``True``)::

    r = shell_run('git log -n 10', critical=False, cwd='/my/repo')

    if r.get('returncode') != 0:
        print('computer says "no" (maybe not in git repo?): %s' %(r.get('out')))
    else:
        print('here is your log: %s' %(r.get('stdout')))

.. seealso:: :func:`util.system.shell_run`
