from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, LanguageSkill

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']

# Register the CustomUserAdmin class
admin.site.register(CustomUser, CustomUserAdmin)

class LanguageSkillAdmin(admin.ModelAdmin):
    list_display = ['user', 'language', 'proficiency_level']

admin.site.register(LanguageSkill, LanguageSkillAdmin)