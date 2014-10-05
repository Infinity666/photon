
def stop_me(reason, exitcode=23):
    from sys import exit
    print('[FATAL] - %s' %(str(reason)))
    exit(exitcode)

def warn_me(reason):
    print('[WARNING] - %s' %(str(reason)))

def shell_run(c, cin=None, timeout=10, critical=True):

    from shlex import split as shsplit
    from subprocess import Popen, PIPE, TimeoutExpired

    res = {'command': c}
    if isinstance(c, str): c = shsplit(c)
    if cin: res.update({'stdin': cin})

    try: p = Popen(c, stdin=PIPE, stdout=PIPE, stderr=PIPE, bufsize=1, universal_newlines=True)
    except Exception as ex: res.update({'exception': ex})
    else:
        try:
            out, err = p.communicate(input=str(cin), timeout=timeout)
            if out: res.update({'stdout': [o for o in out.split('\n') if o]})
            if err: res.update({'stderr': [e for e in err.split('\n') if e]})
            res.update({'returncode': p.returncode})
        except TimeoutExpired as ex: res.update({'exception': ex, 'timeout': timeout}); p.kill()
        except Exception as ex: res.update({'exception': ex})

    if res.get('returncode', -1) != 0:
        res.update({'critical': critical})
        e = res.get('exception')
        e = [str(e)] if e else [r for r in res.get('stderr') or res.get('stdout') if r]
        e = 'error in shell command \'%s\'\n\t%s' %(' '.join(c), '\n\t'.join(e))
        stop_me(e) if critical else warn_me(e)
    return res

def sh(c, cin=None, critical=True):
    res = shell_run(c, cin=cin, critical=critical)
    if res.get('returncode', -1) != 0: return False
    return res.get('stderr') or res.get('stdout')
