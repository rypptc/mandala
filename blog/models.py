from django.db import models
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.search import index
from wagtail.fields import RichTextField, StreamField
from core.blocks import BaseStreamBlock
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import Tag, TaggedItemBase
from modelcluster.fields import ParentalKey
from django_comments_xtd.models import XtdComment
from core.models import CustomUser
import datetime



class BlogIndexPage(Page):
        max_count = 1
        subpage_types = [
            "blog.PostPage",
        ]

        intro = RichTextField(blank=True)

        content_panels = Page.content_panels + [
            FieldPanel("intro")
        ]

        def get_template(self, request, *args, **kwargs):
            if request.htmx:
                return "blog/components/blog_post_items.html"
            return "blog/blog_index_page.html"


        def get_context(self, request):
            # Update context to include only published posts, ordered by reverse-chron
            context = super().get_context(request)
            # blog_posts = self.get_children().live().filter(alias_of_id__isnull=True).order_by('-first_published_at')
            blog_posts = PostPage.objects.descendant_of(self).filter(alias_of_id__isnull=True).live().public().order_by('-first_published_at')
            if request.GET.get('tag', None):
                tags = request.GET.get('tag')
                blog_posts = blog_posts.filter(tags__slug__in=[tags])
            paginator = Paginator(blog_posts, 3) #@todo: update paginator
            page = request.GET.get("page")
            try:
                 blog_posts = paginator.page(page)

            except PageNotAnInteger:
                 blog_posts = paginator.page(1)

            except EmptyPage:
                 print("No results for page:", page)
                 blog_posts = paginator.page(paginator.num_pages)
                 
            context['blog_posts'] = blog_posts

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
    subpage_types = []
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
        index.SearchField("title"),
        index.SearchField("subtitle"),
        index.SearchField("intro"),
        index.SearchField("body"),
    ]

    def get_absolute_url(self):
        return self.get_url()

    content_panels = Page.content_panels + [
         FieldPanel("subtitle"),
         FieldPanel("intro"),
         FieldPanel("featured_image"),
         FieldPanel("body"),
         FieldPanel("tags"),
    ]

    def save(self, *args, **kwargs):
        # If the author is not set, set it to the currently logged-in user
        if not self.author_id and self.owner:
            self.author = self.owner
        super().save(*args, **kwargs)


class CustomComment(XtdComment):
    page = ParentalKey(PostPage, on_delete=models.CASCADE, related_name='customcomments')

    def save(self, *args, **kwargs):
        if self.user:
            self.user_name = self.user.username
        self.page = PostPage.objects.get(pk=self.object_pk)
        super(CustomComment, self).save(*args, **kwargs)
