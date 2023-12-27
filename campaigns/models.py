from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User
# Create your models here.
from portals.models import BaseModel
from portals.choices import RaiseChoices,ZakatChoices,CampaignChoices



class Campaigncategory(BaseModel):
    name   = models.CharField(max_length=50)
    image  = models.ImageField(upload_to="static/media_files/",blank=True,null=True,)
    status = models.BooleanField(default=False)

class Campaign(BaseModel):
    category        = models.ForeignKey(Campaigncategory,on_delete=models.CASCADE,)
    user            = models.ForeignKey(User,on_delete=models.CASCADE)
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
    description     = models.TextField()
    summary         = models.TextField()
   
    is_successfull  = models.BooleanField(default=False)
    is_featured    = models.BooleanField(default=False)
    is_reported     = models.BooleanField(default=False)

# want to combine these two models 
class CampaignKycBenificiary(BaseModel):
    campaign            = models.OneToOneField(Campaign,on_delete=models.CASCADE,related_name='bank_details')
    account_holder_name = models.CharField(max_length=124)
    account_number      = models.PositiveIntegerField()
    bank_name           = models.CharField(max_length=124)
    branch_name         = models.CharField(max_length=124)
    ifsc_code           = models.CharField(max_length=124)
    passbook_image      = models.ImageField(upload_to="static/media_files/",blank=True,null=True,)
    
    pan_card            = models.CharField(max_length=10)
    pan_card_image      = models.ImageField(upload_to="static/media_files/",blank=True,null=True,)
    adhar_card          = models.CharField(max_length=16)
    adhar_card_image    = models.ImageField(upload_to="static/media_files/",blank=True,null=True,)
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

class Documents(BaseModel):
    campaign = models.ForeignKey(Campaign,on_delete=models.CASCADE,related_name="documents")
    doc_name = models.CharField(max_length=124)
    doc_file     = models.FileField(upload_to="static/media_files/",blank=True,null=True)




