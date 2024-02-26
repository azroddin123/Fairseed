from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ValidationError
from portals.choices import UserChoices,RoleChoices
from .models import User,UserRole
from rest_framework import serializers
from django.db import models


class UserSerializer(ModelSerializer):
    class Meta :
        model  = User
        fields = "__all__"
        
    def save(self):
        user = User(**self.validated_data)
        password = self.validated_data["password"]
        user.set_password(password)
        role_name = UserRole.objects.get(role_name="Normal")
        user.user_role = role_name
        if self.validated_data.get("user_role") == "Admin" :
            user.is_admin = True
        user.save()
        return user
    
class UserSerializer1(ModelSerializer):
    user_role = serializers.SerializerMethodField(read_only=True)
    class Meta :
        model = User
        exclude = ("last_login","created_on","updated_on","is_admin","password")

    def get_user_role (self,obj):
        return obj.user_role.role_name if obj.user_role else None
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    model = User

    def validate(self, value):
        if (self.initial_data["old_password"] and self.initial_data["new_password"]) :
            return value
        raise ValidationError(
            {
                "old_password": "This field may not be null.",
                "new_password": "This field may not be null.",
            }
        )

    def validate_old_password(self, old_password):
        print("in validate password")
        try : 
            user = self.context['request'].thisUser
        except : 
            raise serializers.ValidationError( "User Not Found")
        if not user.check_password(old_password):
            raise serializers.ValidationError("Old password is incorrect.")
        return old_password
    
    def save(self):
        if (
            self.validated_data["old_password"]
            and self.validated_data["new_password"]
        ):
            user = self.context['request'].thisUser
            user.set_password(self.validated_data["new_password"])
            user.save()
        return user

class UserAdminSerializer(ModelSerializer):
    class Meta :
        model = User
        fields = ('username','email','mobile_number','profile_pic',)

class UserRoleSerializer(ModelSerializer):
    class Meta :
        model = UserRole 
        fields = "__all__"