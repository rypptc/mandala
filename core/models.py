from django.contrib.auth.models import AbstractUser
from django.db import models
from languages_plus.models import Language
from django.urls import reverse


class CustomUser(AbstractUser):
    pass

class LanguageSkill(models.Model):
    proficiency_choices = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('native', 'Native'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    proficiency_level = models.CharField(max_length=20, choices=proficiency_choices)

    def __str__(self):
        return f"{self.language.name} - {self.get_proficiency_level_display()}"
