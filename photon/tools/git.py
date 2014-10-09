
class Git(object):
    def __init__(self, local, m, remote_url=None):

        super().__init__()

        from ..util.locations import locate_file

        if callable(m): self.m = m
        else: raise Exception('wrong m(')

        self.__local = locate_file(local, create_in=local)
        self.__remote_url = remote_url

        if not self.__log(num=0, critical=False).get('returncode', False) == 0:
            if not self.remote_url:
                self.m(
                    'a new git clone without remote url makes no sense',
                    state=True,
                    more=dict(local=self.__local, remote_url=self.__remote_url)
                )
            else: self.__clone()

        self.info

        self.m(
            'git tool startup done',
            more=dict(local=self.__local, remote_url=self.__remote_url),
            verbose=False
        )

    @property
    def info(self):
        return {
            'local': self.local,
            'remote': self.remote,
            'remote_url': self.remote_url,
            'commit': self.commit,
            'log': self.log,
            'status': self.status,
            'branch': self.branch,
        }

    @property
    def local(self):
        return self.__local

    @property
    def remote_url(self):
        return self.__remote_url

    @property
    def remote(self):
        remote = self.__remote_show().get('out')
        if remote: remote

    @property
    def commit(self):
        commit = self.__log(num=1, format='%H').get('out')
        if commit: return commit

    @property
    def log(self):
        log = self.__log(num=10, format='%h::%b').get('stdout')
        if log: return [dict(commit=c, message=m) for c, m in [l.split('::') for l in log]]

    @property
    def status(self):
        status = self.m(
            'getting git status',
            cmdd=dict(cmd='git status --porcelain', cwd=self.local),
            verbose=False
        ).get('out')
        if status: return status

    @property
    def branch(self):
        branch = self.__branch_show().get('stdout')
        if branch: return ''.join([b for b in branch if '*' in b]).replace('*', '').strip()

    @branch.setter
    def branch(self, branch):

        if not branch: branch = 'master'
        tracking = '' if branch in self.__branch_show(remotes=True).get('out') else '-B '
        self.m(
            'checking out branch',
            cmdd=dict(cmd='git checkout %s%s' %(tracking, branch), cwd=self.local)
        )
        return self.branch

    def __clone(self):

        return self.m(
            'cloning into repo',
            cmdd=dict(cmd='git clone %s %s' %(self.remote_url, self.local))
        )

    def __remote_show(self, cached=True):

        return self.m(
            'getting current remote',
            cmdd=dict(cmd='git remote show %s' %('-n' if cached else ''), cwd=self.local),
            verbose=False
        )

    def __log(self, num=5, format='%h - %b', critical=True):

        return self.m(
            'getting git log',
            cmdd=dict(cmd='git log -n %s --format="%s"' %(num, format), cwd=self.local),
            critical=critical,
            verbose=False
        )

    def __branch_show(self, remotes=None):

        return self.m(
            'getting git branch information',
            cmdd=dict(cmd='git branch %s' %('-r' if remotes else ''), cwd=self.local),
            verbose=False
        )
