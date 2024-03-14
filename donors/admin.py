from django.contrib import admin
from .models import * 

# Register your models here.

class DonorAdmin(admin.ModelAdmin):
    list_display = ['campaign','donation_type','full_name','amount','email','city','country','mobile','pancard','comment','payment_type','is_anonymous','status','created_on','updated_on']


class BTAdmin(admin.ModelAdmin):
    list_display = ['donor','transaction_id','bank_name','transaction_date','other_details']

class UTAdmin(admin.ModelAdmin):
    list_display = ['donor','payment_id','order_id','signature']
    
admin.site.register(Donor,DonorAdmin)
admin.site.register(BankTransaction,BTAdmin)
admin.site.register(UpiTransaction)
