from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from wagtailseo.models import SeoMixin

from .blocks import CommonBlockStream

class RegularPage(SeoMixin, Page):
    """A standard page with a body StreamField."""
    template = "base_page.html"

    body = StreamField(
        CommonBlockStream(),
        null=True,
        blank=True,
        use_json_field=True,
    )

    # Table of Contents toggle
    show_table_of_contents = models.BooleanField(
        default=False,
        help_text="Display a table of contents sidebar that auto-generates from page headings"
    )

    promote_panels = SeoMixin.seo_panels

    content_panels = Page.content_panels + [
        FieldPanel("show_table_of_contents"),
        FieldPanel("body"),
    ]

    class Meta:
        verbose_name = "Regular Page"
        verbose_name_plural = "Regular Pages"
