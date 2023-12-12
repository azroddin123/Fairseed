from django.shortcuts import render
from django.db.models import Sum
from donor.models import Donor
from .serializers import * 
from .models import (
    Campaign,
    CampaignCatagories,
    BenificiaryBankDetails,
    KycDetails
)
from rest_framework.views import APIView

from fairseed.GM import GenericMethodsMixin
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class CampaignApi(GenericMethodsMixin,APIView):
    model = Campaign
    serializer_class = CampaignSerializer
    lookup_field = "id"

class  CampaignCatagoryApi(GenericMethodsMixin,APIView):
    model = CampaignCatagories
    serializer_class = CampaignCatagorySerializer
    lookup_field = "id"

class BBDApi(GenericMethodsMixin,APIView):
    model = BenificiaryBankDetails
    serializer_class = BBDetailSerailizer
    lookup_field = "id"

class KycApi(GenericMethodsMixin,APIView):
    model = KycDetails
    serializer_class = KycDetailSerializer
    lookup_field = "id"


class DashboardApi(APIView):
    def get(self,request,*args, **kwargs) :
        data = {
        "total_campaign" : Campaign.objects.count(),
        "total_donation" : Donor.objects.aggregate(total_amount=Sum("amount")).get('total_amount', 0),
        "donor_count" : Donor.objects.count(),
        "successfull_campaign" : Campaign.objects.filter(is_successfull=True).count(),
        "student_benifited" : Campaign.objects.filter(is_successfull=True).count()
        }

        print(data)
        
        serializer = DashboardSerializer(data=data)
        if serializer.is_valid():
            return Response(data=serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class CampaignFilterApi(APIView):
    def get(self,request,*args, **kwargs):
        try : 
            catagory = request.GET.get('name')
            campain_id=CampaignCatagories.objects.get(name=catagory)
            print("1===================>")
            campaing_data = Campaign.objects.filter(catagory=campain_id)
            print("campaign data",campaing_data)
    
            serializer = CampaignSerializer1(campaing_data,many=True)
            return Response({"error": False, "data" : serializer.data },status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error" : str(e) },status=status.HTTP_200_OK)

