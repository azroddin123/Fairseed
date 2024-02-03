
# Create your views here.
# from django.shortcuts import render
from django.db.models import Sum
from donors.models import Donor
from campaigns.serializers import * 
from donors.serializers import * 
from campaigns.models import * 
from rest_framework.views import APIView
from portals.GM2 import GenericMethodsMixin
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator
from django.utils import timezone


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
        donation_data = Donor.objects.filter(date__range=(start_date,end_date),user=request.thisUser).values('date').annotate(
               total_amount=Sum('amount')
                ).order_by('date')
        # Date list 
        date_list = [start_date + timedelta(days=x) for x in range(30)]
        result = [
                {"date": date.date(), "total_amount": next((item["total_amount"] for item in donation_data if item["date"] == date.date()), 0)}
                for date in date_list
            ]
        return Response({"donation_data" : result},status=status.HTTP_200_OK)


# FundRaised API
class FundRaisedApi(APIView):
    def get(self,request):
        end_date = timezone.now()
        start_date = end_date - timedelta(days=30)
        fundraise_data = Campaign.objects.filter(donors__date__range=(start_date,end_date),user=request.thisUser).values('donors__date').annotate(
        total_amount=Sum('donors__amount')
        ).order_by('donors__date')
        date_list = [start_date + timedelta(days=x) for x in range(30)]
        result = [
                {"date": date.date(), "total_amount": next((item["total_amount"] for item in fundraise_data if item["donors__date"] == date.date()), 0)}
                for date in date_list
            ]
        return Response({"fundraised_data" : result },status=status.HTTP_200_OK)
        
        
# Campaign API
class CampaignApi(GenericMethodsMixin,APIView):
    model = Campaign
    serializer_class = CampaignAdminSerializer
    create_serializer_class = CampaignSerializer
    lookup_field = "id"
    
    def put(self,request,pk,*args, **kwargs):
        print(request.data)
        campaign = Campaign.objects.get(id=pk)
        print(request.data)
        campaign.campaign_data=request.data
        campaign.save()
        return Response({"error" : False , "message" : "Campaign Edit request sent to admin"},status=status.HTTP_200_OK)
# Donor API Donation Done By MySelf 
class MyDonationApi(GenericMethodsMixin,APIView):
    model= Donor
    serializer_class = DonorSerializer
    lookup_field = "id"
    
    
# Recieved Donation For my Campaign 
class RecivedDonationApi(APIView):
    def get(self,request,*args, **kwargs):
        data = Donor.objects.filter(campaign__user="bee9ed7f-ade9-4dd3-a136-d043dd4b9a52")
        serializer = DonorSerializer(data,many=True)
        return Response({"data": serializer.data},status=status.HTTP_200_OK)


# class BankKycApi(GenericMethodsMixin,APIView):
#     model = BankKYC
#     serializer_class = BankKYCSerializer
#     lookup_field = "id"
    
# user --> Campaign --> Donation 
# User = request.thisUser 

class ViewBankAndKycAPi(APIView):
    def get(self,request,pk,*args, **kwargs):
        try : 
            bank_data = AccountDetail.objects.get(campaign=pk)
            kyc_data  = Kyc.objects.get(campaign=pk)
            
            serializer      = AccountDSerializer(bank_data)
            kyc_serializer  = KycSerializer(kyc_data)
            return Response({ "error" : False , "bank_data" : serializer.data ,
                "kyc_data" : kyc_serializer.data
            },status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error" : True , "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk,*args, **kwargs):
        try :
            bank_data = AccountDetail.objects.get(campaign=pk)
            kyc_data  = Kyc.objects.get(campaign=pk)

            bank_serializer = AccountDSerializer(bank_data,data=request.data,partial=True)
            if bank_serializer.is_valid():
                bank_serializer.save()
            
            kyc_serializer = KycSerializer(kyc_data,data=request.data,partial=True)
            if kyc_serializer.is_valid():
                kyc_serializer.save()
            
            return Response({"error" : False ,"message" : "Your Request sent to admin for verification"})
        except Exception as e :
            return Response({"error" : True , "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)

                