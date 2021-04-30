import copy
from django.utils.html import escape, format_html
from wagtail.images.formats import Format, register_image_format
from wagtail.images.shortcuts import get_rendition_or_not_found


class CaptionedImageFormat(Format):

    def image_to_html(self, image, alt_text, extra_attributes=None):
        if extra_attributes is None:
            extra_attributes = {}
        rendition = get_rendition_or_not_found(image, self.filter_spec)
        extra_attributes['alt'] = escape(alt_text)
        default_html = rendition.img_tag(extra_attributes)

        return format_html(
            "<div class='{}'>{}<figcaption>{}</figcaption></div>", "%s" % escape(
                self.classnames), default_html, alt_text
        )


register_image_format(
    CaptionedImageFormat('captioned_fullwidth', 'Captioned full width', 'captioned-image richtext-image full-width', 'width-800')
)
register_image_format(
    CaptionedImageFormat('captioned_left', 'Captioned half width left aligned', 'captioned-image richtext-image left', 'width-500')
)
register_image_format(
    CaptionedImageFormat('captioned_right', 'Captioned half width right aligned', 'captioned-image richtext-image right', 'width-500')
)
