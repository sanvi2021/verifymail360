from rest_framework import serializers
from authentication.models import *
from django.contrib.auth import get_user_model
User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "password", "username", "email" , "ip_address" ,"browser", "created_at", "last_login")

class SignupCreateSerializer(serializers.ModelSerializer):    
    class Meta:
        model = User
        fields =("email", "password","username")
        
    def create(self, validated_data):
        print("inside the serializer class")
        user = User(
            email=validated_data['email'] ,
            username = validated_data["username"]
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ActivateSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length= 700)

    class Meta:
        model = User