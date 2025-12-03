import os
from django.db import models
from django.contrib.auth.models import User

from app_auth.api.utils import OverwriteStorage
from app_allergens.models import Allergen, UserAllergen, CustomProfileAllergen
from app_groups.models import Group


def profile_picture_path(instance, filename):
    ext = filename.split('.')[-1].lower()
    if filename.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')):
        return os.path.join('avatars', 'users', f'user_{instance.user.id}', f'profile.{ext}')


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    groups = models.ManyToManyField(Group, blank=True, related_name='members')
    avatar = models.ImageField(upload_to=profile_picture_path, blank=True, null=True, storage=OverwriteStorage())
    created_at = models.DateTimeField(auto_now_add=True)

    allergens = models.ManyToManyField(Allergen, through=UserAllergen, related_name="profiles", blank=True)

    def __str__(self):
        return self.user.username

    def get_allergens(self):
        return UserAllergen.objects.filter(user_profile=self)


class CustomProfile(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='custom_profiles')
    nickname = models.CharField(max_length=100)
    groups = models.ManyToManyField(Group, blank=True, related_name='custom_members')
    created_at = models.DateTimeField(auto_now_add=True)

    allergens = models.ManyToManyField(Allergen, through=CustomProfileAllergen, related_name="custom_profiles", blank=True)

    def __str__(self):
        return self.nickname

    def get_allergens(self):
        return CustomProfileAllergen.objects.filter(custom_profile=self)