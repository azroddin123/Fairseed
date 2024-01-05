from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from portals.models import BaseModel

# from portals.singleton import SingletonModel,SingletonModelManager,ConcreteSingletonModel
class GeneralSetting(BaseModel):
    namesite                    = models.CharField(max_length=32)
    welcome_text                = models.CharField(max_length=32)
    welcome_subtitle            = models.CharField(max_length=32)
    Keyword                     = models.TextField(null=True,blank=True)
    description                 = models.CharField(max_length=124)
    email_admin                 = models.EmailField(max_length=254)
    tandc_url                   = models.CharField(max_length=254)
    privacy_policy_url          = models.CharField(max_length=254)
    email_no_reply              = models.CharField(max_length=124)

    new_registration_enabled    = models.BooleanField(default=True)
    auto_approve_enabled        = models.BooleanField(default=False)
    email_verification_enabled  = models.BooleanField(default=False)
    facebook_login_enabled      = models.BooleanField(default=False)
    google_login_enabled        = models.BooleanField(default=False)
    captcha_enabled             = models.BooleanField(default=False)
    input_field_enabled         = models.BooleanField(default=False)
    
    def save(self,*args, **kwargs):
        # check the record count if it is one then update the existing one otherwise save the record 
        count = GeneralSetting.objects.count()
        print(count)
        if count == 0  :
            return super(GeneralSetting,self).save(*args, **kwargs)
        else :
            obj = GeneralSetting.objects.all()
            obj.delete()
            return super(GeneralSetting,self).save(*args, **kwargs)

class Keyword(BaseModel):
    gs   = models.ForeignKey(GeneralSetting,on_delete=models.CASCADE,blank=True,null=True)
    name = models.CharField(max_length=50,unique=True)
    
class Limit(BaseModel):
    num_campaigns           = models.PositiveIntegerField()
    max_file_size           = models.PositiveIntegerField()
    campaign_min_amount     = models.PositiveIntegerField()
    donation_min_amount     = models.PositiveIntegerField()
    donation_max_amount     = models.PositiveIntegerField()
    campaign_max_amount     = models.PositiveIntegerField()
    max_donation_amount     = models.PositiveIntegerField()
    
    
    def save(self,*args, **kwargs):
        # check the record count if it is one then update the existing one otherwise save the record 
        count = Limit.objects.count()
        print(count)
        if count == 0  :
            return super(Limit,self).save(*args, **kwargs)
        else :
            obj = Limit.objects.all()
            obj.delete()
            return super(Limit,self).save(*args, **kwargs)

class SocialProfile(BaseModel):
    # Shall I related it to the the admin model
    facebook_url  = models.CharField(max_length=124)
    twitter_url   = models.CharField(max_length=124)
    instagram_url = models.CharField(max_length=124)

    def save(self,*args, **kwargs):
        # check the record count if it is one then update the existing one otherwise save the record 
        count = SocialProfile.objects.count()
        print(count)
        if count == 0  :
            return super(SocialProfile,self).save(*args, **kwargs)
        else :
            obj = SocialProfile.objects.all()
            obj.delete()
            return super(SocialProfile,self).save(*args, **kwargs)
  
class LandingPage(BaseModel):
    logo              = models.ImageField(upload_to="static/media_files/",blank=True,null=True,)
    logo_footer       = models.ImageField(upload_to="static/media_files/",blank=True,null=True,)
    favicon           = models.ImageField(upload_to="static/media_files/",blank=True,null=True,)
    image_header      = models.ImageField(upload_to="static/media_files/",blank=True,null=True,)
    image_bottom      = models.ImageField(upload_to="static/media_files/",blank=True,null=True,)
    avtar             = models.ImageField(upload_to="static/media_files/",blank=True,null=True,)
    image_category    = models.ImageField(upload_to="static/media_files/",blank=True,null=True,)
    default_link_color= models.CharField(max_length=45)

class Pages(BaseModel):
    title       = models.CharField(max_length=50)
    slug        = models.CharField(max_length=124)
    show_navbar = models.BooleanField(default=False)
    show_footer = models.BooleanField(default=True)
    show_page   = models.BooleanField(default=True)
    content     = models.TextField()

