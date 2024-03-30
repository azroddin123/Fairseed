from django.contrib import admin

# Register your models here.
from .models import *

class CCAdmin(admin.ModelAdmin):
    list_display = ('name','image','is_active','id')

admin.site.register(Campaign)
admin.site.register(Campaigncategory,CCAdmin)
admin.site.register(Documents)
admin.site.register(BankKYC)
admin.site.register(RevisionHistory)
admin.site.register(CauseEdit)
admin.site.register(BankKYCEdit)
admin.site.register(ReportedCampaign)


