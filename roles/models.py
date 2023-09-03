from django.db import models
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect


from wagtail.contrib.forms.models import (
    AbstractEmailForm,
    AbstractFormField
)
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel
)
from wagtail.fields import RichTextField
from wagtailcaptcha.models import WagtailCaptchaEmailForm


class CollaboratorRequestFormField(AbstractFormField):
    page = ParentalKey(
        'CollaboratorRequestPage',
        on_delete=models.CASCADE,
        related_name='form_fields',
    )

class CollaboratorRequestPage(WagtailCaptchaEmailForm):
    template = "collaborator/collaborator_request_page.html"
    subpage_types = []
    parent_page_types = ['home.HomePage']

    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro'),
        InlinePanel('form_fields', label='Form Fields'),
        FieldPanel('thank_you_text'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel("subject"),
        ], heading="Collaborator Request"),
    ]


    def serve(self, request, *args, **kwargs):
        user = request.user

        if not (
            user.first_name and
            user.last_name and
            user.email and
            user.languageskill_set.count() >= 2
        ):
            messages.error(request, "Your profile is incomplete. Please fill in your first name, last name, email, and include at least two language skills.")
            return redirect(reverse('core:account_profile'))

        return super().serve(request, *args, **kwargs)




