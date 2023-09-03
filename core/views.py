from django.shortcuts import render
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from .models import CustomUser
from .forms import CustomUserUpdateForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserUpdateForm
from django.shortcuts import get_object_or_404
from wagtail.users.models import UserProfile
from .forms import CustomAvatarForm



@login_required
def profile_view(request):
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('core:account_profile')
    else:
        form = CustomUserUpdateForm(instance=request.user)

    return render(request, 'account/profile.html', {'form': form})


class CustomUserUpdateView(UpdateView):
    model = CustomUser
    form_class = CustomUserUpdateForm


class CustomUserDeleteView(DeleteView):
    model = CustomUser
    success_url = reverse_lazy('account_signup')


class CustomAvatarUpdateView(UpdateView):
    model = UserProfile
    form_class = CustomAvatarForm
    success_url = "/settings/"  # Change this to the desired success URL


    def get_object(self):
        return get_object_or_404(UserProfile, user=self.request.user)

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('accounts:account_profile')  # Replace with the actual profile page URL name
