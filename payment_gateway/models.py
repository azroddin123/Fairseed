from django.db import models

class PGSetting(models.Model):
    currency_code     = models.CharField(max_length=50)
    currency_symobl   = models.CharField(max_length=10)
    fee_for_donaion   = models.IntegerField()
    cuurency_position = models.CharField(max_length=124)
    decimal_format    = models.DecimalField(max_digits=5,decimal_places=2) 

class PayPal(models.Model):
    percentage_fee   = models.CharField(max_length=124)
    fee_cents        = models.CharField(max_length=124)
    paypal_account   = models.CharField(max_length=124)
    paypal_sandbox   = models.BooleanField(default=False)
    status           = models.BooleanField(default=False)

class Stripe(models.Model):
    fee_percent       = models.IntegerField()
    fee_cents         = models.IntegerField()
    stripe_public_key = models.CharField(max_length=124)
    stripe_secret_key = models.CharField(max_length=124)
    status            = models.BooleanField(default=False)

class BankTransfer(models.Model) :
    fee_percent  = models.IntegerField()
    bank_details = models.TextField()
    status       = models.BooleanField(default=True)


class RazorPay(models.Model):
    razorpay_key    = models.BooleanField(max_length=154)
    razorpay_secret = models.BooleanField(max_length=154)
    status          = models.BooleanField(default=False)
    fee_percent     = models.IntegerField()
    fee_cents       = models.IntegerField()


class PhonePay(models.Model):
    phonepay_key    = models.CharField(max_length=154)
    phonepay_secret = models.CharField(max_length=154)
    fee_percent     = models.IntegerField()
    fee_cents       = models.IntegerField()
    status          = models.BooleanField(default=False)


class QRTransfer(models.Model):
    fee_percent     = models.IntegerField()
    QR_Path         = models.ImageField(upload_to="static/media_files/",blank=True,null=True)
    status          = models.BooleanField(default=False)

