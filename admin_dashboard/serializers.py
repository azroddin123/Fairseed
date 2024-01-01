from .models import * 
from rest_framework.serializers import ModelSerializer 

class GSSerializer(ModelSerializer):
    class Meta :
        model = GeneralSetting
        exclude = ("new_registration","auto_approve","email_verification","facebook_login","google_login")

   
    
    
class KeywordSerializer(ModelSerializer):
    class Meta :
        model = Keyword
        fields = "__all__"

class LimitSerializer(ModelSerializer):
    class Meta :
        model = Limit
        fields = "__all__"

class SocialProfileSerializer(ModelSerializer):
    class Meta :
        model = SocialProfile
        fields = "__all__"
    
    
    def save(self,*args, **kwargs):
        data = SocialProfile.objects.all()
        print("data",data)
        data.delete()
        return super().save(*args, **kwargs)

class LandingPageSerializer(ModelSerializer):
    class Meta :
        model = LandingPage
        fields = "__all__"

class PageSerializer(ModelSerializer):
    class Meta :
        model = Pages
        fields = "__all__"