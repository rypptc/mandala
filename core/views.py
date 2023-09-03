from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import UpdateView, DeleteView

from .models import CustomUser, LanguageSkill
from .forms import LanguageSkillForm, CustomUserUpdateForm

from wagtail.users.models import UserProfile


@login_required
def profile_view(request):
    user = request.user
    language_skills = LanguageSkill.objects.filter(user=user)

    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        user_profile = None

    # Check if the user is a member of the "collaborators" group
    is_collaborator = user.groups.filter(name='collaborators').exists()


    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()

            # Update the avatar in the UserProfile if it exists
            if user_profile:
                user_profile.avatar = form.cleaned_data['avatar']
                user_profile.save()

            messages.success(request, 'Your profile has been updated.')
            return redirect('accounts:account_profile')
    else:
        form = CustomUserUpdateForm(instance=request.user)

    context = {
        'user': user,
        'language_skills': language_skills,
        'form': form,
        'is_collaborator': is_collaborator
    }

    return render(request, 'account/profile.html', context)



def update_language_skills(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = LanguageSkillForm(request.POST)
        if form.is_valid():
            # Create and save the new language skill
            language_skill = form.save(commit=False)
            language_skill.user = user
            language_skill.save()
            return redirect(request.path)
    else:
        form = LanguageSkillForm()
    
    language_skills = LanguageSkill.objects.filter(user=user)
    
    return render(request, 'account/update_language_skills.html', {'form': form, 'language_skills': language_skills})


def add_language_skill(request):
    if request.method == 'POST':
        form = LanguageSkillForm(request.POST)
        if form.is_valid():
            language_skill = form.save(commit=False)
            language_skill.user = request.user
            language_skill.save()
            return redirect('accounts:update-language-skills')
        
        form = LanguageSkillForm()
    return render(request, 'add_language_skill.html', {'form': form})


def delete_language_skill(request, language_skill_id):
    language_skill = get_object_or_404(LanguageSkill, id=language_skill_id)
    
    if language_skill.user == request.user:
        language_skill.delete()
    
    return redirect('accounts:update-language-skills', user_id=request.user.id)