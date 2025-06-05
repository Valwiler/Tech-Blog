# base_page/ad_blocks.py
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class AdZoneBlock(blocks.StructBlock):
    """A block for placing ads within content"""

    AD_SIZE_CHOICES = [
        ('responsive', 'Responsive'),
        ('banner', 'Banner (728x90)'),
        ('leaderboard', 'Leaderboard (728x90)'),
        ('medium_rectangle', 'Medium Rectangle (300x250)'),
        ('large_rectangle', 'Large Rectangle (336x280)'),
        ('skyscraper', 'Skyscraper (120x600)'),
        ('wide_skyscraper', 'Wide Skyscraper (160x600)'),
        ('half_page', 'Half Page (300x600)'),
        ('square', 'Square (250x250)'),
        ('small_square', 'Small Square (200x200)'),
        ('custom', 'Custom Size'),
    ]

    AD_TYPE_CHOICES = [
        ('display', 'Display Ad'),
        ('native', 'Native Ad'),
        ('in_feed', 'In-Feed Ad'),
        ('in_article', 'In-Article Ad'),
        ('matched_content', 'Matched Content'),
        ('custom', 'Custom Ad Code'),
    ]

    ad_type = blocks.ChoiceBlock(
        choices=AD_TYPE_CHOICES,
        default='display',
        help_text="Type of ad to display"
    )

    ad_size = blocks.ChoiceBlock(
        choices=AD_SIZE_CHOICES,
        default='responsive',
        help_text="Ad size (for display ads)"
    )

    custom_width = blocks.IntegerBlock(
        required=False,
        help_text="Custom width in pixels (if custom size selected)"
    )

    custom_height = blocks.IntegerBlock(
        required=False,
        help_text="Custom height in pixels (if custom size selected)"
    )

    ad_slot = blocks.CharBlock(
        required=False,
        help_text="Ad slot/unit ID (e.g., for AdSense)"
    )

    custom_ad_code = blocks.TextBlock(
        required=False,
        help_text="Custom ad code (overrides other settings)"
    )

    alignment = blocks.ChoiceBlock(
        choices=[
            ('left', 'Left'),
            ('center', 'Center'),
            ('right', 'Right'),
        ],
        default='center',
        help_text="Ad alignment"
    )

    disable_on_mobile = blocks.BooleanBlock(
        default=False,
        required=False,
        help_text="Hide this ad on mobile devices"
    )

    class Meta:
        template = 'blocks/ad_zone_block.html'
        icon = 'placeholder'
        label = 'Advertisement'


class SponsoredContentBlock(blocks.StructBlock):
    """A block for sponsored content/native advertising"""

    sponsor_name = blocks.CharBlock(
        help_text="Name of the sponsor"
    )

    sponsor_logo = ImageChooserBlock(
        required=False,
        help_text="Sponsor's logo"
    )

    title = blocks.CharBlock(
        help_text="Sponsored content title"
    )

    description = blocks.TextBlock(
        help_text="Brief description of sponsored content"
    )

    link_url = blocks.URLBlock(
        help_text="Link to sponsored content"
    )

    link_text = blocks.CharBlock(
        default="Learn More",
        help_text="Call-to-action text"
    )

    disclosure_text = blocks.CharBlock(
        default="Sponsored",
        help_text="Disclosure label"
    )

    tracking_code = blocks.TextBlock(
        required=False,
        help_text="Additional tracking code for this sponsored content"
    )

    class Meta:
        template = 'blocks/sponsored_content_block.html'
        icon = 'pick'
        label = 'Sponsored Content'


class AffiliateProductBlock(blocks.StructBlock):
    """A block for affiliate product recommendations"""

    product_name = blocks.CharBlock(
        help_text="Product name"
    )

    product_image = ImageChooserBlock(
        help_text="Product image"
    )

    description = blocks.TextBlock(
        help_text="Product description"
    )

    price = blocks.CharBlock(
        required=False,
        help_text="Product price (e.g., $29.99)"
    )

    affiliate_link = blocks.URLBlock(
        help_text="Affiliate link to product"
    )

    button_text = blocks.CharBlock(
        default="Check Price",
        help_text="Button text"
    )

    disclosure_text = blocks.CharBlock(
        default="As an Amazon Associate, I earn from qualifying purchases.",
        help_text="Affiliate disclosure"
    )

    rating = blocks.DecimalBlock(
        required=False,
        min_value=0,
        max_value=5,
        help_text="Product rating (0-5)"
    )

    pros = blocks.ListBlock(
        blocks.CharBlock(),
        required=False,
        help_text="Product pros/advantages"
    )

    cons = blocks.ListBlock(
        blocks.CharBlock(),
        required=False,
        help_text="Product cons/disadvantages"
    )

    class Meta:
        template = 'blocks/affiliate_product_block.html'
        icon = 'tag'
        label = 'Affiliate Product'


# Update CommonBlockStream to include ad blocks

class CommonBlockStreamWithAds(blocks.StreamBlock):
    """Extended StreamBlock with advertising blocks"""
    ad_zone = AdZoneBlock()
    sponsored_content = SponsoredContentBlock()
    affiliate_product = AffiliateProductBlock()
