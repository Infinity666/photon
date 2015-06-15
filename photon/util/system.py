'''
.. |use_photon_m| replace:: This method is just a helper method within photon. If you need this functionality use :func:`photon.Photon.m` instead
'''


def shell_notify(msg, state=False, more=None, exitcode=None, verbose=True):
    '''
    A pretty long wrapper for a :py:func:`print` function. But this :py:func:`print` is the only one in Photon.

    .. note:: |use_photon_m|

    :param msg: The message to show
    :param state: The message will be prefixed with [`state`]

        * If ``False`` (default): Prefixed with ~
        * If ``None``: Prefixed with [WARNING]
        * If ``True``: Prefixed with [FATAL] and the exitcode will be set (see below)

    :param more: Something to add to the message (see below)

        * Anything you have. Just for further information.
        * Will be displayed after the message, pretty printed using :py:func:`pprint.pformat`

    :param exitcode: |appteardown| with given code
    :param verbose: Show message or not (see below)

        * If set to ``False``, you can use :func:`shell_notify` for the dictionary it returns.
        * Will be overruled if `exitcode` is set.

    :returns: A dictionary containing untouched `msg`, `more` and `verbose`
    '''

    from sys import exit as _exit
    from pprint import pformat as _pformat

    if state is True:
        state = '[FATAL]'
        exitcode = 23
    elif state is None:
        state = '[WARNING]'
    elif state is False:
        state = '~'
    else:
        state = '[%s]' % (str(state))
    m = ' %s %s' % (state, str(msg))
    if more:
        m += '\n\t' + _pformat(more).replace('\n', '\n\t')
    if verbose or isinstance(exitcode, int):
        print(m)
    if isinstance(exitcode, int):
        _exit(exitcode)
    return dict(message=msg, more=more, verbose=verbose)


def shell_run(cmd, cin=None, cwd=None, timeout=10, critical=True, verbose=True):
    '''
    Runs a shell command within a controlled environment.

    .. note:: |use_photon_m|

    :param cmd: The command to run

        * A string one would type into a console like :command:`git push -u origin master`.
        * Will be split using :py:func:`shlex.split`.
        * It is possible to use a list here, but then no splitting is done.

    :param cin: Add something to stdin of `cmd`
    :param cwd: Run `cmd` insde specified current working directory
    :param timeout: Catch infinite loops (e.g. ``ping``). Exit after `timeout` seconds
    :param critical: If set to ``True``: |appteardown| on failure of `cmd`
    :param verbose: Show messages and warnings
    :returns: A dictionary containing the results from running `cmd` with the following:

            * 'command': `cmd`
            * 'stdin': `cin` (If data was set in `cin`)
            * 'cwd': `cwd` (If `cwd` was set)
            * 'exception': exception message (If an exception was thrown)
            * 'timeout': `timeout` (If a timeout exception was thrown)
            * 'stdout': List from stdout (If any)
            * 'stderr': List from stderr (If any)
            * 'returncode': The returncode (If not any exception)
            * 'out': The most urgent message as joined string. ('exception' > 'stderr' > 'stdout')
    '''

    from shlex import split as _split
    from subprocess import Popen as _Popen, PIPE as _PIPE, TimeoutExpired as _TimeoutExpired

    res = dict(command=cmd)
    if cin:
        cin = str(cin)
        res.update(dict(stdin=cin))
    if cwd:
        res.update(dict(cwd=cwd))

    if isinstance(cmd, str):
        cmd = _split(cmd)

    try:
        p = _Popen(cmd, stdin=_PIPE, stdout=_PIPE, stderr=_PIPE, bufsize=1, cwd=cwd, universal_newlines=True)
    except Exception as ex:
        res.update(dict(exception=str(ex)))
    else:

        try:
            out, err = p.communicate(input=cin, timeout=timeout)
            if out:
                res.update(dict(stdout=[o for o in out.split('\n') if o]))
            if err:
                res.update(dict(stderr=[e for e in err.split('\n') if e]))
            res.update(dict(returncode=p.returncode))

        except _TimeoutExpired as ex:
            res.update(dict(exception=str(ex), timeout=timeout))
            p.kill()
        except Exception as ex:
            res.update(dict(exception=str(ex)))

    o = res.get('exception') or '\n'.join(res.get('stderr') or res.get('stdout', ''))
    res.update(out=o)

    if res.get('returncode', -1) != 0:
        res.update(dict(critical=critical))

        shell_notify(
            'error in shell command \'%s\'' % (res.get('command')),
            state=True if critical else None,
            more=res,
            verbose=verbose
        )

    return res


def get_timestamp(time=True, precice=False):
    '''
    What time is it?

    :param time: Append ``-%H.%M.%S`` to the final string.
    :param precice: Append ``-%f`` to the final string. Is only recognized when `time` is set to ``True``
    :returns: A timestamp string of now in the format ``%Y.%m.%d-%H.%M.%S-%f``

    .. seealso:: `strftime.org <http://strftime.org/>`_ is awesome!
    '''

    from datetime import datetime as _datetime

    f = '%Y.%m.%d'
    if time:
        f += '-%H.%M.%S'
        if precice:
            f += '-%f'
    return _datetime.now().strftime(f)


def get_hostname():
    '''
    Determines the current hostname by probing  ``uname -n``. Falls back to ``hostname`` in case of problems.

    |appteardown| if both failed (usually they don't but consider this if you are debugging weird problems..)

    :returns: The hostname as string. Domain parts will be split off
    '''

    h = shell_run('uname -n', critical=False, verbose=False)
    if not h:
        h = shell_run('hostname', critical=False, verbose=False)
    if not h:
        shell_notify('could not retrieve hostname', state=True)
    return str(h.get('out')).split('.')[0]
