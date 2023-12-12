from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User
# Create your models here.


class CampaignCatagories(models.Model):
    name   = models.CharField(max_length=50)
    status = models.BooleanField(default=False)


ZAKAT_CHOICES = [
    ('yes', 'yes'),
    ('no', 'no'),
]

RAISE_CHOICES = [
    ('self','self'),
    ('others','others')
]

class Campaign(models.Model):
    catagory        = models.ForeignKey(CampaignCatagories,on_delete=models.CASCADE)
    user            = models.ForeignKey(User,on_delete=models.CASCADE)
    rasing_for      = models.CharField(choices=RAISE_CHOICES,max_length=124)
    title           = models.CharField(max_length=50)
    goal_amount     = models.PositiveIntegerField(validators=[MinValueValidator(100, message="Value must be greater than or equal to 0"),
                    MaxValueValidator(1000, message="Value must be less than or equal to 100")])
    fund_raised     = models.PositiveIntegerField(default=0,validators=[MinValueValidator(100, message="Value must be greater than or equal to 0"),
                    MaxValueValidator(10000, message="Value must be less than or equal to 100")])
    location        = models.CharField(max_length=124)
    zakat_eligible  = models.CharField(choices=ZAKAT_CHOICES,max_length=124)
    description     = models.TextField()
    summary         = models.TextField()

    is_successfull  = models.BooleanField(default=False)
    status          = models.BooleanField(default=False)
    is_featured    = models.BooleanField(default=False)
    is_reported     = models.BooleanField(default=False)
    
    is_scholarship  = models.BooleanField(default=False)
    course          = models.CharField(max_length=50,blank=True,null=True)


class BenificiaryBankDetails(models.Model):
    campaign            = models.OneToOneField(Campaign,on_delete=models.CASCADE)
    account_holder_name = models.CharField(max_length=124)
    account_number      = models.PositiveIntegerField()
    bank_name           = models.CharField(max_length=124)
    branch_name         = models.CharField(max_length=124)
    ifsc_code           = models.CharField(max_length=124)
    passbook_image      = models.ImageField(upload_to="static/media_files/",blank=True,null=True,)
   
   
class KycDetails(models.Model):
    campaign           = models.OneToOneField(Campaign,on_delete=models.CASCADE)
    pan_card           = models.CharField(max_length=10)
    pan_card_img       = models.ImageField(upload_to="static/media_files/",blank=True,null=True,)
    adhar_card         = models.CharField(max_length=16)
    adhar_card_image   = models.ImageField(upload_to="static/media_files/",blank=True,null=True,)
    other_details      = models.CharField(max_length=100,blank=True,null=True)
    is_verified        = models.BooleanField(default=False)









