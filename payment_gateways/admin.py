from django.contrib import admin
from .models import * 

# Register your models here.

admin.site.register(PGSetting)
admin.site.register(PayPal)
admin.site.register(Stripe)
admin.site.register(BankTransfer)
admin.site.register(RazorPay)
admin.site.register(PhonePay)
admin.site.register(QRTransfer)