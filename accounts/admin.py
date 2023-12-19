from django.contrib import admin

# Register your models here.
from .models import User,UserRole


class UserAdmin(admin.ModelAdmin) :
    list_display = ['id','username','email','mobile_number','city','country','user_type','accepted_policy','created_at','updated_at']

class UserRoleAdmin(admin.ModelAdmin) :
    list_display = ['id','role_name']


admin.site.register(User,UserAdmin)
admin.site.register(UserRole,UserRoleAdmin)
