from django.db import models
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ValidationError
from django.contrib.auth.hashers import make_password
from .models import User, UserRole

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
    # old_password = serializers.CharField(required=True)
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
                # "old_password": "This field may not be null.",
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


####################################################################################################################

from django.contrib.auth.hashers import make_password


class UserOTPSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'is_verified', 'password']

    def save(self, **kwargs):
        self.validated_data['password'] = make_password(self.validated_data.get('password'))
        return super().save(**kwargs)

# class VerifyOTPSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     otp = serializers.CharField()

class EmailSMTPSerializer(serializers.Serializer):
    subject = serializers.CharField(max_length=255)
    message = serializers.CharField()

class UserSerializer11(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'create')
    
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return User.objects.create_user(**validated_data)

class UserLatestMember(ModelSerializer):
    created_on = serializers.DateTimeField(format="%b %d, %Y", read_only=True)

    class Meta :
        model = User
        fields = ('username', 'created_on')

class LatestMembersSerializer(serializers.ModelSerializer):
    user_images = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username', 'created_on', 'user_images')

    def get_user_images(self, obj):
        return obj.user_images.url if obj.user_images else None
    
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, data):
        email = data.get('email')

        if not email:
            raise ValidationError({'message': 'Email is required.'})

        user = User.objects.filter(email=email).first()

        if not user:
            raise ValidationError({'message': 'Email not found in the database.'})

        return data
    
class VerifyForgotOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(required=True)

    def validate(self, data):
        email = data.get('email')
        otp = data.get('otp')

        if not (email and otp):
            raise ValidationError({'message': 'Email and OTP are required.'})

        user = User.objects.filter(email=email).first()

        if not user or user.otp != otp:
            raise ValidationError({'message': 'Invalid email or OTP.'})

        return data
    
class SetNewPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        email = data.get('email')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        if not (email and new_password and confirm_password):
            raise ValidationError({'message': 'Email, new password, and confirm password are required.'})

        user = User.objects.filter(email=email).first()

        if not user:
            raise ValidationError({'message': 'User not found in the database.'})

        if new_password != confirm_password:
            raise ValidationError({'message': 'New password and confirm password do not match.'})

        return data
    
    def save(self):
        print("Save")
        user = User.objects.get(email=self.validated_data['email'])
        user.set_password(self.validated_data['new_password'])
        user.save()
        print("Save1")

####################################################################################################################
