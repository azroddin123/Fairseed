from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(CampaignCatagory)
admin.site.register(Campaign)
admin.site.register(BenificiaryBankDetails)
admin.site.register(KycDetails)

