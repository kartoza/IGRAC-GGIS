import collections
import os
import shutil
from urllib import parse

import requests
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


def generate_cache(url, delete_folder=False):
    """Render cache."""
    params = get_params(url)
    if not os.path.exists(folder):
        os.mkdir(folder)

    params_for_name = params.replace('/', '-')
    file = os.path.join(folder, params_for_name)
    content_type_file = os.path.join(folder, params_for_name) + ';content_type'

    response = requests.get('http://istsos/istsos/istsos?' + params)

    if response.status_code == 200:
        if delete_folder and os.path.exists(folder):
            shutil.rmtree(folder)
            os.mkdir(folder)

        f = open(file, "wb+")
        f.write(response.content)
        f.close()
        f = open(content_type_file, "w+")
        f.write(response.headers['Content-Type'])
        f.close()


def check_cache(url):
    """Check cache."""
    params = get_params(url)
    if not os.path.exists(folder):
        os.mkdir(folder)
    params_for_name = params.replace('/', '-')
    file = os.path.join(folder, params_for_name)
    content_type_file = os.path.join(folder, params_for_name) + ';content_type'
    if os.path.exists(file) and os.path.exists(content_type_file):
        f = open(file, "rb+")
        content = f.read()
        f = open(content_type_file, "r+")
        content_type = f.read()
        return content, content_type
    return None, None
