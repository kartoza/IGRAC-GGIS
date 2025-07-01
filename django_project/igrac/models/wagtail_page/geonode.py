from django.http import HttpResponse
from modelcluster.fields import ParentalManyToManyField
from wagtail.contrib.routable_page.models import route
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

    @route(r'^body-only/$')
    def body_only_view(self, request):
        return HttpResponse(self.body, content_type='text/html')
