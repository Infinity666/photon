

def get_timestamp(precice=False):

    from datetime import datetime as _datetime

    f = '%Y.%m.%d-%H.%M.%S'
    if precice: f += '-%f'
    return _datetime.now().strftime(f)

