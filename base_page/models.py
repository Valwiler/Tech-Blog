
from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

from .blocks import CommonBlockStream
class RegularPage(Page):
    """A standard page with a body StreamField."""
    template = "base_page.html"
    body = StreamField(
        CommonBlockStream(),
        null=True,
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    class Meta:
        verbose_name = "Regular Page"
        verbose_name_plural = "Regular Pages"
