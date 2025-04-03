from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

from base_page.blocks import *


class HomePage(Page):
    """A simple homepage model with a hero banner and a streamfield body."""

    hero_title = models.CharField(max_length=250, blank=True, null=True)
    hero_subtitle = models.CharField(max_length=250, blank=True, null=True)
    body = StreamField(
        CommonBlockStream(),  # uses the blocks defined in blocks.py
        null=True,
        blank=True,
        use_json_field=True, 
    )

    content_panels = Page.content_panels + [
        FieldPanel("hero_title"),
        FieldPanel("hero_subtitle"),
        FieldPanel("body"),
    ]

    class Meta:
        verbose_name = "Homepage"
        verbose_name_plural = "Homepages"
