from django.db import models
from core.blocks import BaseStreamBlock
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel

from wagtail.models import Page


class PortfolioIndexPage(Page):
    max_count = 1
    subpage_types = [
        "portfolio.EntryPage",
    ]
    intro_title = models.CharField(max_length=100, null=True, blank=True)
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro_title"),
        FieldPanel("intro")
    ]


class EntryPage(Page):
    subpage_types = [
        "portfolio.EntryPage",
    ]

    template = "portfolio/project_entry_page.html"
    project_title = models.CharField(blank=True, null=True, max_length=255)
    project_description = models.TextField(help_text="Text to describe the project", 
                                           blank=True,
                                           null=True)
    project_detail = StreamField(
        BaseStreamBlock(), 
        verbose_name="Project",
        null=True,
        blank=True,
        use_json_field=True
    )



    content_panels = Page.content_panels + [
        FieldPanel("project_title"),
        FieldPanel("project_description"),
        FieldPanel("project_detail"),
    ]