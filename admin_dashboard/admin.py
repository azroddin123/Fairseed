from django.contrib import admin

# Register your models here.
from .models import * 


class GSAdmin(admin.ModelAdmin):
    list_display = ('namesite','welcome_text','welcome_subtitle','description','email_admin','tandc_url','privacy_policy_url','email_no_reply','new_registration','auto_approve','email_verification','facebook_login','google_login')

class KeywordAdmin(admin.ModelAdmin):
    list_display = ('gs','name')

class LimitAdmin(admin.ModelAdmin):
    list_display = ('num_campaigns','file_size','campaign_min_amount','campaign_max_amount','donation_min_amount','donation_max_amount','max_donation_amount')

class SocialProfileAdmin(admin.ModelAdmin):
    list_display = ('facebook_url','twitter_url','instagram_url')

class LandingPageAdmin(admin.ModelAdmin):
    list_display = ('logo','logo_footer','favicon','image_header','image_bottom','avtar','image_category','default_link_color')

class PageAdmin(admin.ModelAdmin):
    list_display = ('title','slug','show_navbar','show_page','content')


admin.site.register(GeneralSetting,GSAdmin)
admin.site.register(Keyword,KeywordAdmin)
admin.site.register(Limit,LimitAdmin)
admin.site.register(SocialProfile,SocialProfileAdmin)
admin.site.register(LandingPage,LandingPageAdmin)
admin.site.register(Pages,PageAdmin)
