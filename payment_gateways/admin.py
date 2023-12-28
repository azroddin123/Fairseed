from django.contrib import admin
from .models import * 

# Register your models here.

class PGAdmin(admin.ModelAdmin):
    list_display = ('currency_code','currency_symbol','fee_for_donation','currency_position','decimal_format')


class PayPalAdmin(admin.ModelAdmin):
    list_display = ('percentage_fee','fee_cents','paypal_account','paypal_sandbox','is_enabled')

class StripeAdmin(admin.ModelAdmin):
    list_display = ('fee_percent','fee_cents','stripe_public_key','stripe_secret_key','is_enabled')

class BTAdmin(admin.ModelAdmin):
    list_display = ('fee_percent','bank_details','is_enabled')


class RazorPayAdmin(admin.ModelAdmin):
    list_display = ('razorpay_key','razorpay_secret','is_enabled','fee_percent','fee_cents')

class PhonePayAdmin(admin.ModelAdmin):
    list_display = ('phonepay_key','phonepay_secret','fee_percent','fee_cents','is_enabled')

class QRAdmin(admin.ModelAdmin):
    list_display = ('fee_percent','qr_path','is_enabled')


admin.site.register(PGSetting,PGAdmin)
admin.site.register(PayPal,PayPalAdmin)
admin.site.register(Stripe,StripeAdmin)
admin.site.register(BankTransfer,BTAdmin)
admin.site.register(RazorPay,RazorPayAdmin)
admin.site.register(PhonePay,PhonePayAdmin)
admin.site.register(QRTransfer,QRAdmin)