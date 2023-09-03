from django import forms
from allauth.account.forms import SignupForm
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django.forms import ModelForm
from .models import CustomUser
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
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email']


# Create a custom avatar form to update the profile image in the frontend
class CustomAvatarForm(forms.ModelForm):
    avatar = forms.ImageField()

    def clean_avatar(self):
        avatar = self.cleaned_data.get("avatar", False)
        file_size = avatar.size
        limit_kb = 2000
        if avatar:
            if file_size > limit_kb * 1024:
                raise ValidationError("The maximum file size is 2 MB.")
            return avatar
        else:
            raise ValidationError("Couldn't read uploaded image")

    class Meta:
        model = UserProfile
        fields = ["avatar"]