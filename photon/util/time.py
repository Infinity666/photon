

def get_timestamp(precice=False):

    from datetime import datetime

    f = '%Y.%m.%d-%H.%M.%S'
    if precice: f += '-%f'
    return datetime.now().strftime(f)

