from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.core.files.base import ContentFile
from moviepy.editor import VideoFileClip
from PIL import Image
import os
from io import BytesIO


class CustomUser(AbstractUser):
    pass


class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='videos/')
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)

        if not self.thumbnail:
            self.generate_thumbnail()

        super().save(*args, **kwargs)

    def generate_thumbnail(self):
        video_path = self.file.path
        thumbnail_path = os.path.join(settings.MEDIA_ROOT, 'thumbnails', f"{self.pk}.jpg")

        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found at path: {video_path}")

        try:
            clip = VideoFileClip(video_path)
            frame = clip.get_frame(1)

            image = Image.fromarray(frame)
            thumbnail_io = BytesIO()
            image.save(thumbnail_io, format='JPEG')
            self.thumbnail.save(os.path.basename(thumbnail_path), ContentFile(thumbnail_io.getvalue()), save=False)
        except Exception as e:
            raise RuntimeError(f"Saving thumbnail failed: {e}")
