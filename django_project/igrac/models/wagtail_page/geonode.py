from modelcluster.fields import ParentalManyToManyField
from wagtailautocomplete.edit_handlers import AutocompletePanel

from geonode.maps.models import Map, Dataset
from igrac.models.wagtail_page.blog import BlogPage


class GeonodePage(BlogPage):
    """Blog map page is used for showing the blog when map is opened."""
    maps = ParentalManyToManyField(Map, blank=True)
    datasets = ParentalManyToManyField(Dataset, blank=True)

    content_panels = BlogPage.content_panels + [
        AutocompletePanel('maps', target_model=Map),
        AutocompletePanel('datasets', target_model=Dataset)
    ]
