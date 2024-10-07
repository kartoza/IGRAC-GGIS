__author__ = 'Irwan Fathurrahman <meomancer@gmail.com>'
__date__ = '02/02/21'

import os

DJANGO_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)


def return_version_from_file(_file):
    """Retun version from file"""
    if os.path.exists(_file):
        version = (open(_file, 'rb').read()).decode("utf-8")
        if version:
            return version
    return None


def project_version(request):
    """ Read project version from file"""
    version = igrac_version()
    _geonode_version = geonode_version()
    if _geonode_version:
        _geonode_version = _geonode_version.replace(
            '-igrac', ''
        ).replace(
            '.igrac', ''
        )
    else:
        _geonode_version = 'unknown'

    if version:
        return {
            'IGRAC_VERSION': {
                'url': (
                    f'https://github.com/kartoza/IGRAC-GGIS/'
                    f'releases/tag/{version}'
                ),
                'name': version
            },
            'GEONODE_VERSION': _geonode_version
        }

    commit = igrac_commit()
    if commit:
        return {
            'IGRAC_VERSION': {
                'url': (
                    f'https://github.com/kartoza/IGRAC-GGIS/commit/{commit}'
                ),
                'name': commit
            },
            'GEONODE_VERSION': _geonode_version
        }
    return {
        'GEONODE_VERSION': _geonode_version
    }


def geonode_version():
    """Return geonode version."""
    return return_version_from_file(
        os.path.join(
            DJANGO_ROOT, 'django_project', 'version', 'geonode_version.txt'
        )
    )


def igrac_version():
    """Return igrac version."""
    return return_version_from_file(
        os.path.join(
            DJANGO_ROOT, 'django_project', 'version', 'version.txt'
        )
    )


def igrac_commit():
    """Return igrac commit."""
    return return_version_from_file(
        os.path.join(
            DJANGO_ROOT, 'django_project', 'version', 'commit.txt'
        )
    )


def gwml2_version():
    """Read gwml2 version from file."""
    return return_version_from_file(
        os.path.join(
            DJANGO_ROOT, 'django_project', 'gwml2', 'version.txt'
        )
    )
