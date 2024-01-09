from django.db import models
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ValidationError

from .models import User, UserRole


###########################################################################
class EmailSMTPSerializer(serializers.Serializer):
    subject = serializers.CharField()
    message = serializers.CharField()
    # recipient = serializers.EmailField()
    
class UserSerializer11(ModelSerializer):
    class Meta:
        model = User
        fields = ["username",  "password"]
        extra_kwargs = {"password" : {"write_only" : True}}

    def create(self, validated_data):
        user = User(username = validated_data["username"])
        user.set_password(validated_data["password"])
        user.save()
        return user
###########################################################################

class UserSerializer(ModelSerializer):
    class Meta :
        model = User
        exclude = ("last_login","created_on","updated_on","is_admin")

    def save(self):
        print(self.validated_data["user_type"])
        user = User(**self.validated_data)
        password = self.validated_data["password"]
        user.set_password(password)
        
        if self.validated_data["user_role"] == "Admin" :
            user.is_admin = True
                
        user.save()
        return user
    
class UserSerializer1(ModelSerializer):
    class Meta :
        model = User
        exclude = ("last_login","created_on","updated_on","is_admin","password")


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)
    model = User

    def validate(self, value):
        if (self.initial_data["old_password"] and self.initial_data["new_password"]
        ) and self.initial_data["confirm_password"]:
            if self.initial_data["new_password"] != self.initial_data["confirm_password"]:
                raise ValidationError({"password": "Passwords must match."})
            return value
        raise ValidationError(
            {
                "old_password": "This field may not be null.",
                "new_password": "This field may not be null.",
                "confirm_password": "This field may not be null.",
            }
        )

    def validate_old_password(self, old_password):
        print("in validate password")
        user = self.context['request'].thisUser
        if not user.check_password(old_password):
            raise serializers.ValidationError("Old password is incorrect.")
        return old_password
    
    def save(self):
        if (
            self.validated_data["old_password"]
            and self.validated_data["new_password"]
            and self.validated_data["confirm_password"]
        ):
            user = self.context['request'].thisUser
            user.set_password(self.validated_data["new_password"])
            user.save()
        return user


class UserAdminSerializer(ModelSerializer):
    class Meta :
        model = User
        fields = ('username','email','mobile_number')


class UserRoleSerializer(ModelSerializer):
    class Meta :
        model = User 
        fields = "__all__"