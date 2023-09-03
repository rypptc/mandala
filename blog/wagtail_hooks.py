from wagtail.contrib.modeladmin.options import (ModelAdmin, modeladmin_register)
from .models import PostPage
from wagtail import hooks


class PostAdmin(ModelAdmin):
    model = PostPage
    menu_label = 'Posts'
    menu_icon = 'doc-full-inverse'
    menu_order = 000
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('title', 'owner')
    search_fields = ('title', 'owner')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        #only show articles from the current user
        return qs.filter(owner=request.user)


modeladmin_register(PostAdmin)

@hooks.register('construct_explorer_page_queryset')
def show_authors_only_their_posts(parent_page, pages, request):
    user_group = request.user.groups.filter(name='Collaborators').exists()
    if user_group:
        pages = pages.filter(owner=request.user)

    return pages