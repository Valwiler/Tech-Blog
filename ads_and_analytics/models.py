# tech_blog_wagtail/settings_models.py
from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, TabbedInterface, ObjectList
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting

# Update the settings base.py to include the new app
# Add this to your INSTALLED_APPS in tech_blog_wagtail/settings/base.py:
# 'tech_blog_wagtail',  # Add this line to register your app


@register_setting
class AnalyticsSettings(BaseSiteSetting):
    """Site-wide analytics settings"""

    ANALYTICS_PROVIDER_CHOICES = [
        ('none', 'None'),
        ('google', 'Google Analytics'),
        ('plausible', 'Plausible Analytics'),
        ('matomo', 'Matomo'),
        ('umami', 'Umami'),
        ('custom', 'Custom Script'),
    ]

    # Analytics Provider
    analytics_provider = models.CharField(
        max_length=20,
        choices=ANALYTICS_PROVIDER_CHOICES,
        default='none',
        help_text="Select your analytics provider"
    )

    # Google Analytics
    google_analytics_id = models.CharField(
        max_length=20,
        blank=True,
        help_text="Google Analytics Measurement ID (e.g., G-XXXXXXXXXX)"
    )

    google_analytics_v4 = models.BooleanField(
        default=True,
        help_text="Use Google Analytics 4 (GA4)"
    )

    # Plausible Analytics
    plausible_domain = models.CharField(
        max_length=255,
        blank=True,
        help_text="Your domain as configured in Plausible"
    )

    plausible_script_url = models.URLField(
        blank=True,
        default="https://plausible.io/js/script.js",
        help_text="Plausible script URL (for self-hosted instances)"
    )

    # Matomo
    matomo_url = models.URLField(
        blank=True,
        help_text="Your Matomo instance URL"
    )

    matomo_site_id = models.CharField(
        max_length=10,
        blank=True,
        help_text="Matomo Site ID"
    )

    # Umami
    umami_script_url = models.URLField(
        blank=True,
        help_text="Umami script URL"
    )

    umami_website_id = models.CharField(
        max_length=50,
        blank=True,
        help_text="Umami Website ID"
    )

    # Custom Script
    custom_analytics_script = models.TextField(
        blank=True,
        help_text="Paste your custom analytics script here (including <script> tags)"
    )

    # Privacy Settings
    enable_anonymize_ip = models.BooleanField(
        default=True,
        help_text="Anonymize visitor IP addresses"
    )

    respect_do_not_track = models.BooleanField(
        default=False,
        help_text="Respect Do Not Track browser setting"
    )

    enable_cookie_consent = models.BooleanField(
        default=True,
        help_text="Show cookie consent banner"
    )

    panels = [
        MultiFieldPanel([
            FieldPanel('analytics_provider'),
        ], heading="Analytics Provider"),

        MultiFieldPanel([
            FieldPanel('google_analytics_id'),
            FieldPanel('google_analytics_v4'),
        ], heading="Google Analytics", classname="collapsible collapsed"),

        MultiFieldPanel([
            FieldPanel('plausible_domain'),
            FieldPanel('plausible_script_url'),
        ], heading="Plausible Analytics", classname="collapsible collapsed"),

        MultiFieldPanel([
            FieldPanel('matomo_url'),
            FieldPanel('matomo_site_id'),
        ], heading="Matomo", classname="collapsible collapsed"),

        MultiFieldPanel([
            FieldPanel('umami_script_url'),
            FieldPanel('umami_website_id'),
        ], heading="Umami", classname="collapsible collapsed"),

        MultiFieldPanel([
            FieldPanel('custom_analytics_script'),
        ], heading="Custom Analytics", classname="collapsible collapsed"),

        MultiFieldPanel([
            FieldPanel('enable_anonymize_ip'),
            FieldPanel('respect_do_not_track'),
            FieldPanel('enable_cookie_consent'),
        ], heading="Privacy Settings"),
    ]

    class Meta:
        verbose_name = "Analytics Settings"


