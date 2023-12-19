from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager
from portals.choices import UserChoices,RoleChoices
from portals.models import BaseModel
import uuid
# Create your models here.
class UserRole(BaseModel):
    role_name  = models.CharField(choices=RoleChoices.choices,max_length=25,unique=True)


class User(AbstractBaseUser):
    id         = models.UUIDField(default=uuid.uuid4,primary_key=True)
    email      = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_admin         = models.BooleanField(default=False)
    username         = models.CharField(max_length = 50)
    mobile_number    = models.CharField(max_length=20,unique=True)
    city             = models.CharField(max_length = 50 ,blank=True, null=True)
    country          = models.CharField(max_length=50, blank=True, null=True)
    user_type        = models.CharField(choices=UserChoices.choices,max_length=25)
    accepted_policy  = models.BooleanField(default=False)

    created_at       = models.DateTimeField(auto_now_add=True,editable=False)
    updated_at       = models.DateTimeField(auto_now=True)

    user_role        = models.ForeignKey(UserRole,on_delete=models.CASCADE,null=True,blank=True)
    
    objects    = UserManager()
    
    USERNAME_FIELD = 'email'
    
    def __str__(self):
        return self.email
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin



