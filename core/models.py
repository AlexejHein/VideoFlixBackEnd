# core/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.core.files.base import ContentFile
import ffmpeg
from io import BytesIO
from PIL import Image


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
        super().save(*args, **kwargs)
        if not self.thumbnail:
            self.generate_thumbnail()

    def generate_thumbnail(self):
        video_path = self.file.path
        thumbnail_path = f"thumbnails/{self.pk}.jpg"

        # Extract a frame from the video using ffmpeg
        out, _ = (
            ffmpeg
            .input(video_path, ss=1)  # ss=1 means 1 second into the video
            .output('pipe:', vframes=1, format='image2', vcodec='mjpeg')
            .run(capture_stdout=True)
        )

        # Save the extracted frame as an image
        image = Image.open(BytesIO(out))
        thumbnail_io = BytesIO()
        image.save(thumbnail_io, format='JPEG')
        self.thumbnail.save(thumbnail_path, ContentFile(thumbnail_io.getvalue()), save=False)
        super().save(update_fields=['thumbnail'])  # Save again to update the thumbnail field