@register_setting
class AdSettings(BaseSiteSetting):
    """Site-wide advertising settings"""

    AD_PROVIDER_CHOICES = [
        ('none', 'None'),
        ('adsense', 'Google AdSense'),
        ('media_net', 'Media.net'),
        ('amazon', 'Amazon Associates'),
        ('taboola', 'Taboola'),
        ('outbrain', 'Outbrain'),
        ('custom', 'Custom Ad Code'),
    ]

    # Global Ad Settings
    enable_ads = models.BooleanField(
        default=False,
        help_text="Enable advertising on the site"
    )

    ad_provider = models.CharField(
        max_length=20,
        choices=AD_PROVIDER_CHOICES,
        default='none',
        help_text="Select your primary ad provider"
    )

    # Google AdSense
    adsense_client_id = models.CharField(
        max_length=50,
        blank=True,
        help_text="Google AdSense Client ID (e.g., ca-pub-XXXXXXXXXXXXXXXX)"
    )

    enable_auto_ads = models.BooleanField(
        default=False,
        help_text="Enable Google Auto Ads"
    )

    # Media.net
    media_net_cid = models.CharField(
        max_length=50,
        blank=True,
        help_text="Media.net Customer ID"
    )

    # Amazon Associates
    amazon_tracking_id = models.CharField(
        max_length=50,
        blank=True,
        help_text="Amazon Associates Tracking ID"
    )

    # Custom Ad Provider
    custom_ad_script = models.TextField(
        blank=True,
        help_text="Custom ad provider script (for header)"
    )

    # Ad Zones Configuration
    enable_header_ads = models.BooleanField(
        default=False,
        help_text="Show ads in header area"
    )

    enable_sidebar_ads = models.BooleanField(
        default=True,
        help_text="Show ads in sidebar"
    )

    enable_in_content_ads = models.BooleanField(
        default=True,
        help_text="Show ads within content"
    )

    enable_footer_ads = models.BooleanField(
        default=False,
        help_text="Show ads in footer area"
    )

    # Ad Frequency
    in_content_ad_frequency = models.IntegerField(
        default=3,
        help_text="Show in-content ad every N paragraphs (0 to disable)"
    )

    max_ads_per_page = models.IntegerField(
        default=5,
        help_text="Maximum number of ads per page"
    )

    # Ad Behavior
    disable_ads_for_logged_in = models.BooleanField(
        default=False,
        help_text="Don't show ads to logged-in users"
    )

    lazy_load_ads = models.BooleanField(
        default=True,
        help_text="Lazy load ads for better performance"
    )

    panels = [
        MultiFieldPanel([
            FieldPanel('enable_ads'),
            FieldPanel('ad_provider'),
        ], heading="General Settings"),

        MultiFieldPanel([
            FieldPanel('adsense_client_id'),
            FieldPanel('enable_auto_ads'),
        ], heading="Google AdSense", classname="collapsible collapsed"),

        MultiFieldPanel([
            FieldPanel('media_net_cid'),
        ], heading="Media.net", classname="collapsible collapsed"),

        MultiFieldPanel([
            FieldPanel('amazon_tracking_id'),
        ], heading="Amazon Associates", classname="collapsible collapsed"),

        MultiFieldPanel([
            FieldPanel('custom_ad_script'),
        ], heading="Custom Ad Provider", classname="collapsible collapsed"),

        MultiFieldPanel([
            FieldPanel('enable_header_ads'),
            FieldPanel('enable_sidebar_ads'),
            FieldPanel('enable_in_content_ads'),
            FieldPanel('enable_footer_ads'),
        ], heading="Ad Zones"),

        MultiFieldPanel([
            FieldPanel('in_content_ad_frequency'),
            FieldPanel('max_ads_per_page'),
        ], heading="Ad Frequency"),

        MultiFieldPanel([
            FieldPanel('disable_ads_for_logged_in'),
            FieldPanel('lazy_load_ads'),
        ], heading="Ad Behavior"),
    ]

    class Meta:
        verbose_name = "Advertising Settings"


@register_setting
class PrivacySettings(BaseSiteSetting):
    """Privacy and cookie consent settings"""

    # Cookie Consent
    cookie_consent_message = models.TextField(
        default="We use cookies to improve your experience and analyze site traffic. By continuing, you agree to our use of cookies.",
        help_text="Message shown in cookie consent banner"
    )

    cookie_consent_button_text = models.CharField(
        max_length=50,
        default="Accept",
        help_text="Text for the accept button"
    )

    cookie_consent_link_text = models.CharField(
        max_length=50,
        default="Learn more",
        help_text="Text for the privacy policy link"
    )

    privacy_policy_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Link to privacy policy page"
    )

    # GDPR Options
    enable_gdpr_features = models.BooleanField(
        default=True,
        help_text="Enable GDPR compliance features"
    )

    allow_cookie_preferences = models.BooleanField(
        default=True,
        help_text="Allow users to manage cookie preferences"
    )

    panels = [
        MultiFieldPanel([
            FieldPanel('cookie_consent_message'),
            FieldPanel('cookie_consent_button_text'),
            FieldPanel('cookie_consent_link_text'),
            FieldPanel('privacy_policy_page'),
        ], heading="Cookie Consent"),

        MultiFieldPanel([
            FieldPanel('enable_gdpr_features'),
            FieldPanel('allow_cookie_preferences'),
        ], heading="GDPR Settings"),
    ]

    class Meta:
        verbose_name = "Privacy Settings"


