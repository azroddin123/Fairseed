from django.contrib import admin
from .models import * 

# Register your models here.

class DonorAdmin(admin.ModelAdmin):
    list_display = ['campaign','donation_type','full_name','amount','email','city','country','mobile','pancard','comment','payment_type','is_anonymous','status','created_on','updated_on']


admin.site.register(Donor,DonorAdmin)
admin.site.register(Withdrawal)

