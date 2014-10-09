
class Git(object):
    def __init__(self, local, m, remote_url=None):

        super().__init__()

        from ..util.locations import locate_file

        if callable(m): self.m = m
        else: raise Exception('wrong m(')

        self.__local = locate_file(local, create_in=local)
        self.__remote_url = remote_url

        if not self.__log(num=0, critical=False).get('returncode', False) == 0: self.__clone()

        self.m('git tool startup done', more=self.info, verbose=False)

    @property
    def info(self):

        return dict(
            local=self.local,
            remote=self.remote,
            remote_url=self.remote_url,
            commit=self.commit,
            log=self.log,
            status=self.status,
            branch=self.branch,
        )

    @property
    def local(self):

        return self.__local

    @property
    def remote_url(self):

        return self.__remote_url

    @property
    def remote(self):

        return self.__remote_show().get('out')


    @property
    def commit(self):

        return self.__log(num=1, format='%H').get('out')


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
        ).get('stdout')
        untracked, modified, deleted, conflicting = list(), list(), list(), list()
        if status:
            for c in status:
                s, f = c[:2], c[3:]
                if '?' in s: untracked.append(f)
                if 'M' in s: modified.append(f)
                if 'D' in s: deleted.append(f)
                if 'U' in s: conflicting.append(f)
        return dict(untracked=untracked or None, modified=modified or None, deleted=deleted or None, conflicting=conflicting or None)

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

        if not self.remote_url: self.m('a new git clone without remote url is not possible. sorry', state=True, more=dict(local=self.local))
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

    def __log(self, num=None, format=None, critical=True):

        num = '-n %s' %(num) if num else ''
        format = '--format="%s"' %(format) if format else ''
        return self.m(
            'getting git log',
            cmdd=dict(cmd='git log %s %s' %(num, format), cwd=self.local),
            critical=critical,
            verbose=False
        )

    def __branch_show(self, remotes=None):

        return self.m(
            'getting git branch information',
            cmdd=dict(cmd='git branch %s' %('-r' if remotes else ''), cwd=self.local),
            verbose=False
        )
