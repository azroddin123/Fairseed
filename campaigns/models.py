from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User
from portals.models import BaseModel
from portals.choices import RaiseChoices,ZakatChoices,CampaignChoices,KycChoices,ApprovalChoices
from django.db.models.signals import post_save
from django.dispatch import receiver
# from django.core.exceptions import ValidationError
from rest_framework.serializers import ValidationError
from donors.models import Donor
from datetime import datetime, timedelta
import markdown

class Campaigncategory(BaseModel):
    name   = models.CharField(max_length=50)
    slug   = models.CharField(max_length=130,blank=True,null=True,)
    image  = models.ImageField(upload_to="campaign/catagory/",blank=True,null=True,)
    is_active = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return str(self.name)

class Campaign(BaseModel):
    campaign_image    = models.ImageField(upload_to='campaign/campaign_images/',null=True,blank=True)
    title             = models.CharField(max_length=124)
    category          = models.ForeignKey(Campaigncategory,on_delete=models.CASCADE)
    user              = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name="campaigns")
    rasing_for        = models.CharField(choices=RaiseChoices.choices,max_length=124)
    goal_amount       = models.PositiveIntegerField(validators=[MinValueValidator(0, message="Value must be greater than or equal to 100"),
                      MaxValueValidator(1000000000, message="Value must be less than or equal to 1000000")])
    fund_raised       = models.PositiveIntegerField(default=0,validators=[MinValueValidator(0, message="Value must be greater than or equal to 0"),
                        MaxValueValidator(100000, message="Value must be less than or equal to 100000")])
    zakat_eligible    = models.BooleanField(default=False)
    rasing_for        = models.CharField(choices=RaiseChoices.choices,max_length=124)
    location          = models.CharField(max_length=124)
    story             = models.TextField(blank=True,null=True)
    summary           = models.TextField(blank=True,null=True)
    status            = models.CharField(max_length=124,choices=CampaignChoices.choices,default=CampaignChoices.PENDING)
    end_date          = models.DateField()
    days_left         = models.IntegerField(default=0)
    is_successful     = models.BooleanField(default=False)
    is_featured       = models.BooleanField(default=False)
    is_reported       = models.BooleanField(default=False)
    is_withdrawal     = models.BooleanField(default=False)
    approval_status   = models.CharField(max_length=240,choices=ApprovalChoices.choices,default=ApprovalChoices.NO_REQUEST)
    campaign_data     = models.JSONField(null=True,blank=True)
    is_admin_approved = models.BooleanField(default=False)
    notes             = models.TextField(blank=True,null=True)
    def __str__(self) -> str:
        return self.title
   
    def get_rendered_text(self):
        return markdown.markdown(self.story)
    
    @property
    def days_left(self):
        return max(0, (self.end_date - datetime.now().date()).days)
   
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
    


class Documents(BaseModel):
    campaign     = models.ForeignKey(Campaign,on_delete=models.CASCADE,related_name="documents",blank=True,null=True)
    doc_file     = models.FileField(upload_to="campaign/documents/",blank=True,null=True)

class BankKYC(BaseModel):
# Bank Details
    campaign            = models.OneToOneField(Campaign,on_delete=models.CASCADE,related_name='bank_kyc')
    account_holder_name = models.CharField(max_length=124)
    account_number      = models.CharField(max_length=240)
    bank_name           = models.CharField(max_length=124)
    branch_name         = models.CharField(max_length=124)
    ifsc_code           = models.CharField(max_length=124)
    passbook_image      = models.ImageField(upload_to="campaign/kyc/",blank=True,null=True,)
# kyc Details
    pan_card            = models.CharField(max_length=10)
    pan_card_image      = models.ImageField(upload_to="campaign/kyc/",blank=True,null=True,)
    adhar_card          = models.CharField(max_length=16)
    adhar_card_image    = models.ImageField(upload_to="campaign/kyc/",blank=True,null=True,)
    other_details       = models.CharField(max_length=100,blank=True,null=True)
    is_verified         = models.BooleanField(default=False)
    status              = models.CharField(max_length=124,choices=KycChoices.choices,default=CampaignChoices.PENDING)
    tandc_accept        = models.BooleanField(default=False)
    # For Approval Proces 
    bank_data           = models.JSONField(default=dict)
    approval_status     = models.CharField(max_length=240,choices=ApprovalChoices.choices,default=ApprovalChoices.NO_REQUEST)
    

class RevisionHistory(BaseModel):
    modeified_by  = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    campaign      = models.ForeignKey(Campaign,on_delete=models.CASCADE,null=True,blank=True)
    campaign_data = models.JSONField(null=True,blank=True)
    
    
