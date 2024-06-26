# core/tasks.py
from celery import shared_task


@shared_task
def convert_video(video_id):
    # Video-Konvertierungslogik hier
    pass
