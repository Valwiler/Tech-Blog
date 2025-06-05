from django import forms
from django.utils.functional import cached_property
from django.utils.html import format_html
from ads_and_analytics.blocks import CommonBlockStreamWithAds
from wagtail import blocks
from wagtail.blocks import StructValue
from wagtail.blocks.struct_block import StructBlockAdapter
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.documents.models import Document
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page
from wagtail.telepath import register


class LinkStructValue(StructValue):
    def url(self):
        url = False
        content_type = self.get('content_type')
        if content_type == "d":
            document = self.get('document')
            if document:
                if type(document) == int:
                    document = Document.objects.get(pk=document)
                url = document.url if document else False
            else:
                url = False
        elif content_type == "l":
            page = self.get('link_page')
            external_url = self.get('link_url')
            if page:
                if type(page) == int:
                    page = Page.objects.get(pk=page)
                url = page.url if page else False
            elif external_url:
                url = external_url
            else:
                url = False
        if url:
            if self.get("open_in_new_tab"):
                return format_html("href='{}' target='#'", url)
            else:
                return format_html("href='{}'", url)
        else:
            return None

    def title(self):
        return self.get('link_title')

class LinkBlock(blocks.StructBlock):
    link_title = blocks.CharBlock(
        required=False,
        label=("Title/Text of the link"),
    )

    content_type = blocks.ChoiceBlock(
        blank=False,
        choices=[
            ("d", ("Document")),
            ("l", ("Link")),
        ],
        label=("Type of content associated with the link"),
        required=False,
    )

    document = DocumentChooserBlock(
        blank=True,
        help_text=("Document to download when clicking the link"),
        label=("Document"),
        required=False,
    )

    link_page = blocks.PageChooserBlock(
        blank=True,
        help_text=("If you fill in the internal URL, the external URL will not be used"),
        label=("URL of the link to an internal page"),
        required=False
    )

    link_url = blocks.URLBlock(
        blank=True,
        help_text=("If you fill in the internal URL, the external URL will not be used"),
        label=("URL of the link to an external page"),
        required=False,
    )

    open_in_new_tab = blocks.BooleanBlock(
        blank=True,
        default=False,
        label=("Check to open the link in a new tab"),
        required=False,
    )

    class Meta:
        icon = "edit"
        value_class = LinkStructValue


class HeadingBlock(blocks.StructBlock):
    """A heading block with a level (h1, h2, etc.) and text."""
    heading_text = blocks.CharBlock(required=True, help_text="Heading text")
    size = blocks.ChoiceBlock(
        choices=[
            ("h1", "H1"),
            ("h2", "H2"),
            ("h3", "H3"),
            ("h4", "H4"),
            ("h5", "H5"),
        ],
        default="h2",
        help_text="Heading size"
    )

    class Meta:
        icon = "title"
        label = "Heading"
        template = "blocks/heading_block.html"


class ParagraphBlock(blocks.RichTextBlock):
    """A rich text paragraph block."""
    def __init__(self, *args, **kwargs):
        feature = kwargs.get("features", None)
        super().__init__(*args, **kwargs)
        if feature:
            self.features = feature
        else :
            self.features = ["h2", "h3", "h4", "h5", "h6", "bold", "italic","ol", "ul", "hr", "link", "embed", "image", "document-link", "code", "superscript", "subscript", "strikethrough", "blockquote"  ]


    class Meta:
        icon = "pilcrow"
        label = "Paragraph"
        template = "blocks/paragraph_block.html"


class CodeBlock(blocks.StructBlock):
    """A code block with a language choice and code text area."""
    language = blocks.ChoiceBlock(
        choices=[
            ("python", "Python"),
            ("javascript", "JavaScript"),
            ("html", "HTML"),
            ("css", "CSS"),
        ],
        default="python",
        help_text="Programming language"
    )
    code = blocks.TextBlock(required=True, help_text="Paste your code here")

    class Meta:
        icon = "code"
        label = "Code Block"
        template = "blocks/code_block.html"


class PullQuoteBlock(blocks.StructBlock):
    """A pull-quote block with a quote and optional attribution."""
    quote = blocks.TextBlock(required=True, help_text="Quote text")
    attribution = blocks.CharBlock(required=False, help_text="Who said it?")

    class Meta:
        icon = "openquote"
        label = "Pull Quote"
        template = "blocks/pull_quote_block.html"


class CallToActionBlock(blocks.StructBlock):
    """A call to action block with title, text, and a link button."""
    title = blocks.CharBlock(required=True)
    text = blocks.TextBlock(required=False)
    button = LinkBlock(required=True, help_text="Button link URL")

    class Meta:
        icon = "placeholder"
        label = "Call To Action"
        template = "blocks/call_to_action_block.html"


class ImageGalleryBlock(blocks.StructBlock):
    """A gallery block with a list of images."""
    gallery_title = blocks.CharBlock(required=False, help_text="Optional gallery title")
    images = blocks.ListBlock(ImageChooserBlock(label="Gallery Image"))

    class Meta:
        icon = "image"
        label = "Image Gallery"
        template = "blocks/image_gallery_block.html"


class EmbedVideoBlock(EmbedBlock):
    """A simple embed block for videos or other embedded content."""
    class Meta:
        icon = "media"
        label = "Embed Video"
        template = "blocks/embed_video_block.html"



class BlogCardBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=True, help_text="Blog card image")
    heading = blocks.CharBlock(required=True, help_text="Title of the blog post")
    publication_date = blocks.DateBlock(required=True, help_text="Publication date")
    excerpt = blocks.TextBlock(required=False, help_text="Short excerpt from the blog post")
    button = LinkBlock(required=False, help_text="Card Button (optional)")
    style = blocks.ChoiceBlock(
        choices=[
            ('modern', 'Modern Clean'),
            ('minimal', 'Minimal'),
            ('premium', 'Premium'),
        ],
        default='modern',
        help_text="Choose the card style"
    )

    class Meta:
        template = "blocks/blog_card_block.html"
        icon = "doc-full-inverse"
        label = "Blog Card"

class BlogCardsListBlock(blocks.ListBlock):
    def __init__(self, **kwargs):
        super().__init__(BlogCardBlock(), **kwargs)

    class Meta:
        icon = "list-ul"
        label = "List of Blog Cards"
        template = "blocks/blog_cards_list_block.html"

class CommonBlockStream(blocks.StreamBlock):
    """StreamBlock containing all the blocks defined above."""
    heading = HeadingBlock()
    paragraph = ParagraphBlock()
    code = CodeBlock()
    pull_quote = PullQuoteBlock()
    call_to_action = CallToActionBlock()
    image = ImageChooserBlock()
    image_gallery = ImageGalleryBlock()
    embed_video = EmbedVideoBlock()
    blog_cards = BlogCardsListBlock()
    ads_and_analytics = CommonBlockStreamWithAds()

    class Meta:
        icon = "placeholder"
        label = "Common Blocks"


class LinkBlockAdapter(StructBlockAdapter):
    js_constructor = 'tech_blog_wagtail.base_page.blocks.LinkBlock'

    @cached_property
    def media(self):
        structblock_media = super().media
        return forms.Media(
            js=structblock_media._js + ['js/link-block.js'],
            css=structblock_media._css
        )


register(LinkBlockAdapter(), LinkBlock)
