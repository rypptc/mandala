from django import forms
from allauth.account.forms import SignupForm
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django.forms import ModelForm
from .models import CustomUser, LanguageSkill
from django.core.exceptions import ValidationError
from wagtail.users.models import UserProfile


# Adding captcha to the frontend user signup form
class CustomSignupForm(SignupForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    def save(self, request):

        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(CustomSignupForm, self).save(request)

        # Add your own processing here.

        # You must return the original result.
        return user

# This form is used in the django profile view
class CustomUserUpdateForm(ModelForm):
    avatar = forms.ImageField(label='Profile Picture', required=False, widget=forms.FileInput())

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email']


class LanguageSkillForm(forms.ModelForm):
    class Meta:
        model = LanguageSkill
        fields = (
            'language',
            'proficiency_level',
        )