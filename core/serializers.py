# core/serializers.py
from django.db import transaction
from rest_framework import serializers
from .models import Video, CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password1', 'first_name', 'last_name')
        extra_kwargs = {'password1': {'write_only': True}}

    def create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create_user(
                email=validated_data['email'],
                username=validated_data['username'],
                password=validated_data['password1'],  # Updated to use 'password1'
                first_name=validated_data.get('first_name', ''),
                last_name=validated_data.get('last_name', '')
            )
            return user


class VideoSerializer(serializers.ModelSerializer):
    thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ('id', 'title', 'description', 'file', 'uploaded_at', 'user', 'thumbnail_url')

    def get_thumbnail_url(self, obj):
        request = self.context.get('request')
        if obj.thumbnail:
            return request.build_absolute_uri(obj.thumbnail.url)
        return None
