
class Photon(object):
    def __init__(self, config='config.yaml', summary='summary.yaml', meta='meta.json', verbose=True):

        super().__init__()

        from atexit import register as _register
        from photon import Settings, Meta, __ident__
        from .util.system import shell_notify

        self.settings = Settings(config=config, summary=summary, verbose=verbose)
        self.meta = Meta(meta=meta, verbose=verbose)
        self.__verbose = verbose

        @_register
        def __say_goodbye():

            if self.meta:
                self.meta.log = shell_notify('end of %s' %(__ident__), verbose=False)

        @_register
        def __copy_settings_to_meta():

            if self.meta and self.settings:
                self.meta.load('%s settings' %(__ident__), 'copy %s settings at exit' %(__ident__), mdict=self.settings.get)

        self.meta.log = shell_notify(
            '%s startup done' %(__ident__),
            more=dict(config=config, summary=summary, meta=meta, verbose=verbose),
            verbose=False
        )

    def m(self, msg, state=False, more=None, cmdd=None, critical=True, verbose=None):

        from .util.system import shell_notify, shell_run

        if verbose == None: verbose = self.__verbose

        res = dict()
        if more and isinstance(more, dict): res.update(more)

        if cmdd and isinstance(cmdd, dict) and cmdd.get('cmd'):
            res.update(shell_run(
                cmdd.get('cmd'),
                cin=cmdd.get('cin'),
                cwd=cmdd.get('cwd'),
                timeout=cmdd.get('timeout', 120),
                critical=False,
                verbose=cmdd.get('verbose', verbose)
            ))

            if res.get('returncode', -1) != 0:
                res.update(dict(failed=True))

        if state or critical and res.get('failed'):
            self.meta.log = dict(message=msg, more=res, verbose=verbose)
            shell_notify(msg, more=res, state=True)
        self.meta.log = shell_notify(msg, more=res, state=state, verbose=verbose)
        return res

    def new_git(self, local, remote_url=None):

        from .tools.git import Git

        return Git(local, self.m, remote_url=remote_url)

    def new_mail(self, to, sender, subject=None, cc=None, bcc=None, punchline=None, add_meta=False, add_settings=True):

        from .tools.mail import Mail

        m = Mail(to, sender, self.m, subject=subject, cc=cc, bcc=bcc)
        if punchline: m.text = '-> ' + punchline + ' <-'
        if add_meta: m.text = self.meta.log
        if add_settings: m.text = self.settings.get
        return m
