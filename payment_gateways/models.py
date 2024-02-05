from django.db import models
from portals.models import BaseModel

class PGSetting(BaseModel):
    VALID_FEE_FOR_DONATION_OPTIONS  = [('0%', '0%'), ('1%', '1%'), ('2%', '2%'), ('3%', '3%'), ('4%', '4%'), ('5%', '5%'), ('6%', '6%'), ('7%', '7%'), ('8%', '8%'), ('9%', '9%'), ('10%', '10%'),('15%', '15%')]
    VALID_CURRENCY_POSITION_OPTIONS = [('₹99 - left', '₹99 - left'), ('99₹ - right', '99₹ - right')]
    VALID_DCIMAL_FORMAT_OPTIONS     = [('10,989.95','10,989.95'), ('10.989,95', '10.989,95')]

    currency_code     = models.CharField(max_length=50)
    currency_symbol   = models.CharField(max_length=10)
    fee_for_donation   = models.CharField(max_length=5,choices=VALID_FEE_FOR_DONATION_OPTIONS)
    currency_position = models.CharField(max_length=15,choices=VALID_CURRENCY_POSITION_OPTIONS)
    # What will be the decimal format of the number 
    decimal_format    = models.CharField(max_length=10,choices=VALID_DCIMAL_FORMAT_OPTIONS) 

    def save(self, *args, **kwargs):
        # Check the record count, if it is one then update the existing one, otherwise save the record
        count = PGSetting.objects.count()
        if count == 0:
            return super(PGSetting, self).save(*args, **kwargs)
        else:
            PGSetting.objects.all().delete()
            return super(PGSetting, self).save(*args, **kwargs)

class PayPal(BaseModel):
    percentage_fee   = models.CharField(max_length=124)
    fee_cents        = models.CharField(max_length=124)
    paypal_account   = models.CharField(max_length=124)
    paypal_sandbox   = models.BooleanField(default=False)
    is_enabled       = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        count = PayPal.objects.count()
        if count == 0:
            return super(PayPal, self).save(*args, **kwargs)
        else:
            PayPal.objects.all().delete()
            return super(PayPal, self).save(*args, **kwargs)

class Stripe(BaseModel):
    fee_percent       = models.IntegerField()
    fee_cents         = models.IntegerField()
    stripe_public_key = models.CharField(max_length=124)
    stripe_secret_key = models.CharField(max_length=124)
    is_enabled        = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Check the record count, if it is one then update the existing one, otherwise save the record
        count = Stripe.objects.count()
        if count == 0:
            return super(Stripe, self).save(*args, **kwargs)
        else:
            Stripe.objects.all().delete()
            return super(Stripe, self).save(*args, **kwargs)

class BankTransfer(BaseModel) :
    fee_percent  = models.IntegerField()
    bank_details = models.TextField()
    is_enabled   = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Check the record count, if it is one then update the existing one, otherwise save the record
        count = BankTransfer.objects.count()
        if count == 0:
            return super(BankTransfer, self).save(*args, **kwargs)
        else:
            BankTransfer.objects.all().delete()
            return super(BankTransfer, self).save(*args, **kwargs)

class RazorPay(BaseModel):
    razorpay_key    = models.CharField(max_length=154)
    razorpay_secret = models.CharField(max_length=154)
    is_enabled      = models.BooleanField(default=False)
    fee_percent     = models.IntegerField()
    fee_cents       = models.IntegerField()

    def save(self, *args, **kwargs):
        # Check the record count, if it is one then update the existing one, otherwise save the record
        count = RazorPay.objects.count()
        if count == 0:
            return super(RazorPay, self).save(*args, **kwargs)
        else:
            # Delete all existing RazorPay objects (assuming only one is allowed)
            RazorPay.objects.all().delete()
            return super(RazorPay, self).save(*args, **kwargs)

class PhonePay(BaseModel):
    phonepay_key    = models.CharField(max_length=154)
    phonepay_secret = models.CharField(max_length=154)
    fee_percent     = models.IntegerField()
    fee_cents       = models.IntegerField()
    is_enabled      = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Check the record count, if it is one then update the existing one, otherwise save the record
        count = PhonePay.objects.count()
        if count == 0:
            return super(PhonePay, self).save(*args, **kwargs)
        else:
            # Delete all existing PhonePay objects (assuming only one is allowed)
            PhonePay.objects.all().delete()
            return super(PhonePay, self).save(*args, **kwargs)

class QRTransfer(BaseModel):
    fee_percent     = models.IntegerField()
    qr_path         = models.ImageField(upload_to="static/media_files/",blank=True,null=True)
    is_enabled      = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        count = QRTransfer.objects.count()
        if count == 0:
            return super(QRTransfer, self).save(*args, **kwargs)
        else:
            QRTransfer.objects.all().delete()
            return super(QRTransfer, self).save(*args, **kwargs)

