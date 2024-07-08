# core/management/commands/generate_thumbnails.py
from django.core.management.base import BaseCommand
from core.models import Video


class Command(BaseCommand):
    help = 'Generate thumbnails for videos that do not have thumbnails'

    def handle(self, *args, **kwargs):
        videos_without_thumbnails = Video.objects.filter(thumbnail__isnull=True)
        for video in videos_without_thumbnails:
            video.generate_thumbnail()
            video.save(update_fields=['thumbnail'])  # Save again to update the thumbnail field
            self.stdout.write(self.style.SUCCESS(f'Generated thumbnail for video {video.id}'))
