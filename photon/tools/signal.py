
class Signal(object):
    '''
    The Signal tool can send signals to processes via ``kill``, returning results.

    :param pid: Either the full path to the pidfile (e.g. :file:`/var/run/proc.pid`) or the pid as number
    :param sudo: Prepend sudo before command. (Make sure to be root yourself if set to ``False`` or expect errors. Further for unattended operation add the user to :file:`sudoers` file.)
    '''

    def __init__(self, m, pid, sudo=True, cmdd_if_no_pid=None):
        super().__init__()

        from ..photon import check_m
        from ..util.files import read_file
        from ..util.locations import search_location

        self.m = check_m(m)

        pidfile = read_file(search_location(str(pid)))
        if pidfile and pidfile.strip().isdigit():
            pid = int(pidfile)

        if not isinstance(pid, int):
            if cmdd_if_no_pid:
                self.m(
                    'running post command',
                    cmdd=cmdd_if_no_pid,
                    critical=True
                )
            self.m(
                'could not determine pid%s' % (' from file' if pidfile else '!'),
                more=dict(pid=pid, pidfile=pidfile),
                state=True
            )

        self.__pid = pid
        self.__sudo = 'sudo' if sudo else ''

        self.m(
            'signal tool startup done',
            more=dict(pid=self.__pid, pidfile=pidfile if pidfile else 'passed directly'),
            verbose=False
        )

    def __signal(self, sig, verbose=None):
        '''
        Helper class preventing code duplication..

        :param sig: Signal to use (e.g. "HUP", "ALRM")
        :param verbose: Overwrite :func:`photon.Photon.m`'s `verbose`
        :returns: |kill_return| with specified `pid`

        .. |kill_return| replace:: :func:`photon.Photon.m`'s result of killing `pid`
        .. |kill_verbose| replace:: with visible shell warning
        '''
        return self.m(
            'killing process %s with "%s"' % (self.__pid, sig),
            cmdd=dict(cmd='%s kill -%s %d' % (self.__sudo, sig, self.__pid)),
            verbose=verbose
        )

    @property
    def alrm(self):
        '''
        :returns: |kill_return| using SIGALRM
        '''

        return self.__signal('ALRM')

    @property
    def hup(self):
        '''
        :returns: |kill_return| using SIGHUP
        '''

        return self.__signal('HUP')

    @property
    def int(self):
        '''
        :returns: |kill_return| using SIGINT |kill_verbose|
        '''

        return self.__signal('INT', verbose=True)

    @property
    def kill(self):
        '''
        :returns: |kill_return| using SIGKILL |kill_verbose|
        '''

        return self.__signal('KILL', verbose=True)

    @property
    def quit(self):
        '''
        :returns: |kill_return| using SIGQUIT |kill_verbose|
        '''

        return self.__signal('QUIT', verbose=True)

    @property
    def stop(self):
        '''
        :returns: |kill_return| using SIGSTOP |kill_verbose|
        '''

        return self.__signal('STOP', verbose=True)

    @property
    def usr1(self):
        '''
        :returns: |kill_return| using SIGUSR1
        '''

        return self.__signal('USR1')

    @property
    def usr2(self):
        '''
        :returns: |kill_return| using SIGUSR2
        '''

        return self.__signal('USR2')
