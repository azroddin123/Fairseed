from django.shortcuts import render
from .serializers import *
from .models import *
from campaigns.models import *
from donors.models import *
from donors.serializers import * 
from django.utils import timezone
from rest_framework.views import APIView
from portals.GM2 import GenericMethodsMixin
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ValidationError
from django.db.models import Sum
from rest_framework.permissions import IsAdminUser
from campaigns.serializers import * 
from django.db import transaction
from accounts.serializers import * 


class PagesAPi(GenericMethodsMixin,APIView):
    model = Pages
    serializer_class = PageSerializer
    lookup_field = "id"


class PagesSlugApi(APIView):
    def get(self,request,slug=None):
        try : 
            data = Pages.objects.get(slug=slug)
            serializer = PageSerializer(data)
            return Response({ "error" : False ,"data" : serializer.data},status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error" : True, "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)

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
        fundraise_data = Campaign.objects.filter(donors__created_on__range=(start_date,end_date)).values('donors__created_on').annotate(
        total_amount=Sum('donors__amount')
        ).order_by('donors__created_on')
        date_list = [start_date + timedelta(days=x) for x in range(30)]
        result = [
                {"date": date.date(), "total_amount": next((item["total_amount"] for item in fundraise_data if item["donors__created_on"] == date.date()), 0)}
                for date in date_list
            ]
        return Response({"fundraised_data" : result },status=status.HTTP_200_OK)
from django.db.models import Count

class AdminCountryApi(APIView):
    def get(self,request,*args, **kwargs):
        user_data =  [
        {
            "country": "India",
            "user_count": 4
        },
        {
            "country": "Australia",
            "user_count": 3
        }]
        country_user_count = User.objects.values('country').annotate(user_count=Count('id'))
        return Response({"error" : False, "user_data" :user_data },status=status.HTTP_200_OK)

class UserUpdateApi(APIView):
    def put(self,request,pk,*args, **kwargs):
        try : 
            user = User.objects.get(id=pk)
            serializer  = UserSerializer1(user,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"error" : False , "data" : serializer.data},status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error" : True, "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)
            
class CampaignKycAPI(GenericMethodsMixin,APIView):
    model = BankKYC
    serializer_class = CampBankKycSerializer
    lookup_field = "id"
    
    def put(self,request,pk,*args, **kwargs):
        try :
            data = request.data
            print(type(data),"data")
            print("data",request.data)
            with transaction.atomic():
                bankkyc = BankKYC.objects.get(id=pk)
                request.POST._mutable = True
                data.update(bankkyc.bank_data)
                print(data,"new data",bankkyc.bank_data)
                print("data",type(bankkyc.bank_data))
                if request.data['approve_kyc'] == 'true' : 
                    serializer = BankKYCSerializer(bankkyc,data=data,partial=True)
                    print("request.data",request.data,bankkyc.bank_data)
                    if serializer.is_valid(raise_exception=True) :
                        print("new bankkyc Data Approved ")
                        serializer.save()
                        # serializer1.save()
                        bankkyc.bank_data = {}
                        print("Approval Status Approved ",bankkyc.bank_data,bankkyc.approval_status)
                        bankkyc.approval_status="Approved"
                        bankkyc.save()
                        # RevisionHistory.objects.create(modeified_by=request.thisUser,bankkyc=bankkyc,bankkyc_data=bankkyc)
                    return Response({"error" : False , "data" : "Bank Kyc  Update Request Approved Successfully" ,"data1" : serializer.data},status=status.HTTP_200_OK)
                else :
                    bankkyc.bank_data = {}
                    bankkyc.approval_status="Rejected"
                    bankkyc.save()
                    # RevisionHistory.objects.create(modeified_by=request.thisUser,campaign=campaign.id,campaign_data=campaign)
                    return Response({"error" : False , "data" : "Bank KYC Update Request Rejected Successfully"},status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error" : True, "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)

class DonorsApi(GenericMethodsMixin,APIView):
    model = Donor
    serializer_class = DonorSerializer
    lookup_field = "id"

class  CampaigncategoryApi2(GenericMethodsMixin,APIView):
    model = Campaigncategory
    serializer_class = CampaignCategorySerializer
    lookup_field = "id"
    
class RevisionHistoryApi(APIView):
    def get(self,request,pk,*args, **kwargs):
        try :
            data = RevisionHistory.objects.filter(campaign=pk)
            print(len(data),"this much objectr")
            serializer = RHSerializer(data,many=True)
            return Response({"error" : False , "data" : serializer.data},status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error" : True, "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)
            
            
class UserApi2(GenericMethodsMixin,APIView):
    model = User
    serializer_class = UserAdminSerializer1
    create_serializer_class = UserSerializer1
    lookup_field  = "id"

class CampaignAdminApi2(GenericMethodsMixin,APIView):
    model = Campaign
    serializer_class = CampaignDocumentSerializer
    create_serializer_class = CampaignSerializer
    lookup_field  = "id"



class CampaignEditApproval(GenericMethodsMixin,APIView):
    model = Campaign
    serializer_class = CampaignSerializer
    lookup_field="id"
    
    def get(self,request,pk=None,*args, **kwargs):
        try :
            if pk==None : 
                data = Campaign.objects.filter(approval_status="Pending")
                print(len(data),"this much objectr")
                serializer = CampaignDocumentSerializer(data,many=True)
                return Response({"error" : False , "rows" : serializer.data},status=status.HTTP_200_OK)
            
            data = Campaign.objects.get(id=pk,approval_status="Pending")
            serializer = CampaignDocumentSerializer(data)
            return Response({"error" : False , "data" : serializer.data},status=status.HTTP_200_OK)

        
        except Exception as e :
            return Response({"error" : True, "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)
      
    def put(self,request,pk,*args, **kwargs):
        try :
            print("=================zaid========",request.data)
            # print(type(request.data['appprove_campaign']),request.data['appprove_campaign'])
            # we have to import all the data in the rh history also 
            with transaction.atomic():
                campaign = Campaign.objects.get(id=pk)
                if request.data['approve_campaign'] == "true" : 
                    serializer = CampaignSerializer(campaign,data=campaign.campaign_data,partial=True)
                    campaign.campaign_data['approval_status'] = "Approved"
                    if serializer.is_valid():
                        print("new campaign Data Approved ")
                        serializer.save()
                        campaign.campaign_data = {}
                        print("Approval Status Approved ",campaign.campaign_data,campaign.approval_status)
                        campaign.approval_status="Approved"
                        campaign.is_admin_approved = True
                        campaign.save()
                        # RevisionHistory.objects.create(modeified_by=request.thisUser,campaign=campaign,campaign_data=campaign)
                    return Response({"error" : False , "data" : "Camapaign Update Request Approved Successfully"},status=status.HTTP_202_ACCEPTED)
                else :
                    campaign.campaign_data = {}
                    campaign.approval_status="Rejected"
                    campaign.save()
                    # RevisionHistory.objects.create(modeified_by=request.thisUser,campaign=campaign.id,campaign_data=campaign)
                    return Response({"error" : False , "data" : "Camapaign Update Request Rejected Successfully"},status=status.HTTP_202_ACCEPTED)
        except Exception as e :
            return Response({"error" : True, "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)

class DocumentAPI(GenericMethodsMixin,APIView):
    model = Documents
    serializer_class = DocumentSerializer
    lookup_field = "id"


# Remaining Work
# 
class WithdrawalApi(GenericMethodsMixin,APIView):
    model = Withdrawal
    serializer_class = WithDrawalSerializer
    lookup_field = "id"

    def post(self,request,*args,**kwargs):
        pass
