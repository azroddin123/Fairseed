from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ValidationError
from .models import User,UserRole
from rest_framework import serializers
from django.db import models

from campaigns.models import Campaign


from django.contrib.auth.hashers import make_password


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
        user = self.context['request'].user
        if not user.check_password(old_password):
            raise serializers.ValidationError("Old password is incorrect.")
        return old_password
    
    def save(self):
        if (
            self.validated_data["old_password"]
            and self.validated_data["new_password"]
            and self.validated_data["confirm_password"]
        ):
            user = self.context['request'].user
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

################################### MY CODE ################################################
    

class UserOTPSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'is_verified', 'password']
        
    def save(self, **kwargs):
        self.validated_data['password'] = make_password(self.validated_data.get('password'))
        return super().save(**kwargs)

class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()




class ChangePasswordSerializer1(serializers.Serializer):
    email = serializers.EmailField(required=True)
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)
    model = User

    def validate(self, data):
        email = data.get('email', '')
        old_password = data.get('old_password', '')
        new_password = data.get('new_password', '')
        confirm_password = data.get('confirm_password', '')

        if not email or not old_password or not new_password or not confirm_password:
            raise serializers.ValidationError("All fields must be provided.")

        if new_password != confirm_password:
            raise serializers.ValidationError("New password and confirm password must match.")

        user = User.objects.filter(email=email).first()

        if not user or not user.check_password(old_password):
            raise serializers.ValidationError("Invalid email or old password.")
        data['user'] = user  
        return data

    def save(self):
        user = self.validated_data['user']
        if user:
            user.set_password(self.validated_data['new_password'])
            user.save()
        return user

class ChangePasswordSerializer2(serializers.Serializer):
    email = serializers.EmailField(required=True)
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)
    model = User

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})




class UserSerializer_AdminPanel(serializers.ModelSerializer):
    campaigns_created_count = serializers.SerializerMethodField()
    registered_as = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'mobile_number', 'campaigns_created_count', 'user_type', 'registered_as']

    def get_campaigns_created_count(self, user):
        return Campaign.objects.filter(user=user).count()

    def get_registered_as(self, user):
        return user.created_on.strftime('%b %d, %Y') if user.created_on else None
    
class AddUserSerializer_AdminPanel(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'mobile_number', 'user_role', 'password', 'confirm_password', 'user_type']

    def validate(self, data):
        #Validate that the passwords match
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        #Create a new user with the validated data
        confirm_password = validated_data.pop('confirm_password')
        validated_data.pop('password', None)
        user = User(**validated_data)
        user.set_password(confirm_password)
        user.save()
        return user

class EditUserSerializer_AdminPanel(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, required=False, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'user_role', 'password', 'confirm_password']

    def validate(self, data):
        
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if password and password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        validated_data.pop('confirm_password', None)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
    
class UserCardSerializer_AdminPanel(serializers.ModelSerializer):
    campaigns_created_count = serializers.SerializerMethodField()
    registered_as = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['registered_as', 'country', 'campaigns_created_count']

    def get_campaigns_created_count(self, user):
        return Campaign.objects.filter(user=user).count()
    
    def get_registered_as(self, user):
        return user.created_on.strftime('%b %d, %Y') if user.created_on else None