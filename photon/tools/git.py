
class Git(object):
    def __init__(self, local, m, remote_url=None):

        super().__init__()

        from ..util.locations import locate_file

        if callable(m): self.m = m
        else: raise Exception('wrong m(')

        self._r = {'local': locate_file(local, create_in=local), 'remote_url': remote_url}

        if not self.__is_git():
            if not self.remote_url:
                self.m(
                    'a new git clone without remote url makes no sense',
                    state=True,
                    more=self._r
                )
            else: self.__clone()

        self.m(
            'git tool startup done',
            more=self._r,
            verbose=False
        )

    @property
    def info(self):
        '''info doc'''
        return self._r

    @property
    def local(self):
        return self._r.get('local')

    @property
    def remote_url(self):
        return self._r.get('remote_url')

    @property
    def remote(self):
        remote = self.__remote_show().get('stdout')[-1]
        if remote: self._r.update({'remote': remote})
        return self._r.get('remote')

    @property
    def branch(self):
        return False

    def __is_git(self):

        c = self.m(
            'checks if this is a git repo (looks at the returncode)',
            cmdd=dict(cmd='git -C %s log -n 0' %(self.local)),
            critical=False,
            verbose=False
        )
        return c.get('returncode', False) == 0

    def __clone(self):

        return self.m(
            'cloning into repo',
            cmdd=dict(cmd='git clone %s %s' %(self.remote_url, self.local)),
        )

    def __remote_show(self, cached=True):

        return self.m(
            'getting current remote',
            cmdd=dict(cmd='git -C %s remote show %s' %(self.local, '-n' if cached else '')),
            verbose=False
        )
