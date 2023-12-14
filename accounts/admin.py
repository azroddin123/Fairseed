from django.contrib import admin

# Register your models here.
from .models import User,UserRole

admin.site.register(UserRole)
admin.site.register(User)