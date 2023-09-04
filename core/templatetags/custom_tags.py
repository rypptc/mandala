from django import template
from django.contrib.auth.models import Group
from blog.models import BlogIndexPage
from wagtail.models.i18n import Locale
from django.urls import reverse


register = template.Library()

@register.filter(name='is_collaborator')
def is_collaborator(user):
    return user.groups.filter(name='Collaborators').exists()


@register.filter(name='new_post_url')
def new_post_url(request):
    # Get the current language from the request object
    lang_code = request.LANGUAGE_CODE

    try:
        # Try to get the Locale object that matches the lang_code
        locale = Locale.objects.get(language_code=lang_code)

        # Query for the BlogIndexPage that corresponds to the current language
        blog_index = BlogIndexPage.objects.filter(slug='blog', locale=locale).first()

        if blog_index:
            # Get the specific ID of the BlogIndexPage
            specific_id = blog_index.specific.id

            # Construct the URL to add a new post in the current language
            url = reverse('wagtailadmin_pages:add', kwargs={'content_type_app_name': 'blog', 'content_type_model_name': 'postpage', 'parent_page_id': specific_id})

            return url
    except Locale.DoesNotExist:
        pass  # Handle the case where the Locale doesn't exist

    return ''
