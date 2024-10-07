__author__ = 'Irwan Fathurrahman <meomancer@gmail.com>'
__date__ = '02/02/21'

import os


def project_version(request):
    """ Read project version from file"""
    DJANGO_ROOT = os.path.dirname(
        os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        ))
    folder = os.path.join(
        DJANGO_ROOT, 'django_project', 'version')
    version = os.path.join(
        folder, 'version.txt')
    if os.path.exists(version):
        version = (open(version, 'rb').read()).decode("utf-8")
        if version:
            return {
                'IGRAC_VERSION': {
                    'url': 'https://github.com/kartoza/IGRAC-GGIS/releases/tag/{}'.format(version),
                    'name': version
                }

            }
    commit = os.path.join(
        folder, 'commit.txt')
    if os.path.exists(commit):
        commit = (open(commit, 'rb').read()).decode("utf-8")
        if commit:
            return {
                'IGRAC_VERSION': {
                    'url': 'https://github.com/kartoza/IGRAC-GGIS/commit/{}'.format(commit),
                    'name': commit
                }
            }
    return {}


def gwml2_version():
    """ Read gwml2 versionfrom file."""
    DJANGO_ROOT = os.path.dirname(
        os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        ))
    _file = os.path.join(
        DJANGO_ROOT,
        'django_project', 'gwml2', 'version'
    )
    if os.path.exists(_file):
        version = (open(_file, 'rb').read()).decode("utf-8")
        if version:
            return version
    return '-'
