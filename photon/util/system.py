
def notify(msg, state=False, more=None, exitcode=None, verbose=True):

    from sys import exit as _exit
    from pprint import pformat as _pformat

    if state == True:
        state = '[FATAL]'
        exitcode = 23
    elif state == None: state = '[WARNING]'
    elif state == False: state = '|'
    else: state = '[%s]' %(str(state))
    m = '%s %s' %(state, str(msg))
    if more: m += '\n\t%s' %(_pformat(more))
    if verbose or isinstance(exitcode, int): print(m)
    if isinstance(exitcode, int): _exit(exitcode)
    return dict(message=msg, more=more, verbose=verbose)

def get_timestamp(precice=False):

    from datetime import datetime as _datetime

    f = '%Y.%m.%d-%H.%M.%S'
    if precice: f += '-%f'
    return _datetime.now().strftime(f)
