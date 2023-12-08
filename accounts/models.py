from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager
# Create your models here.
USER_TYPES = [
    ('as INDIVIDUAL', 'Indiviudal'),
    ('as NGO', 'NGO'),
]

class User(AbstractBaseUser):
    email    = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_admin         = models.BooleanField(default=False)
    username         = models.CharField(max_length = 50 ,blank=True , null=True)
    mobile_number    = models.CharField(max_length=20)
    city             = models.CharField(max_length = 50 ,blank=True , null=True)
    country          = models.CharField(max_length=50, blank=True, null=True)
    user_type        = models.CharField(choices=USER_TYPES,max_length=23)
    privacy_policy   = models.BooleanField(default=False)

    created_at       = models.DateTimeField(auto_now_add=True,editable=False)
    updated_at       = models.DateTimeField(auto_now=True)
    
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


ROLE_CHOICES = [
    (
        "normal" ,"Normal",
        "campaign_approver" , "Campaign_Approver",
        "campaign_manager", "Campaign_Manager"
        "admin","Admin"
    )
]

# class UserRole(models.Model):
#     user       = models.ForeignKey(User,on_delete=models.CASCADE)
#     role_name  = models.CharField(choices=ROLE_CHOICES,max_length=25,default="normal")