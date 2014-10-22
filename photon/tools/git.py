'''
.. |param_local| replace:: The local folder of the repository
.. |param_remote_url| replace:: The remote URL of the repository
'''

class Git(object):
    '''
    The git tools help to deal with git repositories.

    :param local: |param_local|

        * If ``None`` given (default), it will be ignored if there is already a git repo at `local`
        * If no git repo is found at `local`, a new one gets cloned from `remote_url`

    :param remote_url: |param_remote_url|

        * |appteardown| if `remote_url` is set to ``None`` but a new clone is necessary

    :param mbranch: The repository's main branch. Is set to `master` when left to ``None``

    '''

    def __init__(self, m, local, remote_url=None, mbranch=None):
        super().__init__()

        from ..util.locations import search_location
        from ..photon import check_m

        self.m = check_m(m)
        self.__local = search_location(local, create_in=local)
        self.__remote_url = remote_url
        if not mbranch: mbranch = 'master'
        self.__mbranch = mbranch

        if self.m(
            'checking for git repo',
            cmdd=dict(cmd='git rev-parse --show-toplevel', cwd=self.local),
            critical=False,
            verbose=False
        ).get('out') != self.local:
            if not self.remote_url: self.m('a new git clone without remote url is not possible. sorry', state=True, more=dict(local=self.local))
            self.m(
                'cloning into repo',
                cmdd=dict(cmd='git clone %s %s' %(self.remote_url, self.local))
            )

        self.m('git tool startup done', more=dict(remote_url=self.remote_url, local=self.local), verbose=False)

    @property
    def local(self):
        '''
        :returns: |param_local|
        '''

        return self.__local

    @property
    def remote_url(self):
        '''
        :returns: |param_remote_url|
        '''

        return self.__remote_url

    @property
    def remote(self):
        '''
        :returns: Current remote
        '''

        return self._get_remote().get('out')


    @property
    def commit(self):
        '''
        :returns: The current commit
        '''

        return self._log(num=1, format='%H').get('out')


    @property
    def log(self):
        '''
        :returns: The last 10 commit entries as dictionary

        * 'commit': The commit-ID
        * 'message': First line of the commit message

        '''

        log = self._log(num=10, format='%h::%b').get('stdout')
        if log: return [dict(commit=c, message=m) for c, m in [l.split('::') for l in log]]

    @property
    def status(self):
        '''
        :returns: Current repository status as dictionary:

        * 'clean': ``True`` if there are no changes ``False`` otherwise
        * 'untracked': A list of untracked files (if any and not 'clean')
        * 'modified': A list of modified files (if any and not 'clean')
        * 'deleted': A list of deleted files (if any and not 'clean')
        * 'conflicting': A list of conflicting files (if any and not 'clean')
        '''

        status = self.m(
            'getting git status',
            cmdd=dict(cmd='git status --porcelain', cwd=self.local),
            verbose=False
        ).get('stdout')
        o, m, f, g = list(), list(), list(), list()
        if status:
            for w in status:
                s, t = w[:2], w[3:]
                if '?' in s: o.append(t)
                if 'M' in s: m.append(t)
                if 'D' in s: f.append(t)
                if 'U' in s: g.append(t)
        clean = False if o + m + f + g else True
        return dict(untracked=o, modified=m, deleted=f, conflicting=g, clean=clean)

    @property
    def branch(self):
        '''
        :param branch: Checks out specified branch (tracking if it exists on remote). If set to ``None``, 'master' will be checked out
        :returns: The current branch (This could also be 'master (Detatched-Head)' - Be warned)
        '''

        branch = self._get_branch().get('stdout')
        if branch: return ''.join([b for b in branch if '*' in b]).replace('*', '').strip()

    @branch.setter
    def branch(self, branch):
        '''
        .. seealso:: :attr:`branch`
        '''

        if not branch: branch = self.__mbranch
        tracking = '' if branch in self._get_branch(remotes=True).get('out') else '-B'
        self._checkout(treeish='%s %s' %(tracking, branch))

    @property
    def tag(self):
        '''
        :param tag: Checks out specified tag. If set to ``None`` the latest tag will be checked out
        :returns: A list of all tags, sorted as version numbers, ascending
        '''

        tag = self.m(
            'getting git tags',
            cmdd=dict(cmd='git tag -l --sort="version:refname"', cwd=self.local),
            verbose=False,
        ).get('stdout')
        if tag: return tag

    @tag.setter
    def tag(self, tag):
        '''
        .. seealso:: :attr:`tag`
        '''

        if not tag:
            t = self.tag
            tag = t[-1] if t else None
        if tag: self._checkout(treeish=tag)

    @property
    def cleanup(self):
        '''
        Commits all local changes (if any) into a working branch, merges it with 'master'.

        Checks out your old branch afterwards.

        |appteardown| if conflicts are discovered
        '''

        from photon import IDENT
        from ..util.system import get_hostname

        hostname = get_hostname()
        old_branch = self.branch

        changes = self.status
        if not changes.get('clean'):

            self.branch = hostname

            for f in changes.get('untracked', []) + changes.get('modified', []):
                self.m(
                    'adding file to repository',
                    cmdd=(dict(cmd='git add %s' %(f), cwd=self.local)),
                    more=f,
                    critical=False
                )
            for f in changes.get('deleted', []):
                self.m(
                    'deleting file from repository',
                    cmdd=(dict(cmd='git rm %s' %(f), cwd=self.local)),
                    more=f,
                    critical=False
                )
            if changes.get('conflicting'): self.m('you have conflicting files in your repository!', state=True, more=changes)

            self.m(
                'auto commiting changes',
                cmdd=dict(cmd='git commit -m "%s %s auto commit"' %(hostname, IDENT), cwd=self.local),
                more=changes
            )

            self.branch = None

            self.m(
                'auto merging branches',
                cmdd=dict(cmd='git merge %s -m "%s %s auto merge"' %(hostname, hostname, IDENT), cwd=self.local),
                more=dict(branch=old_branch, temp_branch=hostname)
            )

            self.branch = old_branch

        pull = self.m('pulling remote changes', cmdd=dict(cmd='git pull --tags', cwd=self.local), critical=False)

        if 'CONFLICT' in pull.get('out'): self.m('you have a merge conflict with your remote repository!', state=True, more=pull)

        return dict(changes=changes, pull=pull)

    @property
    def publish(self):
        '''
        Runs :func:`cleanup` first to push the changes to the :attr:`remote`.
        '''

        self.cleanup

        remote = self.remote
        branch = self.branch
        return self.m(
            'pushing changes to %s/%s' %(remote, branch),
            cmdd=dict(cmd='git push -u %s %s' %(remote, branch), cwd=self.local),
            more=dict(remote=remote, branch=branch)
        )

    def _get_remote(self, cached=True):
        '''
        Helper function to determine remote

        :param cached: Use cached values or query remotes
        '''

        return self.m(
            'getting current remote',
            cmdd=dict(cmd='git remote show %s' %('-n' if cached else ''), cwd=self.local),
            verbose=False
        )

    def _log(self, num=None, format=None):
        '''
        Helper function to receive git log

        :param num: Number of entries
        :param format: Use formatted output with specified format string
        '''

        num = '-n %s' %(num) if num else ''
        format = '--format="%s"' %(format) if format else ''
        return self.m(
            'getting git log',
            cmdd=dict(cmd='git log %s %s' %(num, format), cwd=self.local),
            verbose=False
        )

    def _get_branch(self, remotes=False):
        '''
        Helper function to determine current branch

        :param remotes: List the remote-tracking branches
        '''

        return self.m(
            'getting git branch information',
            cmdd=dict(cmd='git branch %s' %('-r' if remotes else ''), cwd=self.local),
            verbose=False
        )

    def _checkout(self, treeish):
        '''
        Helper function to checkout something

        :param treeish: String for '`tag`', '`branch`', or remote tracking '-B `banch`'
        '''

        return self.m(
            'checking out "%s"' %(treeish),
            cmdd=dict(cmd='git checkout %s' %(treeish), cwd=self.local),
            verbose=False
        )
