
class Photon(object):
    def __init__(self, config='config.yaml', summary='summary.yaml', meta='meta.json', verbose=True):

        super().__init__()

        from atexit import register as _register
        from photon import Settings, Meta, __ident__
        from .util.system import notify

        self.settings = Settings(config=config, summary=summary, verbose=verbose)
        self.meta = Meta(meta=meta, verbose=verbose)
        self.__verbose = verbose

        @_register
        def __copy_settings_to_meta_and_say_goodbye():

            if self.meta:
                if self.settings: self.meta.load('%s settings' %(__ident__), 'copy %s settings at exit' %(__ident__), mdict=self.settings.get)
                self.meta.log = notify('end of %s' %(__ident__), verbose=False)

        self.meta.log = notify(
            '%s startup done' %(__ident__),
            more=dict(config=config, summary=summary, meta=meta, verbose=verbose),
            verbose=False
        )

    def sh(self, msg, cmd, cin=None, cwd=None, timeout=10, critical=True, sh_verb=None):

        from shlex import split as _split
        from subprocess import Popen as _Popen, PIPE as _PIPE, TimeoutExpired as _TimeoutExpired
        from .util.system import notify

        res = {'command': cmd}
        more = cin
        if cin: res.update({'stdin': cin})
        if cwd: res.update({'cwd': cwd})

        if sh_verb == None: sh_verb = self.__verbose

        if cmd != None:
            if isinstance(cmd, str): cmd = _split(cmd)
            try: p = _Popen(cmd, stdin=_PIPE, stdout=_PIPE, stderr=_PIPE, bufsize=1, cwd=cwd, universal_newlines=True)
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
                notify('error in shell command \'%s\'' %(res.get('command')), state=s, more=e, verbose=sh_verb)
            more = res

        self.meta.log = notify(msg, more=more, verbose=sh_verb)
        return res
