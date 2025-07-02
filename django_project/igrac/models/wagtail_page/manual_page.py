from django.urls import reverse
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from django.db.models import Q


class ManualPage(Page):
    """Model to define manual page for wagtail"""

    intro = RichTextField(blank=True)
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        FieldPanel('body'),
    ]

    subpage_types = [
        'igrac.ManualPage',
    ]
    parent_page_type = [
        'wagtailcore.Page',
    ]

    def get_children_with_permission(self, page, request):
        pages = page.get_children()
        if not request.user.is_authenticated:
            # only pages with no view restrictions at all
            pages = pages.public()
        else:
            if request.user.is_superuser:
                return pages
            pages = pages.filter(
                # pages with no view restrictions
                Q(view_restrictions__isnull=True) |
                # pages restricted to any logged-in user
                Q(view_restrictions__restriction_type='login') |
                # pages restricted by group
                Q(view_restrictions__restriction_type='groups',
                  view_restrictions__groups__in=request.user.groups.all())
            )
        return pages

    def get_children_menu(self, page, request):
        from wagtail.admin.urls.pages import app_name
        menu = []
        for child in self.get_children_with_permission(page, request):
            if child.live:
                url = child.url
            elif request.user.is_superuser:
                url = reverse(
                    '{}:edit'.format(app_name),
                    args=[child.id])
            else:
                url = None
            children_data = {
                'title': child.title,
                'slug': child.slug,
                'url': url,
                'live': child.live
            }
            if child.get_children():
                children_data['children'] = self.get_children_menu(
                    child, request)
            menu.append(children_data)
        return menu

    def get_context(self, request, *args, **kwargs):
        context = super(ManualPage, self).get_context(request, *args, **kwargs)
        ancestors = self.get_ancestors()
        if len(ancestors) > 1:
            page = ancestors[1]
        else:
            page = self
        menu = self.get_children_menu(page, request)
        context['menu'] = menu

        return context
