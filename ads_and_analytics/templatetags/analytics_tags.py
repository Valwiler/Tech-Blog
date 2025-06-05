# tech_blog_wagtail/templatetags/__init__.py
# Empty file to make this directory a Python package

# tech_blog_wagtail/templatetags/analytics_tags.py
from django import template
from django.utils.safestring import mark_safe
from wagtail.models import Site

register = template.Library()


@register.inclusion_tag('tags/analytics_scripts.html', takes_context=True)
def analytics_scripts(context):
    """Render analytics scripts based on settings"""
    request = context.get('request')
    if not request:
        return {}

    site = Site.find_for_request(request)
    if not site:
        return {}

    # Get analytics settings
    from ..models import AnalyticsSettings
    analytics_settings = AnalyticsSettings.for_site(site)

    # Check Do Not Track
    if analytics_settings.respect_do_not_track:
        dnt = request.META.get('HTTP_DNT')
        if dnt == '1':
            return {'analytics_disabled': True}

    return {
        'analytics_settings': analytics_settings,
        'request': request,
    }


@register.inclusion_tag('tags/cookie_consent.html', takes_context=True)
def cookie_consent(context):
    """Render cookie consent banner"""
    request = context.get('request')
    if not request:
        return {}

    site = Site.find_for_request(request)
    if not site:
        return {}

    from ..models import AnalyticsSettings, PrivacySettings
    analytics_settings = AnalyticsSettings.for_site(site)
    privacy_settings = PrivacySettings.for_site(site)

    # Don't show if cookies already accepted or analytics disabled
    if not analytics_settings.enable_cookie_consent:
        return {}

    return {
        'privacy_settings': privacy_settings,
        'request': request,
    }


