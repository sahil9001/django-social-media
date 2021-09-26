from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Users


class UserSerializer(ModelSerializer):
    class Meta:
        model = Users
        fields = ["phone", "username", "fullname", "email", "password"]

    def save(self, **kwargs):
        user = Users.objects.create_user(
            fullname=self.validated_data["fullname"],
            username=self.validated_data["username"],
            email=self.validated_data["email"],
            password=self.validated_data["password"],
            phone=self.validated_data["phone"],
        )
        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)