from django.db import models
from portals.models import BaseModel

class PGSetting(BaseModel):
    currency_code     = models.CharField(max_length=50)
    currency_symbol   = models.CharField(max_length=10)
    fee_for_donation   = models.IntegerField()
    currency_position = models.CharField(max_length=124)
    # What will be the decimal format of the number 
    decimal_format    = models.CharField(max_length=124) 


class BankTransfer(BaseModel) :
    fee_percent  = models.IntegerField()
    bank_details = models.TextField()
    is_enabled       = models.BooleanField(default=True)

class PhonePay(BaseModel):
    phonepay_key    = models.CharField(max_length=154)
    phonepay_secret = models.CharField(max_length=154)
    fee_percent     = models.IntegerField()
    fee_cents       = models.IntegerField()
    is_enabled          = models.BooleanField(default=False)


