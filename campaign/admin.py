from django.contrib import admin
from .models import Campaign, CampaignCatagories

# Register your models here.

admin.site.register(Campaign)
admin.site.register(CampaignCatagories)
