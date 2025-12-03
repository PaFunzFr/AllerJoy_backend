import os
from django.db import models
from django.contrib.auth.models import User

from app_auth.api.utils import OverwriteStorage
from app_allergies.models import Allergen
from app_groups.models import Group

USER_TYPES = [
    ('business', 'Business'),
    ('customer','Customer')
]

AVATAR_IDS = [(i, str(i)) for i in range(10)]

def profile_picture_path(instance, filename):
    ext = filename.split('.')[-1].lower()
    if filename.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')):
        return os.path.join('avatars', 'users', f'user_{instance.user.id}', f'profile.{ext}')


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    allergens = models.ManyToManyField(Allergen, blank=True)
    groups = models.ManyToManyField(Group, blank=True, related_name='members')
    avatar = models.ImageField(upload_to=profile_picture_path, blank=True, null=True, storage=OverwriteStorage())
    avatar_preset = models.IntegerField(choices=AVATAR_IDS, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def display_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        elif self.avatar_preset != 0:
            return f'/media/avatars/defaults/{self.avatar_preset}.png'
        else:
            return '/media/avatars/defaults/placeholder.png'

    def __str__(self):
        return self.user.username


class CustomProfile(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='custom_profiles')
    nickname = models.CharField(max_length=100)
    allergens = models.ManyToManyField(Allergen, blank=True)
    groups = models.ManyToManyField(Group, blank=True, related_name='custom_members')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nickname