from django.contrib import admin
from .models import * 

# Register your models here.

class PGAdmin(admin.ModelAdmin):
    list_display = ('currency_code','currency_symbol','fee_for_donation','currency_position','decimal_format')


class BTAdmin(admin.ModelAdmin):
    list_display = ('fee_percent','bank_details','is_enabled')

class PhonePayAdmin(admin.ModelAdmin):
    list_display = ('phonepay_key','phonepay_secret','fee_percent','fee_cents','is_enabled')




admin.site.register(PGSetting,PGAdmin)
admin.site.register(BankTransfer,BTAdmin)
admin.site.register(PhonePay,PhonePayAdmin)
