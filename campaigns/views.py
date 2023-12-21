from django.shortcuts import render
from django.db.models import Sum
from donors.models import Donor
from .serializers import * 
from .models import (
    Campaign,
    CampaignCatagory,
    CampaignKycBenificiary,
)
from rest_framework.views import APIView
import uuid
from fairseed.GM1 import GenericMethodsMixin
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class CampaignApi(GenericMethodsMixin,APIView):
    model = Campaign
    serializer_class = CampaignSerializer
    lookup_field = "id"

class  CampaignCatagoryApi(GenericMethodsMixin,APIView):
    model = CampaignCatagory
    serializer_class = CampaignCatagorySerializer
    lookup_field = "id"

class CKBApi(GenericMethodsMixin,APIView):
    model = CampaignKycBenificiary
    serializer_class = CKBSerializer
    lookup_field = "id"

# class KycApi(GenericMethodsMixin,APIView):
#     model = KycDetails
#     serializer_class = KycDetailSerializer
#     lookup_field = "id"

class CampaignAdminApi(GenericMethodsMixin,APIView):
    model = Campaign
    serializer_class = CampaignAdminSerializer
    lookup_field  = "id"


class DocumentApi(GenericMethodsMixin,APIView):
    model = Documents
    serializer_class = DocumentSerializer
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
            campain_id=CampaignCatagory.objects.get(name=catagory)
            campaing_data = Campaign.objects.filter(catagory=campain_id)
            serializer = CampaignSerializer1(campaing_data,many=True)
            return Response({"error": False, "data" : serializer.data },status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error" : str(e) },status=status.HTTP_400_BAD_REQUEST)

# getting some issues in this api
class CampaignByCatagoryApi(APIView):
    def get(self,pk,request,*args, **kwargs):
        try :
            data = CampaignCatagory.objects.get(id=pk)
            serializer = CampaignByCatagorySerializer(data)
            return Response({"error" : False,"data" : serializer.data},status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error" : str(e) },status=status.HTTP_400_BAD_REQUEST)

class ReportedCauseApi(APIView):
    def get(self,request,*args, **kwargs) :
        try :
            data = Campaign.objects.filter(is_reported=True)
            serializer = CampaignSerializer1(data,many=True)
            return Response({"error": False, "data" : serializer.data },status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error" : str(e) },status=status.HTTP_400_BAD_REQUEST)




class CampaignDetailsApi(APIView):
    model = Campaign
    serializer_class = CampaignSerializer
    lookup_field  = "id"

    def get(self,request,pk=None,*args, **kwargs):
        # try :
            print(type(pk),"pk is a valid id")
            if pk == None or pk == str(0) :
                print("111111111111")
                try : 
                    data = Campaign.objects.all()
                    serializer = CampaignAdminSerializer(data,many=True)
                    return Response(data=serializer.data,status=status.HTTP_200_OK)
                except Campaign.DoesNotExist:
                    return Response({"error" : "Record not found or exists"},status=status.HTTP_400_BAD_REQUEST)
            else :
                data = Campaign.objects.get(pk=pk)
                serializer = CampaignDetailSerializer(data)
                return Response(data=serializer.data,status=status.HTTP_200_OK)
        # except :
        #         return Response(status=status.HTTP_400_BAD_REQUEST)
    