from django.db import models
# from campaigns.models import Campaign
from portals.models import BaseModel
from portals.choices import DonationChoices,PaymentChoices,StatusChoices


# Create your models here.
class Donor(BaseModel):
    campaign         = models.ForeignKey("campaigns.Campaign",on_delete=models.CASCADE,related_name="donors")
    user             = models.ForeignKey("accounts.User",on_delete=models.CASCADE,null=True,blank=True)
    donation_type    = models.CharField(choices=DonationChoices.choices,max_length=124)
    full_name        = models.CharField(max_length=124,blank=True,null=True)
    amount           = models.DecimalField(max_digits=10, decimal_places=2)
    email            = models.CharField(max_length=124,blank=True,null=True)
    city             = models.CharField(max_length=124,blank=True,null=True)
    country          = models.CharField(max_length=124,blank=True,null=True)
    mobile           = models.CharField(max_length=124,blank=True,null=True)
    pancard          = models.CharField(max_length=124,blank=True,null=True)
    comment          = models.TextField(blank=True,null=True)
    payment_type     = models.CharField(choices=PaymentChoices.choices,max_length=124)
    is_anonymous     = models.BooleanField(default=False)
    status           = models.CharField(max_length=124,choices=StatusChoices.choices,default=StatusChoices.PENDING)
    is_approved      = models.BooleanField(default=False)
    transaction_id   = models.CharField(max_length=256,blank=True,null=True)
    bank_name        = models.CharField(max_length=124,blank=True,null=True)
    transaction_date = models.DateField(blank=True,null=True)
    other_details    = models.CharField(max_length=124,blank=True,null=True)

class Withdrawal(BaseModel):
    campaign          = models.ForeignKey("campaigns.Campaign",on_delete=models.CASCADE)
    make_withdrawal   = models.CharField(max_length=124,blank=True,null=True)
    withdrawal_status = models.CharField(max_length=124,blank=True,null=True)

    
