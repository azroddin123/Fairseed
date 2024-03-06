# Create your views here.
# from django.shortcuts import render
from django.db.models import Sum
from donors.models import Donor
from campaigns.serializers import * 
from donors.serializers import * 
from campaigns.models import * 
from rest_framework.views import APIView
from portals.GM1 import GenericMethodsMixin
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder
import json


# User Dasboard API
class UserDashboardApi(APIView):
    def get(self,request,*args, **kwargs):
        print(request.thisUser)
        # print(Donor.objects.count(user=request.thisUser))
        data = {
            "no_of_donation" : Donor.objects.filter(user=request.thisUser).count(),
            "total_campaign" : Campaign.objects.filter(user=request.thisUser).count(),
            "amount_receieved" : Campaign.objects.filter(user=request.thisUser).aggregate(Sum('fund_raised'))['fund_raised__sum'] or 0,
        }
        return Response({"data" : data},status=status.HTTP_200_OK)


# Donation Count API
class DonationCountApi(APIView):
    def get(self,request):
        end_date = timezone.now()
        start_date = end_date - timedelta(days=30)
        # Donation Data
        donation_data = Donor.objects.filter(created_on__range=(start_date,end_date),user=request.thisUser).values('created_on').annotate(
               total_amount=Sum('amount')
                ).order_by('created_on')
        # Date list 
        date_list = [start_date + timedelta(days=x) for x in range(30)]
        result = [
                {"date": date.date(), "total_amount": next((item["total_amount"] for item in donation_data if item["created_on"] == date.date()), 0)}
                for date in date_list
            ]
        return Response({"donation_data" : result},status=status.HTTP_200_OK)

# FundRaised API
class FundRaisedApi(APIView):
    def get(self,request):
        end_date = timezone.now()
        start_date = end_date - timedelta(days=30)
        fundraise_data = Campaign.objects.filter(donors__created_on__range=(start_date,end_date),user=request.thisUser).values('donors__created_on').annotate(
        total_amount=Sum('donors__amount')
        ).order_by('donors__created_on')
        date_list = [start_date + timedelta(days=x) for x in range(30)]
        result = [
                {"date": date.date(), "total_amount": next((item["total_amount"] for item in fundraise_data if item["donors__created_on"] == date.date()), 0)}
                for date in date_list
            ]
        return Response({"fundraised_data" : result },status=status.HTTP_200_OK)
        
        
# Campaign API
class CampaignApi3(GenericMethodsMixin,APIView):
    model = Campaign
    serializer_class = CampaignAdminSerializer
    create_serializer_class = CampaignSerializer
    lookup_field = "id"
    
    def put(self,request,pk,*args, **kwargs):
        try :
            campaign = Campaign.objects.get(id=pk)
            campaign.campaign_data = request.data
            campaign.approval_status = "Pending"
            campaign.save()
            return Response({"error" : False , "message" : "Your changes have been recorded for this campaign and are sent for approval to the admin"},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error" : True , "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)

# Donor API Donation Done By MySelf 
class MyDonationApi(GenericMethodsMixin,APIView):
    model= Donor
    serializer_class = DonorSerializer
    lookup_field = "id"
    
# Recieved Donation For my Campaign 
class RecivedDonationApi(APIView):
    def get(self,request,*args, **kwargs):
        data = Donor.objects.filter(campaign__user=request.thisUser)
        serializer = DonorSerializer(data,many=True)
        return Response({"data": serializer.data},status=status.HTTP_200_OK)

class BankKycApi(GenericMethodsMixin,APIView):
    model = BankKYC
    serializer_class = BankKYCSerializer
    lookup_field = "id"
    
    def put(self,request,pk,*args, **kwargs):
        try :
            campaign = BankKYC.objects.get(id=pk)
            campaign.campaign_data = request.data
            campaign.approval_status = "Pending"
            campaign.save()
            return Response({"error" : False , "message" : "Your changes have been recorded for this campaign and are sent for approval to the admin"},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error" : True , "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)

class ViewBankAndKycAPi(APIView):
    def get(self,request,pk,*args, **kwargs):
        try : 
            bank_data       = BankKYC.objects.get(campaign=pk)
            serializer      = BankKYCSerializer(bank_data)
            return Response({ "error" : False , "data" : serializer.data ,
            },status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error" : True , "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request,pk,*args, **kwargs):
        try :
            kyc = BankKYC.objects.get(campaign=pk)
            kyc.bank_data = request.data
            kyc.approval_status = "Pending"
            kyc.save()
            return Response({"error" : False , "message" : " Your changes has been recorded and are  sent for approval to Admin "},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error" : True , "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)
        

        