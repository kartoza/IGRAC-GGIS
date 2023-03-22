from django.apps import AppConfig


class IgracConfig(AppConfig):
    name = 'igrac'

    def ready(self):
        import igrac.signals
        import igrac.monkeypatch
        from django.conf import settings
        geonode_mapstore_client_template_dir = ''
        for template_dir in settings.TEMPLATES[0]['DIRS']:
            if 'geonode_mapstore_client' in template_dir:
                geonode_mapstore_client_template_dir = template_dir
                settings.TEMPLATES[0]['DIRS'].remove(template_dir)
                break
        if geonode_mapstore_client_template_dir:
            settings.TEMPLATES[0]['DIRS'].append(
                geonode_mapstore_client_template_dir
            )
