
class Mail(object):
    '''
    The Mail tool helps to send out mails.

    :param to: Where to ('user@example.com')
    :param sender: Yourself ('me@example.com' - you should have set ``example.com`` as reverse dns not to get caught up in spamfilters)
    :param subject: The subject line
    :param cc: One or a list of CCs
    :param bcc: One or a list of BCCs

    '''


    def __init__(self, to, sender, m, subject=None, cc=None, bcc=None):
        super().__init__()

        from itertools import chain as _chain
        from email import charset as _charset
        from email.mime.multipart import MIMEMultipart as _MIMEMultipart
        from email.utils import formatdate as _formatdate
        from photon import IDENT
        from ..photon import check_m
        from ..util.structures import to_list
        from ..util.system import get_timestamp

        self.m = check_m(m)

        to = to_list(to)
        cc = to_list(cc)
        bcc = to_list(bcc)
        if not subject: subject = IDENT
        subject = '%s - %s' %(subject, get_timestamp())

        self.__sender = sender
        self.__recipients = list(_chain(to, cc, bcc))

        _charset.add_charset('utf-8', _charset.QP, _charset.QP, 'UTF-8')

        self.__message = _MIMEMultipart()
        self.__message.add_header('To', ', '.join(to))
        if cc: self.__message.add_header('CC', ', '.join(cc))
        self.__message.add_header('From', sender)
        self.__message.add_header('Subject', subject)
        self.__message.add_header('Date', _formatdate())
        self.__message.add_header('X-Mailer', 'Postbote Willy')

        self.m('mail tool startup done', more=dict(to=to, cc=cc, bcc=bcc, sender=sender, subject=subject), verbose=False)

    @property
    def text(self):
        '''
        Add more text to the mail

        :param elem: Add some more text
        :returns: All text & headers as raw mail source
        '''

        return self.__message.as_string().encode('UTF-8')

    @text.setter
    def text(self, elem):
        '''
        .. seealso:: :attr:`text`
        '''

        from email.mime.text import MIMEText as _MIMEText
        from pprint import pformat as _pformat

        if elem:
            if not isinstance(elem, str): elem = _pformat(elem)
            self.m(
                'add text to mail',
                more=dict(len=len(elem))
            )
            self.__message.attach(_MIMEText(elem, 'plain', 'UTF-8'))

    @property
    def send(self):
        '''
        Sends the compiled mail

        .. note:: You need to have a postfix/sendmail running and listening on localhost
        '''

        from smtplib import SMTP as _SMTP, SMTPException as _SMTPException
        from socket import error as _error

        res = dict(sender=self.__sender, recipients=self.__recipients)
        try:
            s = _SMTP()
            s.connect('localhost')
            res.update(dict(result=s.sendmail(self.__sender, self.__recipients, self.text)))
            self.m('mail sent', more=res)
        except (_SMTPException, _error) as ex:
            res.update(dict(exception=str(ex)))
            self.m('error sending mail', verbose=True, more=res)
        return res