@register_setting
class AnalyticsSettings(BaseSiteSetting):
    """Site-wide analytics settings"""

    ANALYTICS_PROVIDER_CHOICES = [
        ('none', 'None'),
        ('google', 'Google Analytics'),
        ('plausible', 'Plausible Analytics'),
        ('matomo', 'Matomo'),
        ('umami', 'Umami'),
        ('custom', 'Custom Script'),
    ]

    # Analytics Provider
    analytics_provider = models.CharField(
        max_length=20,
        choices=ANALYTICS_PROVIDER_CHOICES,
        default='none',
        help_text="Select your analytics provider"
    )

    # Google Analytics
    google_analytics_id = models.CharField(
        max_length=20,
        blank=True,
        help_text="Google Analytics Measurement ID (e.g., G-XXXXXXXXXX)"
    )

    google_analytics_v4 = models.BooleanField(
        default=True,
        help_text="Use Google Analytics 4 (GA4)"
    )

    # Plausible Analytics
    plausible_domain = models.CharField(
        max_length=255,
        blank=True,
        help_text="Your domain as configured in Plausible"
    )

    plausible_script_url = models.URLField(
        blank=True,
        default="https://plausible.io/js/script.js",
        help_text="Plausible script URL (for self-hosted instances)"
    )

    # Matomo
    matomo_url = models.URLField(
        blank=True,
        help_text="Your Matomo instance URL"
    )

    matomo_site_id = models.CharField(
        max_length=10,
        blank=True,
        help_text="Matomo Site ID"
    )

    # Umami
    umami_script_url = models.URLField(
        blank=True,
        help_text="Umami script URL"
    )

    umami_website_id = models.CharField(
        max_length=50,
        blank=True,
        help_text="Umami Website ID"
    )

    # Custom Script
    custom_analytics_script = models.TextField(
        blank=True,
        help_text="Paste your custom analytics script here (including <script> tags)"
    )

    # Privacy Settings
    enable_anonymize_ip = models.BooleanField(
        default=True,
        help_text="Anonymize visitor IP addresses"
    )

    respect_do_not_track = models.BooleanField(
        default=False,
        help_text="Respect Do Not Track browser setting"
    )

    enable_cookie_consent = models.BooleanField(
        default=True,
        help_text="Show cookie consent banner"
    )

    panels = [
        MultiFieldPanel([
            FieldPanel('analytics_provider'),
        ], heading="Analytics Provider"),

        MultiFieldPanel([
            FieldPanel('google_analytics_id'),
            FieldPanel('google_analytics_v4'),
        ], heading="Google Analytics", classname="collapsible collapsed"),

        MultiFieldPanel([
            FieldPanel('plausible_domain'),
            FieldPanel('plausible_script_url'),
        ], heading="Plausible Analytics", classname="collapsible collapsed"),

        MultiFieldPanel([
            FieldPanel('matomo_url'),
            FieldPanel('matomo_site_id'),
        ], heading="Matomo", classname="collapsible collapsed"),

        MultiFieldPanel([
            FieldPanel('umami_script_url'),
            FieldPanel('umami_website_id'),
        ], heading="Umami", classname="collapsible collapsed"),

        MultiFieldPanel([
            FieldPanel('custom_analytics_script'),
        ], heading="Custom Analytics", classname="collapsible collapsed"),

        MultiFieldPanel([
            FieldPanel('enable_anonymize_ip'),
            FieldPanel('respect_do_not_track'),
            FieldPanel('enable_cookie_consent'),
        ], heading="Privacy Settings"),
    ]

    class Meta:
        verbose_name = "Analytics Settings"


