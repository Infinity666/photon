
def shell_notify(msg, state=False, more=None, exitcode=None, verbose=True):

    from sys import exit as _exit
    from pprint import pformat as _pformat

    if state == True:
        state = '[FATAL]'
        exitcode = 23
    elif state == None: state = '[WARNING]'
    elif state == False: state = '|'
    else: state = '[%s]' %(str(state))
    m = '%s %s' %(state, str(msg))
    if more: m += '\n\t' + _pformat(more).replace('\n', '\n\t')
    if verbose or isinstance(exitcode, int): print(m)
    if isinstance(exitcode, int): _exit(exitcode)
    return dict(message=msg, more=more, verbose=verbose)

def shell_run(cmd, cin=None, cwd=None, timeout=10, critical=True, verbose=True):

    from shlex import split as _split
    from subprocess import Popen as _Popen, PIPE as _PIPE, TimeoutExpired as _TimeoutExpired

    res = dict(command=cmd)
    if cin:
        cin = str(cin)
        res.update(dict(stdin=cin))
    if cwd: res.update(dict(cwd=cwd))

    if isinstance(cmd, str): cmd = _split(cmd)

    try: p = _Popen(cmd, stdin=_PIPE, stdout=_PIPE, stderr=_PIPE, bufsize=1, cwd=cwd, universal_newlines=True)
    except Exception as ex: res.update(dict(exception=str(ex)))
    else:

        try:
            out, err = p.communicate(input=cin, timeout=timeout)
            if out: res.update(dict(stdout=[o for o in out.split('\n') if o]))
            if err: res.update(dict(stderr=[e for e in err.split('\n') if e]))
            res.update(dict(returncode=p.returncode))
        except _TimeoutExpired as ex: res.update(dict(exception=str(ex),timeout=timeout)); p.kill()
        except Exception as ex: res.update(dict(exception=str(ex)))

    o = res.get('exception') or '\n'.join(res.get('stderr') or res.get('stdout', ''))
    res.update(out=o)

    if res.get('returncode', -1) != 0:
        res.update(dict(critical=critical))

        shell_notify(
            'error in shell command \'%s\'' %(res.get('command')),
            state=True if critical else None,
            more=res,
            verbose=verbose
        )

    return res

def get_timestamp(precice=False):

    from datetime import datetime as _datetime

    f = '%Y.%m.%d-%H.%M.%S'
    if precice: f += '-%f'
    return _datetime.now().strftime(f)

def get_hostname():

    h = shell_run('uname -n', critical=False, verbose=False)
    if not h: h = shell_run('hostname', critical=False, verbose=False)
    if not h: shell_notify('could not retrieve hostname', state=True)
    return str(h.get('out')).split('.')[0]


