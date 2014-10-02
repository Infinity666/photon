

def get_timestamp(precice=False):

    from datetime import datetime

    fstr = '%Y.%m.%d-%H.%M.%S'
    if precice: fstr += '-%f'
    return datetime.now().strftime(fstr)

