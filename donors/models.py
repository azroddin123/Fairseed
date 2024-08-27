from django.db import models
# from campaigns.models import Campaign
from portals.models import BaseModel
from portals.choices import DonationChoices,PaymentChoices,StatusChoices,WithdrawalChoices
from fairseed.task import send_email_fun
from fairseed.settings import EMAIL_HOST_USER
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.serializers import ValidationError

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
    date             = models.DateField(auto_now_add=True,null=True,blank=True)


@receiver(post_save, sender=Donor,weak=False)
def update_campaign(sender, instance,created, **kwargs):
    print("",created)
    print("post_save signal triggered")
    if kwargs.get('created', False):
        print("New donor created, skipping...")
        return
    
    if instance.pk:
        print("pk==================>", instance.pk)
        try:
            original_instance = Donor.objects.get(pk=instance.pk)
            print("Original status:", original_instance.status)
            print("New status:", instance.status)
            if instance.status == "Approved":
                campaign = instance.campaign
                required_amount = campaign.goal_amount - campaign.fund_raised
                print("Required amount:", required_amount)
                print("amount",instance.amount)
                if instance.amount > required_amount:
                    print(f"Donation amount {instance.amount} exceeds required amount.")
                    raise ValidationError({
                        "error": True,
                        "message": f"You can make a donation for this campaign up to {required_amount} Rs only."
                    })

                campaign.fund_raised += instance.amount
                campaign.save()
                print("Campaign updated successfully.")
        except Donor.DoesNotExist:
            print("Donor instance does not exist.")
        
# @receiver(post_save, sender=Donor)
# def send_email_on_model_creation_or_update(sender, instance, created, **kwargs):
#     if created:
#         subject = "Fairseed Donation Email"
#         message = f"Your Donation For Campaign  '{instance.campaign.title}' of '{instance.amount} has been done successfully."
#         send_email_fun.delay(subject, message, EMAIL_HOST_USER, instance.user.email)

class Withdrawal(BaseModel):
    campaign          = models.OneToOneField("campaigns.Campaign",on_delete=models.CASCADE)
    withdrawal_status = models.CharField(max_length=124,choices=WithdrawalChoices.choices,default=WithdrawalChoices.PENDING)
    transfer_details  = models.TextField(blank=True,null=True)
# username fund_Raised ,goal_amount,beniiciary name.