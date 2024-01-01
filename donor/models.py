from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from campaign.models import Campaign

# Create your models here.


payment_type = [
    ("bank_transfer" ,"bank_transfer"),
    ("upi/credit_card/" ,"upi")
]

class Donor(models.Model):
    campaign      = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    donation_type = models.CharField(max_length=124)
    full_name     = models.CharField(max_length=124)
    amount        = models.PositiveIntegerField(validators=[MinValueValidator(50, message="Value must be greater than or equal to 50"),
                    MaxValueValidator(100000, message="Value must be less than or equal to 100")])
    email         = models.CharField(max_length=124)
    city          = models.CharField(max_length=124)
    country       = models.CharField(max_length=124)
    mobile        = models.CharField(max_length=124)
    pancard       = models.CharField(max_length=124)
    comment       = models.TextField()
    payment_type  = models.CharField(max_length=124)
    is_anonymous  = models.CharField(max_length=124)
    status        = models.BooleanField(default=True)


    def __str__(self):
        return self.full_name
    
class BankTransfer(models.Model):
    donor            = models.ForeignKey(Donor,on_delete=models.CASCADE)
    transaction_id   = models.CharField(max_length=124)
    bank_name        = models.CharField(max_length=124)
    transaction_date = models.DateField()
    other_details    = models.TextField()


class UpiTransaction(models.Model):
    donor            = models.ForeignKey(Donor,on_delete=models.CASCADE) 
    payment_id       = models.CharField(max_length=100),
    order_id         = models.CharField(max_length=100),
    signature        = models.CharField(max_length=200)
    datetime         = models.DateTimeField(auto_now_add=True)


