from django.contrib import admin

# Register your models here.
from .models import *

class CCAdmin(admin.ModelAdmin):
    list_display = ('name','image','is_active')

class CampaignAdmin(admin.ModelAdmin):
    list_display = ('category','user','rasing_for','title','goal_amount','fund_raised','location','zakat_eligible','status','start_date','end_date','description','summary','is_successful','is_featured','is_reported')

class BBAdmin(admin.ModelAdmin):
    list_display = ('campaign','account_holder_name','account_number','bank_name','branch_name','ifsc_code','passbook_image')

# class KycAdmin(admin.ModelAdmin):
#     list_display = ('campaign','pan_card','pan_card_image','adhar_card','adhar_card_image','other_details','is_verified')

admin.site.register(Campaigncategory,CCAdmin)
admin.site.register(Campaign,CampaignAdmin)
admin.site.register(CampaignKycBenificiary,BBAdmin)
admin.site.register(CampaignModification)
# admin.site.register(KycDetails,KycAdmin)