@register_setting
class AdSettings(BaseSiteSetting):
    """Site-wide advertising settings"""

    AD_PROVIDER_CHOICES = [
        ('none', 'None'),
        ('adsense', 'Google AdSense'),
        ('media_net', 'Media.net'),
        ('amazon', 'Amazon Associates'),
        ('taboola', 'Taboola'),
        ('outbrain', 'Outbrain'),
        ('custom', 'Custom Ad Code'),
    ]

    # Global Ad Settings
    enable_ads = models.BooleanField(
        default=False,
        help_text="Enable advertising on the site"
    )

    ad_provider = models.CharField(
        max_length=20,
        choices=AD_PROVIDER_CHOICES,
        default='none',
        help_text="Select your primary ad provider"
    )

    # Google AdSense
    adsense_client_id = models.CharField(
        max_length=50,
        blank=True,
        help_text="Google AdSense Client ID (e.g., ca-pub-XXXXXXXXXXXXXXXX)"
    )

    enable_auto_ads = models.BooleanField(
        default=False,
        help_text="Enable Google Auto Ads"
    )

    # Media.net
    media_net_cid = models.CharField(
        max_length=50,
        blank=True,
        help_text="Media.net Customer ID"
    )

    # Amazon Associates
    amazon_tracking_id = models.CharField(
        max_length=50,
        blank=True,
        help_text="Amazon Associates Tracking ID"
    )

    # Custom Ad Provider
    custom_ad_script = models.TextField(
        blank=True,
        help_text="Custom ad provider script (for header)"
    )

    # Ad Zones Configuration
    enable_header_ads = models.BooleanField(
        default=False,
        help_text="Show ads in header area"
    )

    enable_sidebar_ads = models.BooleanField(
        default=True,
        help_text="Show ads in sidebar"
    )

    enable_in_content_ads = models.BooleanField(
        default=True,
        help_text="Show ads within content"
    )

    enable_footer_ads = models.BooleanField(
        default=False,
        help_text="Show ads in footer area"
    )

    # Ad Frequency
    in_content_ad_frequency = models.IntegerField(
        default=3,
        help_text="Show in-content ad every N paragraphs (0 to disable)"
    )

    max_ads_per_page = models.IntegerField(
        default=5,
        help_text="Maximum number of ads per page"
    )

    # Ad Behavior
    disable_ads_for_logged_in = models.BooleanField(
        default=False,
        help_text="Don't show ads to logged-in users"
    )

    lazy_load_ads = models.BooleanField(
        default=True,
        help_text="Lazy load ads for better performance"
    )

    panels = [
        MultiFieldPanel([
            FieldPanel('enable_ads'),
            FieldPanel('ad_provider'),
        ], heading="General Settings"),

        MultiFieldPanel([
            FieldPanel('adsense_client_id'),
            FieldPanel('enable_auto_ads'),
        ], heading="Google AdSense", classname="collapsible collapsed"),

        MultiFieldPanel([
            FieldPanel('media_net_cid'),
        ], heading="Media.net", classname="collapsible collapsed"),

        MultiFieldPanel([
            FieldPanel('amazon_tracking_id'),
        ], heading="Amazon Associates", classname="collapsible collapsed"),

        MultiFieldPanel([
            FieldPanel('custom_ad_script'),
        ], heading="Custom Ad Provider", classname="collapsible collapsed"),

        MultiFieldPanel([
            FieldPanel('enable_header_ads'),
            FieldPanel('enable_sidebar_ads'),
            FieldPanel('enable_in_content_ads'),
            FieldPanel('enable_footer_ads'),
        ], heading="Ad Zones"),

        MultiFieldPanel([
            FieldPanel('in_content_ad_frequency'),
            FieldPanel('max_ads_per_page'),
        ], heading="Ad Frequency"),

        MultiFieldPanel([
            FieldPanel('disable_ads_for_logged_in'),
            FieldPanel('lazy_load_ads'),
        ], heading="Ad Behavior"),
    ]

    class Meta:
        verbose_name = "Advertising Settings"


@register_setting
class PrivacySettings(BaseSiteSetting):
    """Privacy and cookie consent settings"""

    # Cookie Consent
    cookie_consent_message = models.TextField(
        default="We use cookies to improve your experience and analyze site traffic. By continuing, you agree to our use of cookies.",
        help_text="Message shown in cookie consent banner"
    )

    cookie_consent_button_text = models.CharField(
        max_length=50,
        default="Accept",
        help_text="Text for the accept button"
    )

    cookie_consent_link_text = models.CharField(
        max_length=50,
        default="Learn more",
        help_text="Text for the privacy policy link"
    )

    privacy_policy_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Link to privacy policy page"
    )

    # GDPR Options
    enable_gdpr_features = models.BooleanField(
        default=True,
        help_text="Enable GDPR compliance features"
    )

    allow_cookie_preferences = models.BooleanField(
        default=True,
        help_text="Allow users to manage cookie preferences"
    )

    panels = [
        MultiFieldPanel([
            FieldPanel('cookie_consent_message'),
            FieldPanel('cookie_consent_button_text'),
            FieldPanel('cookie_consent_link_text'),
            FieldPanel('privacy_policy_page'),
        ], heading="Cookie Consent"),

        MultiFieldPanel([
            FieldPanel('enable_gdpr_features'),
            FieldPanel('allow_cookie_preferences'),
        ], heading="GDPR Settings"),
    ]

    class Meta:
        verbose_name = "Privacy Settings"
