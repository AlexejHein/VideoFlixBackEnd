# core/serializers.py
from django.db import transaction
from rest_framework import serializers
from .models import Video, CustomUser
from django.contrib.auth import get_user_model


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        try:
            with transaction.atomic():
                user = CustomUser(
                    email=validated_data['email'],
                    username=validated_data['username'],
                    first_name=validated_data['first_name'],
                    last_name=validated_data['last_name'],
                )
                user.set_password(validated_data['password'])
                user.save()
                return user
        except Exception as e:
            # Hier können Sie spezifische Ausnahmen behandeln oder loggen
            raise serializers.ValidationError({"error": "Fehler bei der Benutzererstellung."})


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
