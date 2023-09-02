from django.db import models
from wagtail.models import Page, TranslatableMixin
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.search import index
from wagtail.models.i18n import Locale
from wagtail.fields import StreamField
from core.blocks import BaseStreamBlock
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import Tag, TaggedItemBase
from modelcluster.fields import ParentalKey
import datetime
from django.conf import settings
from core.models import CustomUser


class BlogIndexPage(Page):
        subpage_types = [
            "blog.PostPage",
        ]

        intro = RichTextField(blank=True)

        content_panels = Page.content_panels + [
            FieldPanel("intro")
        ]

        def get_context(self, request):
            # Update context to include only published posts, ordered by reverse-chron
            context = super().get_context(request)
            blogpages = self.get_children().live().filter(alias_of_id__isnull=True).order_by('-first_published_at')
            
            print(type(blogpages))
            context['blogpages'] = blogpages
            return context


class PostPageTag(TaggedItemBase):
    """
    This model allows us to create a many-to-many relationship between
    the BlogPage object and tags. There's a longer guide on using it at
    https://docs.wagtail.org/en/stable/reference/pages/model_recipes.html#tagging
    """

    content_object = ParentalKey(
        "PostPage", related_name="tagged_items", on_delete=models.CASCADE
    )

class PostPage(Page):
    subtitle = models.CharField(blank=True, max_length=255)
    intro = models.TextField(help_text="Text to describe the page", blank=True)
    featured_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Landscape mode only; horizontal width between 1000px and 3000px.",
    )
    body = StreamField(
        BaseStreamBlock(), verbose_name="Page body", blank=True, use_json_field=True
    )
    tags = ClusterTaggableManager(through=PostPageTag, blank=True)
    date_published = models.DateField(
         "Date article published", 
         blank=True, 
         null=True,
         default=datetime.datetime.today
         )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    search_fields = Page.search_fields + [
        index.SearchField("body"),
    ]

    content_panels = Page.content_panels + [
         FieldPanel("subtitle"),
         FieldPanel("intro"),
         FieldPanel("featured_image"),
         FieldPanel("body"),
         FieldPanel("tags"),
    ]

    def save(self, *args, **kwargs):
        # If the author is not set, set it to the currently logged-in user
        if not self.author_id and hasattr(self, 'request') and self.request.user.is_authenticated:
            self.author = self.request.user
        super().save(*args, **kwargs)
