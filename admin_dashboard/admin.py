from django.contrib import admin

# Register your models here.
from .models import * 

admin.site.register(GeneralSetting)
admin.site.register(Keyword)
admin.site.register(Limit)
admin.site.register(SocialProfile)
admin.site.register(LandingPage)
admin.site.register(Pages)
