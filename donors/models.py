from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from campaigns.models import Campaign

# Create your models here.


payment_type = [
    ("bank_transfer" ,"bank_transfer"),
    ("upi/credit_card/" ,"upi")
]

class Donor(models.Model):
    campaign      = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    donation_type = models.CharField(max_length=124)
from campaigns.models import Campaign
from django.core.validators import MinValueValidator, MaxValueValidator
from portals.models import BaseModel
from portals.choices import DonationChoices,PaymentChoices
# Create your models here.

class Donor(BaseModel):
    campaign      = models.ForeignKey(Campaign,on_delete=models.CASCADE,related_name="donors")
    donation_type = models.CharField(choices=DonationChoices.choices,max_length=124)
    full_name     = models.CharField(max_length=124)
    amount        = models.PositiveIntegerField(validators=[MinValueValidator(50, message="Value must be greater than or equal to 50"),
                    MaxValueValidator(100000, message="Value must be less than or equal to 100")])
    email         = models.CharField(max_length=124)
    city          = models.CharField(max_length=124)
    country       = models.CharField(max_length=124)
    mobile        = models.CharField(max_length=124)
    pancard       = models.CharField(max_length=124,blank=True,null=True)
    comment       = models.TextField()
    payment_type  = models.CharField(choices=PaymentChoices.choices,max_length=124)
    is_anonymous  = models.BooleanField(default=False)
    status        = models.BooleanField(default=True)
    is_approved   = models.BooleanField(default=False)


    def __str__(self):
        return self.full_name
    
class BankTransfer(models.Model):
    donor            = models.ForeignKey(Donor,on_delete=models.CASCADE)
class BankTransaction(BaseModel):
    donor            = models.ForeignKey(Donor,on_delete=models.CASCADE,related_name="bank_transaction")
    transaction_id   = models.CharField(max_length=124)
    bank_name        = models.CharField(max_length=124)
    transaction_date = models.DateField()
    other_details    = models.CharField(max_length=124,blank=True,null=True)

class UpiTransaction(BaseModel):
    donor            = models.ForeignKey(Donor,on_delete=models.CASCADE,related_name="upi_transaction") 
    payment_id       = models.CharField(max_length=100),
    order_id         = models.CharField(max_length=100),
    signature        = models.CharField(max_length=200)
    datetime         = models.DateTimeField(auto_now_add=True)


