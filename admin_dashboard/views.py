from django.shortcuts import render
from .serializers import *
from .models import *
from campaigns.models import *
from donors.models import *
from django.utils import timezone
from rest_framework.views import APIView
from portals.GM2 import GenericMethodsMixin
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ValidationError
from django.db.models import Sum
from rest_framework.permissions import IsAdminUser
from campaigns.serializers import * 

class PagesAPi(APIView):
    model = Pages
    serializer_class = PageSerializer
    lookup_field = "id"
    permission_classes = [IsAdminUser]

class GeneralSettingApi(GenericMethodsMixin,APIView):
    model = GeneralSetting
    serializer_class = GSSerializer
    lookup_field = "id"

class KeywordSApi(GenericMethodsMixin,APIView):
    model = Keyword
    serializer_class = KeywordSerializer
    lookup_field = "id"

class LimitApi(GenericMethodsMixin,APIView):
    model = Limit
    serializer_class = LimitSerializer
    lookup_field = "id"

class SocialProfileApi(GenericMethodsMixin,APIView):
    model = SocialProfile
    serializer_class = SocialProfileSerializer
    lookup_field = "id"

class LandingPageSettingApi(GenericMethodsMixin,APIView):
    model = LandingPage
    serializer_class = LandingPageSerializer
    lookup_field = "id"

class AdminDashboardApi(APIView):
    def get(self,request,*args, **kwargs):
        data = {
                "no_of_donation" : Donor.objects.count(),
                "total_campaign" : Campaign.objects.count(),
                "fund_raised" : Campaign.objects.filter().aggregate(Sum('fund_raised'))['fund_raised__sum'] or 0,
                "user" : User.objects.filter().count()
            }
        return Response({"data" : data},status=status.HTTP_200_OK)                    

class AdminDonationApi(APIView):
    def get(self,request,*args, **kwargs):
        end_date = timezone.now()
        start_date = end_date - timedelta(days=30)
        fundraise_data = Campaign.objects.filter(donors__date__range=(start_date,end_date)).values('donors__date').annotate(
        total_amount=Sum('donors__amount')
        ).order_by('donors__date')
        date_list = [start_date + timedelta(days=x) for x in range(30)]
        result = [
                {"date": date.date(), "total_amount": next((item["total_amount"] for item in fundraise_data if item["donors__date"] == date.date()), 0)}
                for date in date_list
            ]
        return Response({"fundraised_data" : result },status=status.HTTP_200_OK)

class UserUpdateApi(APIView):
    def put(self,request,pk,*args, **kwargs):
        try : 
            campaign = Campaign.objects.get(id=pk)
            data = campaign.campaign_data
            serializer  = CampaignSerializer(campaign,data=data,partial=True)
            if serializer.is_valid():
                serializer.save()
                campaign.is_admin_approved = True
                return Response({"error" : False , "data" : serializer.data},status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error" : True, "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)
            
class CampaignKycAPI(APIView):
    model = BankKYC
    serializer_class = CampBankKycSerializer
    lookup_field = "id"
               
# user role and authentication.
# user update api.
# update the data when admin approve it.
# add admin authentication
# add user authentication
# 