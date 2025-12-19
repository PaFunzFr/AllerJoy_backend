import os
from django.db import models
from django.contrib.auth.models import User

from app_auth.api.utils import OverwriteStorage

def group_picture_path(instance, filename):
    ext = filename.split('.')[-1].lower()
    if filename.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')):
        return os.path.join('group_images', f'group_{instance.id}', f'group_image.{ext}')

class Group(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to=group_picture_path, blank=True, storage=OverwriteStorage())
    date = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name