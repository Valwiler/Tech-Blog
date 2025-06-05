# tech_blog_wagtail/templatetags/ad_tags.py
from django import template
from django.utils.safestring import mark_safe
from wagtail.models import Site
import random

register = template.Library()


@register.inclusion_tag('tags/ad_zone.html', takes_context=True)
def ad_zone(context, zone='sidebar', size='responsive', custom_slot=None):
    """Render an ad zone"""
    request = context.get('request')
    if not request:
        return {}

    site = Site.find_for_request(request)
    if not site:
        return {}

    from ..models import AdSettings
    ad_settings = AdSettings.for_site(site)

    # Check if ads are enabled
    if not ad_settings.enable_ads:
        return {}

    # Check if zone is enabled
    zone_enabled = {
        'header': ad_settings.enable_header_ads,
        'sidebar': ad_settings.enable_sidebar_ads,
        'footer': ad_settings.enable_footer_ads,
        'content': ad_settings.enable_in_content_ads,
    }.get(zone, True)

    if not zone_enabled:
        return {}

    # Check if ads disabled for logged-in users
    if ad_settings.disable_ads_for_logged_in and request.user.is_authenticated:
        return {}

    # Generate unique ad ID for this placement
    ad_id = f"ad-{zone}-{random.randint(1000, 9999)}"

    return {
        'ad_settings': ad_settings,
        'zone': zone,
        'size': size,
        'custom_slot': custom_slot,
        'ad_id': ad_id,
        'lazy_load': ad_settings.lazy_load_ads,
    }


@register.simple_tag(takes_context=True)
def should_show_ad(context, ad_number=1):
    """Check if an ad should be shown based on frequency settings"""
    request = context.get('request')
    if not request:
        return False

    site = Site.find_for_request(request)
    if not site:
        return False

    from ..models import AdSettings
    ad_settings = AdSettings.for_site(site)

    if not ad_settings.enable_ads or not ad_settings.enable_in_content_ads:
        return False

    if ad_settings.disable_ads_for_logged_in and request.user.is_authenticated:
        return False

    # Check max ads per page
    shown_ads = context.get('shown_ads', 0)
    if shown_ads >= ad_settings.max_ads_per_page:
        return False

    # Check frequency
    if ad_settings.in_content_ad_frequency == 0:
        return False

    return ad_number % ad_settings.in_content_ad_frequency == 0


@register.simple_tag(takes_context=True)
def increment_ad_count(context):
    """Increment the shown ads counter"""
    context['shown_ads'] = context.get('shown_ads', 0) + 1
    return ''


@register.inclusion_tag('tags/ad_scripts.html', takes_context=True)
def ad_scripts(context):
    """Render ad provider scripts (for header)"""
    request = context.get('request')
    if not request:
        return {}

    site = Site.find_for_request(request)
    if not site:
        return {}

    from ..models import AdSettings
    ad_settings = AdSettings.for_site(site)

    if not ad_settings.enable_ads:
        return {}

    if ad_settings.disable_ads_for_logged_in and request.user.is_authenticated:
        return {}

    return {
        'ad_settings': ad_settings,
    }
