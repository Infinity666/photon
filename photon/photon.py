
class Photon(object):
    '''
    Photon uses :ref:`core` and some functions from :ref:`util` in its :meth:`m`-method.
    The :meth:`m`-method itself is used in each tool to interact with photon to:

        * Launch shell commands, and receive the results
        * Add messages to the `meta`-file
        * Show the messages if necessary
        * Tear down application completely in case of any serious problems

    Further, Photon provides direct handlers for :class:`settings.Settings` and :class:`meta.Meta`
    and a handler for each tool from :ref:`tools` by it's methods.

    :param defaults: Pass `defaults` down to :class:`settings.Settings`
    :param config: Pass `config` down to :class:`settings.Settings`
    :param meta: Pass `meta` down to :class:`meta.Meta`
    :param verbose: Sets the global `verbose` flag. Passes it down to the underlying :ref:`util` functions and :ref:`core`
    :var settings: The settings handler initialized with `defaults` and `config`
    :var meta: The meta handler initialized with `meta`

    Photon registers two exit functions:

        * One to copy all content from settings into the meta-header,
        * Another one to add a final log entry (to save the meta-file).
    '''

    def __init__(self, defaults='defaults.yaml', config='config.yaml', meta='meta.json', verbose=True):
        super().__init__()

        from atexit import register as _register
        from photon import Settings, Meta, IDENT
        from .util.system import shell_notify

        self.settings = Settings(defaults=defaults, config=config, verbose=verbose)
        self.meta = Meta(meta=meta, verbose=verbose)
        self.__verbose = verbose

        @_register
        def __say_goodbye():

            if self.meta:
                self.meta.log = shell_notify('end of %s' %(IDENT), verbose=False)

        @_register
        def __copy_settings_to_meta():

            if self.meta and self.settings:
                self.meta.load('%s settings' %(IDENT), 'copy %s settings at exit' %(IDENT), mdict=self.settings.get)

        self.meta.log = shell_notify(
            '%s startup done' %(IDENT),
            more=dict(defaults=defaults, config=config, meta=meta, verbose=verbose),
            verbose=False
        )

    def m(self, msg, state=False, more=None, cmdd=None, critical=True, verbose=None):
        '''
        Mysterious mega method managing multiple meshed modules magically

        .. note:: If this function is used, the code contains facepalms: ``m(``

        * It is possible to just show a message, or to run a command with message.
        * But it is not possible to run a command without a message, use the `verbose`-flag to hide your debug message.

        :param msg: Add a message. Shown depending on `verbose` (see below)
        :param state: Pass `state` down to :func:`util.system.shell_notify`
        :param more: Pass `more` down to :func:`util.system.shell_notify`
        :param dict cmdd: If given, :func:`util.system.shell_run` is launched with it's values
        :param critical: If set to ``True``: |appteardown| on failure of `cmdd` contents.

            * Similar to :func:`util.system.shell_run` `critical`-flag

        :param verbose: Overrules parent's class `verbose`-flag.

            * If left to ``None``, the verbose value Photon was started with is used
            * Messages are shown/hidden if explicitly set to ``True``/``False``

        :returns: A dictionary specified the following:

        * 'more': `more` if it is not a dictionary otherwise it gets merged in if `more` is specified
        * The output of :func:`util.system.shell_run` gets merged in if `cmdd` is specified
        * 'failed': ``True`` if command failed

        :func:`util.system.shell_notify` is used with this dictionary to pipe it's output into :func:`meta.Meta.log` before returning.
        '''

        from .util.system import shell_notify, shell_run

        if verbose == None: verbose = self.__verbose

        res = dict()
        if more:
            res.update(more) if isinstance(more, dict) else res.update(dict(more=more))

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

    def git_handler(self, *args, **kwargs):
        '''
        :returns: A new git handler

        .. seealso:: :ref:`tools_git`
        '''

        from .tools.git import Git

        return Git(self.m, *args, **kwargs)

    def mail_handler(self, punchline=None, add_meta=False, add_settings=True, *args, **kwargs):
        '''
        :param punchline: Adds a punchline before further text
        :param add_meta: Appends current meta to the mail
        :param add_settings: Appends current settings to the mail
        :returns: A new mail handler

        .. seealso:: :ref:`tools_mail`
        '''

        from .tools.mail import Mail

        m = Mail(self.m, *args, **kwargs)
        if punchline: m.text = '-> %s <-' %(punchline)
        if add_meta: m.text = self.meta.log
        if add_settings: m.text = self.settings.get
        return m

    def ping_handler(self, *args, **kwargs):
        '''
        :returns: A new ping handler

        .. seealso:: :ref:`tools_ping`
        '''

        from .tools.ping import Ping

        return Ping(self.m, *args, **kwargs)

    def signal_handler(self, *args, **kwargs):
        '''
        :returns: A new signal handler

        .. seealso:: :ref:`tools_signal`
        '''

        from .tools.signal import Signal

        return Signal(self.m, *args, **kwargs)

def check_m(pm):
    '''
    Shared helper function for all :ref:`tools` to check if the passed m-function is indeed :func:`photon.Photon.m`

    :params pm: Suspected m-function
    :returns: Now to be proven correct m-function, tears down whole application otherwise.
    '''

    from .util.system import shell_notify

    if not callable(pm) or pm.__name__ != Photon.m.__name__ or pm.__doc__ != Photon.m.__doc__:
        shell_notify('wrong "m-function" passed!', state=True, more=pm.__name__)
    return pm
