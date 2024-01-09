from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User
from portals.models import BaseModel
from portals.choices import RaiseChoices,ZakatChoices,CampaignChoices
from django.db.models.signals import post_save
from django.dispatch import receiver
# from django.core.exceptions import ValidationError
from rest_framework.serializers import ValidationError
from donors.models import Donor
from datetime import datetime, timedelta


class Campaigncategory(BaseModel):
    name   = models.CharField(max_length=50)
    image  = models.ImageField(upload_to="static/media_files/catagory/",blank=True,null=True,)
    is_active = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return str(self.name)
    

class Campaign(BaseModel):
    category        = models.ForeignKey(Campaigncategory,on_delete=models.CASCADE)
    user            = models.ForeignKey(User,on_delete=models.CASCADE)
    campaign_image  = models.ImageField(upload_to='static/media_files/campaign_images/', null=True, blank=True)
    rasing_for      = models.CharField(choices=RaiseChoices.choices,max_length=124)
    title           = models.CharField(max_length=50)
    goal_amount     = models.PositiveIntegerField(validators=[MinValueValidator(100, message="Value must be greater than or equal to 100"),
                    MaxValueValidator(1000000, message="Value must be less than or equal to 1000000")])
    fund_raised     = models.PositiveIntegerField(default=0,validators=[MinValueValidator(0, message="Value must be greater than or equal to 0"),
                    MaxValueValidator(100000, message="Value must be less than or equal to 100000")])
    location        = models.CharField(max_length=124)
    zakat_eligible  = models.CharField(max_length=124,choices=ZakatChoices.choices,default=ZakatChoices.YES)
    status          = models.CharField(max_length=124,choices=CampaignChoices.choices,default=CampaignChoices.PENDING)
    start_date      = models.DateField(null=True,blank=True)
    end_date        = models.DateField(null=True,blank=True)
    days_left       = models.IntegerField(default=0)
    description     = models.TextField()
    summary         = models.TextField()

    is_successful   = models.BooleanField(default=False)
    is_featured     = models.BooleanField(default=False)
    is_reported     = models.BooleanField(default=False)
    is_withdrawal   = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.title
    
    
    @property
    def update_days_left(self):
        self.days_left = (self.end_date - datetime.now().date()).days
        self.save()
    
    @receiver(post_save,sender=Donor)
    def update_campaign(sender, instance, **kwargs):
            campaign = instance.campaign
            required_amount = campaign.goal_amount - campaign.fund_raised
            if instance.amount > required_amount:
                print(instance.delete(),"instance deleted successfully")
                raise ValidationError({"error": True, "message": f"You can make a donation for this campaign up to {required_amount} Rs Only"})
            campaign.fund_raised += instance.amount
            campaign.save()


    @classmethod
    def get_reported_campaigns(cls):
        return cls.objects.filter(is_reported=True)
   
    @classmethod
    def get_successful_campaign(cls):
        return cls.objects.filter(is_successful=True)

# want to combine these two models 
class CampaignKycBenificiary(BaseModel):
    campaign            = models.OneToOneField(Campaign,on_delete=models.CASCADE,related_name='bank_details')
    account_holder_name = models.CharField(max_length=124)
    account_number      = models.PositiveIntegerField()
    bank_name           = models.CharField(max_length=124)
    branch_name         = models.CharField(max_length=124)
    ifsc_code           = models.CharField(max_length=124)
    passbook_image      = models.ImageField(upload_to="static/media_files/kyc/",blank=True,null=True,)
    
    pan_card            = models.CharField(max_length=10)
    pan_card_image      = models.ImageField(upload_to="static/media_files/kyc/",blank=True,null=True,)
    adhar_card          = models.CharField(max_length=16)
    adhar_card_image    = models.ImageField(upload_to="static/media_files/kyc/",blank=True,null=True,)
    other_details       = models.CharField(max_length=100,blank=True,null=True)
    is_verified         = models.BooleanField(default=False)

# class KycDetails(BaseModel):
#     campaign           = models.OneToOneField(Campaign,on_delete=models.CASCADE,related_name='kyc_details')
#     pan_card           = models.CharField(max_length=10)
#     pan_card_image     = models.ImageField(upload_to="static/media_files/",blank=True,null=True,)
#     adhar_card         = models.CharField(max_length=16)
#     adhar_card_image   = models.ImageField(upload_to="static/media_files/",blank=True,null=True,)
#     other_details      = models.CharField(max_length=100,blank=True,null=True)
#     is_verified        = models.BooleanField(default=False)

# Document fields of Django Admin Panel

class Documents(BaseModel):
    campaign     = models.ForeignKey(Campaign,on_delete=models.CASCADE,related_name="documents")
    doc_name     = models.CharField(max_length=124)
    doc_file     = models.FileField(upload_to="static/media_files/documents/",blank=True,null=True)




