from geonode.layers.models import Style

Style._meta.ordering = ['sld_title', 'name']
