import collections
import os
from urllib import parse

from django.conf import settings

folder = os.path.join(settings.GWML2_FOLDER, 'istsos')


def param_to_lowercase(param):
    return param.lower() if isinstance(param, str) else param


def get_params(url):
    """Get params."""
    params = dict(parse.parse_qs(parse.urlsplit(url).query))
    try:
        del params['api-key']
    except KeyError:
        pass
    ordered_params = collections.OrderedDict(sorted(params.items()))
    params = []
    for key, value in ordered_params.items():
        if key == 'request':
            params.append(f'{key}={param_to_lowercase(value[0])}')
        else:
            params.append(f'{key}={value[0]}')
    return '&'.join(params)
