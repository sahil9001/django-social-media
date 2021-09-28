from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Posts
from posts import models


class PostSerializer(ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Posts
        fields = ("title", "body", "image_url", "created_at")

    def get_image_url(self, post):
        request = self.context.get("request")
        image_url = post.image.url
        return request.build_absolute_uri(image_url)
