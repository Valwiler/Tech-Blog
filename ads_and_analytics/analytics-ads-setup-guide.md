# Analytics and Advertising Setup Guide for Wagtail Blog

## Overview

I've implemented a comprehensive analytics and advertising system for your Wagtail blog that includes:

- **Multiple Analytics Providers**: Google Analytics, Plausible, Matomo, Umami, or custom scripts
- **Multiple Ad Providers**: Google AdSense, Media.net, Amazon Associates, and more
- **Privacy Compliance**: Cookie consent, GDPR features, Do Not Track support
- **Flexible Ad Placement**: Header, sidebar, footer, and in-content ads
- **Content Blocks**: Ad zones, sponsored content, and affiliate product blocks

## Setup Instructions

### 1. File Structure Setup

Create the following directories and files:

```
tech_blog_wagtail/
├── __init__.py
├── apps.py
├── settings_models.py
├── templatetags/
│   ├── __init__.py
│   ├── analytics_tags.py
│   └── ad_tags.py
└── templates/
    └── tags/
        ├── analytics_scripts.html
        ├── cookie_consent.html
        ├── ad_zone.html
        └── ad_scripts.html

base_page/
├── ad_blocks.py
└── templates/
    └── blocks/
        ├── ad_zone_block.html
        ├── sponsored_content_block.html
        └── affiliate_product_block.html
```

### 2. Update Django Settings

In `tech_blog_wagtail/settings/base.py`, add to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ... other apps
    'tech_blog_wagtail',  # Add this before wagtail apps
    # ... wagtail apps
]
```

### 3. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Configure Analytics in Wagtail Admin

1. Log into Wagtail admin
2. Go to **Settings** → **Analytics Settings**
3. Choose your analytics provider:
   - **Google Analytics**: Enter your Measurement ID (G-XXXXXXXXXX)
   - **Plausible**: Enter your domain
   - **Matomo**: Enter your instance URL and Site ID
   - **Custom**: Paste your analytics script
4. Configure privacy settings as needed

### 5. Configure Advertising

1. In Wagtail admin, go to **Settings** → **Advertising Settings**
2. Enable ads and choose your provider:
   - **Google AdSense**: Enter your Client ID (ca-pub-XXXXXXXXXXXXXXXX)
   - **Media.net**: Enter your Customer ID
   - **Amazon Associates**: Enter your Tracking ID
3. Configure ad zones (header, sidebar, footer, in-content)
4. Set ad frequency and behavior preferences

### 6. Configure Privacy Settings

1. Go to **Settings** → **Privacy Settings**
2. Customize the cookie consent message
3. Link to your privacy policy page
4. Enable GDPR features if needed

## Using Ad Blocks in Content

### Ad Zone Block
Add advertisements within your content:
- Choose ad type (display, native, in-feed, etc.)
- Select size (responsive, banner, rectangle, etc.)
- Optionally disable on mobile devices

### Sponsored Content Block
Create native advertising content:
- Add sponsor name and logo
- Write sponsored content title and description
- Include tracking code if needed
- Automatic disclosure label

### Affiliate Product Block
Showcase affiliate products:
- Add product image and details
- Include price and ratings
- List pros and cons
- Automatic affiliate disclosure

## Template Usage

### In Templates
```django
{% load ad_tags analytics_tags %}

<!-- Add analytics scripts in head -->
{% analytics_scripts %}

<!-- Add ad scripts in head -->
{% ad_scripts %}

<!-- Add cookie consent banner -->
{% cookie_consent %}

<!-- Place ad zones -->
{% ad_zone zone="sidebar" size="medium_rectangle" %}
```

### In Content
When editing pages, you'll see new block options:
- **Advertisement** - Place ads within content
- **Sponsored Content** - Native advertising
- **Affiliate Product** - Product recommendations

## Privacy and Performance

### Privacy Features
- IP anonymization option
- Respect Do Not Track headers
- Cookie consent management
- GDPR compliance tools
- Option to disable ads for logged-in users

### Performance Optimization
- Lazy loading for ads
- Conditional loading based on user preferences
- Efficient script loading
- Responsive ad units

## Revenue Optimization Tips

1. **Ad Placement**:
   - Place ads above the fold for better visibility
   - Use responsive ads for mobile optimization
   - Test different ad sizes and positions

2. **Content Integration**:
   - Use in-content ads every 3-4 paragraphs
   - Place affiliate products in relevant articles
   - Create dedicated review pages with multiple affiliate products

3. **User Experience**:
   - Don't overwhelm users with too many ads
   - Ensure ads don't interfere with content
   - Use lazy loading to improve page speed

## Troubleshooting

### Analytics Not Tracking
- Check if cookie consent is blocking scripts
- Verify analytics ID is correct
- Ensure Do Not Track is not enabled
- Check browser console for errors

### Ads Not Showing
- Verify ad provider credentials
- Check if ads are enabled for the zone
- Ensure you're not logged in (if disabled for logged-in users)
- Ad blockers may be preventing display

### Template Errors
- Ensure `tech_blog_wagtail` is in INSTALLED_APPS
- Check that all template files are in correct locations
- Verify template tag libraries are loaded

## Next Steps

1. Set up your analytics provider account
2. Apply for ad network approval (AdSense, Media.net, etc.)
3. Create privacy and terms of service pages
4. Test cookie consent functionality
5. Monitor analytics and optimize ad placement

The system is designed to be flexible and grow with your blog. You can start with basic analytics and add advertising later when you have sufficient traffic.