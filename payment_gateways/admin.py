from django.contrib import admin
from .models import * 

# Register your models here.

class PGAdmin(admin.ModelAdmin):
    list_display = ('currency_code','currency_symbol','fee_for_donation','currency_position','decimal_format')


class PayPalAdmin(admin.ModelAdmin):
    list_display = ('percentage_fee','fee_cents','paypal_account','paypal_sandbox','status')

class StripeAdmin(admin.ModelAdmin):
    list_display = ('fee_percent','fee_cents','stripe_public_key','stripe_secret_key','status')

class BTAdmin(admin.ModelAdmin):
    list_display = ('fee_percent','bank_details','status')


class RazorPayAdmin(admin.ModelAdmin):
    list_display = ('razorpay_key','razorpay_secret','status','fee_percent','fee_cents')

class PhonePayAdmin(admin.ModelAdmin):
    list_display = ('phonepay_key','phonepay_secret','fee_percent','fee_cents','status')

class QRAdmin(admin.ModelAdmin):
    list_display = ('fee_percent','qr_path','status')


admin.site.register(PGSetting,PGAdmin)
admin.site.register(PayPal,PayPalAdmin)
admin.site.register(Stripe,StripeAdmin)
admin.site.register(BankTransfer,BTAdmin)
admin.site.register(RazorPay,RazorPayAdmin)
admin.site.register(PhonePay,PhonePayAdmin)
admin.site.register(QRTransfer,QRAdmin)