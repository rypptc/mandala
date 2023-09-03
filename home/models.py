from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel


from wagtail.contrib.settings.models import (
    BaseGenericSetting,
    register_setting,
)
from modelcluster.models import ClusterableModel



class HomePage(Page):
    """Home page model"""
    max_count = 3
    parent_page_type = [
        'wagtailcore.Page'
    ]
    subpage_types = [
        'blog.BlogIndexPage',
        'portfolio.PortfolioIndexPage',
        'roles.CollaboratorRequestPage',
    ]
    first_section_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="First Section Image",
    )
    first_section_heading = models.CharField(
        max_length=255,
        blank=True,
        help_text="First Section Heading",
    )
    first_section_text = RichTextField(
        blank=True,
        help_text="First Section Text",
    )
    first_section_cta_text = models.CharField(
        max_length=255,
        blank=True,
        help_text="Text for the Call to Action button",
    )
    first_section_cta_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Choose a page to link to for the Call to Action in the first section",
    )

    first_section_cta_text_2 = models.CharField(
        max_length=255,
        blank=True,
        help_text="Text for the Call to Action button",
    )
    first_section_cta_link_2 = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Choose a page to link to for the Call to Action in the first section",
    )



    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("first_section_image"),
                FieldPanel("first_section_heading"),
                FieldPanel("first_section_text"),
                FieldPanel("first_section_cta_text"),
                FieldPanel("first_section_cta_link"),
                FieldPanel("first_section_cta_text_2"),
                FieldPanel("first_section_cta_link_2"),
            ],
            heading="First Section Image",
        ),

    ]

@register_setting
class GenericSettings(ClusterableModel, BaseGenericSetting):
    instagram_url = models.URLField(verbose_name="Instagram URL", blank=True)
    twitter_url = models.URLField(verbose_name="Twitter URL", blank=True)
    youtube_url = models.URLField(verbose_name="YouTube URL", blank=True)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("instagram_url"),
                FieldPanel("twitter_url"),
                FieldPanel("youtube_url"),
            ],
            heading="Social settings",
        )
    ]