
def shell_notif(msg, state=False, more=None, exitcode=None):

    from sys import exit as _exit
    from .structures import to_list

    if state == True:
        state = '[FATAL]'
        exitcode = 23
    elif state == None: state = '[WARNING]'
    elif state == False: state = '|'
    else: state = '[%s]' %(str(state))
    msg = '%s %s' %(state, str(msg))
    if more: msg += '\n\t%s' %('\n\t'.join([str(m) for m in to_list(more)]))
    print(msg)
    if exitcode and isinstance(exitcode, int): _exit(exitcode)

def shell_run(c, cin=None, cwd=None, timeout=10, critical=True):

    from shlex import split as _split
    from subprocess import Popen as _Popen, PIPE as _PIPE, TimeoutExpired as _TimeoutExpired

    res = {'command': c}
    if isinstance(c, str): c = _split(c)
    if cin: res.update({'stdin': cin})
    if cwd: res.update({'cwd': cwd})

    try: p = _Popen(c, stdin=_PIPE, stdout=_PIPE, stderr=_PIPE, bufsize=1, cwd=cwd, universal_newlines=True)
    except Exception as ex: res.update({'exception': ex})
    else:
        try:
            out, err = p.communicate(input=str(cin), timeout=timeout)
            if out: res.update({'stdout': [o for o in out.split('\n') if o]})
            if err: res.update({'stderr': [e for e in err.split('\n') if e]})
            res.update({'returncode': p.returncode})
        except _TimeoutExpired as ex: res.update({'exception': ex, 'timeout': timeout}); p.kill()
        except Exception as ex: res.update({'exception': ex})

    if res.get('returncode', -1) != 0:
        res.update({'critical': critical})
        e = res.get('exception')
        e = [str(e)] if e else [r for r in res.get('stderr') or res.get('stdout') if r]
        s = True if critical else None
        shell_notif('error in shell command \'%s\'' %(' '.join(c)), state=s, more=e)
    return res

def sh(c, cin=None, critical=True):

    res = shell_run(c, cin=cin, critical=critical)
    if res.get('returncode', -1) != 0: return False
    return res.get('stderr') or res.get('stdout')
