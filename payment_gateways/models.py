from django.db import models
from portals.models import BaseModel

class PGSetting(BaseModel):
    currency_code     = models.CharField(max_length=50)
    currency_symbol   = models.CharField(max_length=10)
    fee_for_donation   = models.IntegerField()
    currency_position = models.CharField(max_length=124)
    # What will be the decimal format of the number 
    decimal_format    = models.CharField(max_length=124) 

class PayPal(BaseModel):
    percentage_fee   = models.CharField(max_length=124)
    fee_cents        = models.CharField(max_length=124)
    paypal_account   = models.CharField(max_length=124)
    paypal_sandbox   = models.BooleanField(default=False)
    is_enabled       = models.BooleanField(default=False)

class Stripe(BaseModel):
    fee_percent       = models.IntegerField()
    fee_cents         = models.IntegerField()
    stripe_public_key = models.CharField(max_length=124)
    stripe_secret_key = models.CharField(max_length=124)
    is_enabled        = models.BooleanField(default=False)

class BankTransfer(BaseModel) :
    fee_percent  = models.IntegerField()
    bank_details = models.TextField()
    is_enabled   = models.BooleanField(default=True)


class RazorPay(BaseModel):
    razorpay_key    = models.CharField(max_length=154)
    razorpay_secret = models.CharField(max_length=154)
    is_enabled          = models.BooleanField(default=False)
    fee_percent     = models.IntegerField()
    fee_cents       = models.IntegerField()


class PhonePay(BaseModel):
    phonepay_key    = models.CharField(max_length=154)
    phonepay_secret = models.CharField(max_length=154)
    fee_percent     = models.IntegerField()
    fee_cents       = models.IntegerField()
    is_enabled      = models.BooleanField(default=False)


class QRTransfer(BaseModel):
    fee_percent     = models.IntegerField()
    qr_path         = models.ImageField(upload_to="static/media_files/",blank=True,null=True)
    is_enabled      = models.BooleanField(default=False)

