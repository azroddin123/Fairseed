from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User
from portals.models import BaseModel
from portals.choices import RaiseChoices,ZakatChoices,CampaignChoices,KycChoices,ApprovalChoices,WithdrawalChoices
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.serializers import ValidationError
from donors.models import Donor
from datetime import datetime, timedelta
import markdown
from django.conf import settings
from fairseed.task import send_email_fun
from fairseed.settings import EMAIL_HOST_USER


class Campaigncategory(BaseModel):
    name   = models.CharField(max_length=50,unique=True)
    slug   = models.CharField(max_length=130,blank=True,null=True,unique=True)
    image  = models.ImageField(upload_to="campaign/category/",blank=True,null=True,)
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

    notes             = models.TextField(blank=True,null=True)
    def __str__(self) -> str:
        return self.title
   
    def get_rendered_text(self):
        return markdown.markdown(self.story)
    
    @property
    def days_left(self):
        return max(0, (self.end_date - datetime.now().date()).days)
   
    # @receiver(post_save,sender=Donor)
    # def update_campaign(sender, instance, **kwargs):
    #         campaign = instance.campaign
    #         required_amount = campaign.goal_amount - campaign.fund_raised
    #         if instance.amount > required_amount:
    #             raise ValidationError({"error": True, "message": f"You can make a donation for this campaign up to {required_amount} Rs Only"})
    #         campaign.fund_raised += instance.amount
    #         campaign.save()

    @classmethod
    def get_reported_campaigns(cls):
        return cls.objects.filter(is_reported=True)
   
    @classmethod
    def get_successful_campaign(cls):
        return cls.objects.filter(is_successful=True)
    
    def save(self, *args, **kwargs):
        # Check if the goal amount is reached
        if self.fund_raised >= self.goal_amount:
            self.is_successful = True
            self.status="Completed"
        else:
            self.is_successful = False
        # Call the original save method
        super().save(*args, **kwargs)

    # Signal handlers
@receiver(post_save, sender=Campaign)
def send_email_on_model_creation_or_update(sender, instance, created, **kwargs):
    if created:
        subject = "Fairseed Campaign Creation Mail"
        message = f"Your campaign '{instance.title}' has been created, and a request for approval has been sent to the admin."
        send_email_fun.delay(subject, message, EMAIL_HOST_USER, instance.user.email)
        # campaign_creation_updation(instance.user.email,instance.status,instance.title,subject,message)
    else:
        subject = "Fairseed Campaign Updation Mail"
        message = "Your Campaign Data is Updated Now"
        send_email_fun.delay(subject, message, EMAIL_HOST_USER, instance.user.email)
        # campaign_creation_updation(instance.email,instance.status,instance.title,subject,message)

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
    other_details       = models.CharField(max_length=100,blank=True,null=True)
    tandc_accept        = models.BooleanField(default=False)

class CauseEdit(BaseModel):
    campaign           = models.ForeignKey(Campaign,on_delete=models.CASCADE,null=True,blank=True)
    campaign_data      = models.JSONField(default=dict,null=True,blank=True)
    campaign_image     = models.ImageField(upload_to='campaign/campaign_images/',null=True,blank=True)
    doc1               = models.ImageField(upload_to='campaign/docs/',null=True,blank=True)
    doc2               = models.ImageField(upload_to='campaign/docs/',null=True,blank=True)
    doc3               = models.ImageField(upload_to='campaign/docs/',null=True,blank=True)
    approval_status    = models.CharField(max_length=240,choices=ApprovalChoices.choices,default=ApprovalChoices.PENDING)

class BankKYCEdit(BaseModel):
    bank_kyc            = models.ForeignKey(BankKYC,on_delete=models.CASCADE,blank=True,null=True)
    bank_data           = models.JSONField(default=dict)
    pan_card_image      = models.ImageField(upload_to="campaign/kyc/",blank=True,null=True,)
    adhar_card_image    = models.ImageField(upload_to="campaign/kyc/",blank=True,null=True,)
    passbook_image      = models.ImageField(upload_to="campaign/kyc/",blank=True,null=True,)
    approval_status     = models.CharField(max_length=240,choices=ApprovalChoices.choices,default=ApprovalChoices.PENDING)


class RevisionHistory(BaseModel):
    modified_by   = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    campaign      = models.ForeignKey(Campaign,on_delete=models.CASCADE,null=True,blank=True)
    cause_data    = models.ForeignKey(CauseEdit,on_delete=models.CASCADE,null=True,blank=True)


class ReportedCampaign(BaseModel):
    campaign           = models.ForeignKey(Campaign,on_delete=models.CASCADE)
    user               = models.ForeignKey(User,on_delete=models.CASCADE)
    email              = models.EmailField(max_length=245,null=True,blank=True)
    contact_no         = models.CharField(max_length=10,null=True,blank=True)
    message            = models.CharField(max_length=240)
    approval_status    = models.CharField(max_length=240,choices=ApprovalChoices.choices,default=ApprovalChoices.PENDING)

    