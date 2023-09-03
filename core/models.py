from django.contrib.auth.models import AbstractUser
from django.db import models
from languages_plus.models import Language
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from wagtail.users.models import UserProfile



class CustomUser(AbstractUser):
    pass

    def get_absolute_url(self):
        return reverse('account_profile')


class LanguageSkill(models.Model):
    proficiency_choices = [
        ('a1', 'A1'),
        ('a2', 'A2'),
        ('b1', 'B1'),
        ('b2', 'B2'),
        ('c1', 'C1'),
        ('c2', 'C2'),
        ('native', 'Native'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    proficiency_level = models.CharField(max_length=20, choices=proficiency_choices)

    class Meta:
        ordering = ['-proficiency_level', 'language']

    def __str__(self):
        return f"{self.language.name} - {self.get_proficiency_level_display()}"

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=CustomUser)