from django import forms
from allauth.account.forms import SignupForm
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox



class CustomSignupForm(SignupForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    def save(self, request):

        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(CustomSignupForm, self).save(request)

        # Add your own processing here.

        # You must return the original result.
        return user