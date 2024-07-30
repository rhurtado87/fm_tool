from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User  # Ensure User model import
from .forms import UserSettingsForm, ProfileForm

from .models import UserProfile  # Import your UserProfile model if extended User model

class SignUpView(CreateView):
    template_name = "registration/signup.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("login")

@login_required
def process_donation(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        message = request.POST.get('message', '')

        # Example: Save donation details to database
        # Donation.objects.create(user=request.user, amount=amount, message=message)

        messages.success(request, 'Thank you for your donation!')
        return redirect('transactions')  # Redirect to transactions page after successful donation
    
    # If request method is not POST (e.g., GET request)
    return redirect('transactions')  # Redirect to transactions page if not a POST request

@login_required
def user_settings(request):
    # Ensure UserProfile exists
    if not hasattr(request.user, 'userprofile'):
        UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        user_form = UserSettingsForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            request.user.email = user_form.cleaned_data['email']
            request.user.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('user_settings')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserSettingsForm(instance=request.user, initial={'email': request.user.email})
        profile_form = ProfileForm(instance=request.user.userprofile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'accounts/user_settings.html', context)

@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to update the session with the new password hash
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password_change')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'registration/password_change.html', {'form': form})
