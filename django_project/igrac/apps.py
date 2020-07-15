from django.apps import AppConfig


class IgracConfig(AppConfig):
    name = 'igrac'

    def ready(self):
        import igrac.signals