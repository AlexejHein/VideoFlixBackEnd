from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Video

admin.site.register(CustomUser, UserAdmin)


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'uploaded_at', 'user')
    search_fields = ('title', 'description')
    list_filter = ('uploaded_at', 'user')
