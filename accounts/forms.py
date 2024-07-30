from django import forms
from .models import UserProfile

from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar']