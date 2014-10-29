
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
    def sub(self):
        '''
        :param fields: Set fields to substitute
        :returns: Substituted Template with given fields
        '''

        from string import Template

        if self.__f: return Template(self.__t).substitute(self.__f)

    @sub.setter
    def sub(self, fields):
        '''
        .. seealso:: :attr:`sub`
        '''

        if isinstance(fields, dict): self.__f = fields
