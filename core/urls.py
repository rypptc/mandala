from django.urls import path
from .views import profile_view, CustomAvatarUpdateView

app_name = 'core'

urlpatterns = [
    path('profile/', profile_view, name='account_profile'),
    path('update-avatar/', CustomAvatarUpdateView.as_view(), name='update-avatar'),
]