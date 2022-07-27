from django.db import models
from django.contrib.auth.models import User
from django.core import files
from io import BytesIO
from PIL import Image

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    picture = models.ImageField(upload_to = 'profile_images', blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        SIZE = 50, 50
        
        if self.picture:
            pic = Image.open(self.picture.path)
            pic.thumbnail(SIZE, Image.LANCZOS)
            pic.save(self.picture.path)

    def __str__(self):
        return self.user.username