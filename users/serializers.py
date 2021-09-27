from django.http import request
from posts import models
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Users
from posts.models import Posts

class UserSerializer(ModelSerializer):
    class Meta:
        model = Users
        fields = ["phone", "username", "fullname", "email", "password","occupation","dob","address"]

    def save(self, **kwargs):
        user = Users.objects.create_user(
            fullname=self.validated_data["fullname"],
            username=self.validated_data["username"],
            email=self.validated_data["email"],
            password=self.validated_data["password"],
            phone=self.validated_data["phone"],
            address = self.validated_data["address"],
            dob = self.validated_data["dob"],
            occupation = self.validated_data["occupation"]
        )
        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)

class CreateFormSerializer(ModelSerializer):
    class Meta:
        model = Posts
        fields = ["title","body","image"]
    
    def save(self,user,**kwargs):
        post = Posts.objects.create(
            title = self.validated_data["title"],
            image = self.validated_data["image"],
            body = self.validated_data["body"],
            user = user,
        )
        post.save()
        return post