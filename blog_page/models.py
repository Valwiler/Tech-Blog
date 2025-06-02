import datetime

from base_page.blocks import CommonBlockStream
from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page
from wagtail.search import index
from wagtailseo.models import SeoMixin, SeoType


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey('blog_page.BlogPage', on_delete=models.CASCADE, related_name='tagged_items')

class BlogPage(SeoMixin, Page):
    """A standard blog page with a body StreamField."""
    template = "blog_page.html"
    date = models.DateField("Post date", default=datetime.date.today)
    body = StreamField(
        CommonBlockStream(),
        null=True,
        blank=True,
        use_json_field=True,
    )
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.FilterField('date'),
    ]

    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    seo_content_type = SeoType.ARTICLE

    promote_panels = SeoMixin.seo_panels + [ FieldPanel('tags')]

    content_panels = Page.content_panels + [
        FieldPanel("body"),
        FieldPanel("date"),
        FieldPanel("feed_image"),
    ]

    subpage_types = ["blog_page.BlogPage"]

    class Meta:
        verbose_name = "Blog article"
        verbose_name_plural = "Blog articles"
