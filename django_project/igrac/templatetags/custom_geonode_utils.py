from django import template
from django.utils.html import word_split_re
from django.template.defaultfilters import stringfilter, urlize

register = template.Library()


@register.filter(name='remove_localhost')
def remove_localhost(url):
    """Remove localhost from url"""
    if url:
        url = url.replace('http://localhost:8080', '')
    return url


@register.filter()
@stringfilter
def urlize_that_is_link(string):
    """no follow url from string"""
    words = word_split_re.split(str(string))
    before2 = None
    before = None
    for idx, word in enumerate(words):
        couple_words = "{}{}{}".format(before2, before, word)
        if ('http://' in word or 'https://' in word) and "href" not in couple_words and '">' not in couple_words:
            words[idx] = urlize(word)
        before2 = before
        before = word
    return ''.join(words)


@register.filter(name='return_metadata_link')
def return_metadata_link(resource):
    """Return metadat link."""
    if resource.embed_url:
        return resource.embed_url.replace('embed', 'metadata_detail')
    return resource.get_absolute_url() + '/metadata_detail'
