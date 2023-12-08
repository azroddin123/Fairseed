from django.db import models

class PGSetting(models.Model):
    currency_code     = models.CharField(max_length=50)
    currency_symobl   = models.CharField(max_length=10)
    fee_for_donaion   = models.IntegerField()
    cuurency_position = models.CharField(max_length=124)
    decimal_format    = models.DecimalField() 

class BankTransfer(models.Model) :
    bank_details = models.TextField()
    status       = models.BooleanField(default=True)

class PhonePay(models.Model):
    phonepay_key    = models.CharField(max_length=154)
    phonepay_secret = models.CharField(max_length=154)
    fee_percent     = models.IntegerField()
    fee_cents       = models.IntegerField()
    status          = models.BooleanField(default=False)

class RazorPay(models.Model):
    razorpay_key    = models.BooleanField(max_length=154)
    razorpay_secret = models.BooleanField(max_length=154)
    status          = models.BooleanField(default=False)
    fee_percent     = models.IntegerField()
    fee_cents       = models.IntegerField()





    
