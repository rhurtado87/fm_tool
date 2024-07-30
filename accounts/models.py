from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add additional fields as needed for your user profile
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default_avatar.png')
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.user.username



