from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='is_collaborator')
def is_collaborator(user):
    return user.groups.filter(name='collaborators').exists()