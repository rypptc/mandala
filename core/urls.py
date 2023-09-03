from django.urls import path
from .views import (
    profile_view,
    update_language_skills,
    delete_language_skill,
    )

app_name = 'core'

urlpatterns = [
    path('profile/', profile_view, name='account_profile'),
    path('update-language-skills/<int:user_id>/', update_language_skills, name='update-language-skills'),
    path('delete-language-skill/<int:language_skill_id>/', delete_language_skill, name='delete-language-skill'),
]