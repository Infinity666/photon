
class Template(object):
    '''
    The Template tool helps to process on strings.

    :param template: The initial template to start with.

        * If it's value is recognized by :func:`util.locations.search_location` (a.k.a is a filename) the file contents will be loaded as template.

    :param fields: Initially set up fields. Can be done later, using :func:`sub`

    The templating-language itself are normal :py:ref:`template-strings`, see there for syntax.
    '''

    def __init__(self, m, template, fields=None):
        super().__init__()

        from ..photon import check_m
        from ..util.files import read_file
        from ..util.locations import search_location

        self.m = check_m(m)

        tfile = search_location(template)

        self.__t = read_file(tfile) if tfile else template
        self.__f = fields

        self.m('template tool startup done', more=dict(fields=self.__f, file=tfile), verbose=False)

    @property
    def raw(self):
        '''
        :returns: The raw template
        '''

        return self.__t

    @property
    def sub(self):
        '''
        :param fields: Set fields to substitute
        :returns: Substituted Template with given fields. If no fields were set up beforehand, :func:`raw` is used
        '''

        from string import Template

        return Template(self.raw).substitute(self.__f) if self.__f else self.raw

    @sub.setter
    def sub(self, fields):
        '''
        .. seealso:: :attr:`sub`
        '''

        self.__f = fields

    def write(self, filename, append=True):
        '''
        :param filename: File to write into
        :param append: Either append to existing content (if not already included) or completely replace `filename`
        '''

        from ..util.files import read_file, write_file

        res = self.sub
        if append:
            org = read_file(filename)
            if org:
                if res in org: res = org
                else: res = org + res

        write_file(filename, res)
        return self.m('template %s' %('appended' if append else 'written'), more=dict(fields=self.__f, file=filename))
