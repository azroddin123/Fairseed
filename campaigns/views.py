# from django.shortcuts import render
from django.db.models import Sum
from donors.models import Donor
from .serializers import * 
from .models import (
    Campaign, 
    Campaigncategory,
    AccountDetail,
    Kyc
    
)
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.views import APIView
import uuid
import math
from portals.GM2 import GenericMethodsMixin
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator

class CampaignApi(GenericMethodsMixin,APIView):
    model = Campaign
    serializer_class = CampaignAdminSerializer
    create_serializer_class = CampaignSerializer
    lookup_field = "id"

class  CampaigncategoryApi(GenericMethodsMixin,APIView):
    model = Campaigncategory
    serializer_class = CampaignCategorySerializer
    lookup_field = "id"

class AccountDetailApi(GenericMethodsMixin,APIView):
    model = AccountDetail
    serializer_class = AccountDSerializer
    lookup_field = "id"

class KycApi(GenericMethodsMixin,APIView):
    model = Kyc
    serializer_class = KycSerializer
    lookup_field = "id"

class CampaignAdminApi(GenericMethodsMixin,APIView):
    model = Campaign
    serializer_class = CampaignAdminSerializer
    create_serializer_class = CampaignSerializer
    lookup_field  = "id"

class DocumentApi(GenericMethodsMixin,APIView):
    model = Documents
    serializer_class = DocumentSerializer
    lookup_field = "id"

class CampaignFilterApi(APIView):
    def get(self,request,*args, **kwargs):
        try : 
            category = request.GET.get('name')
            campain_id=Campaigncategory.objects.get(name=category).first()
            campaing_data = Campaign.objects.filter(category=campain_id)
            serializer = CampaignSerializer1(campaing_data,many=True)
            return Response({"error": False, "rows" : serializer.data },status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error" : str(e) },status=status.HTTP_400_BAD_REQUEST)

class ReportedCauseApi(APIView):
    def get(self,request,*args, **kwargs) :
        try :
            data = Campaign.objects.filter(is_reported=True)
            serializer = CampaignAdminSerializer(data,many=True)
            return Response({"error": False,"count":  len(data) or 0,"rows" : serializer.data },status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error" : str(e) },status=status.HTTP_400_BAD_REQUEST)

class SuccessfulCauseApi(APIView):
    def get(self,request,*args, **kwargs) :
        try :
            data = Campaign.objects.filter(is_successful=True)
            serializer = CampaignAdminSerializer(data,many=True)
            return Response({"error": False,"count":  len(data) or 0,"rows" : serializer.data },status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error" : str(e) },status=status.HTTP_400_BAD_REQUEST)

class CampaignByCategoryApi(APIView):
    def get(self, request, *args, **kwargs):
        try:
            cat_id = request.GET.get('category')
            data = Campaign.objects.filter(category=cat_id)
            print(len(data))
            serializer = CampaignAdminSerializer(data, many=True)
            return Response({
                "count": len(data),
                "error": False,
                "rows": serializer.data,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CampaignDetailsApi(APIView):
    def get(self,request,pk,*args, **kwargs): 
        try :       
            data = Campaign.objects.get(pk=pk)
            serializer = CampaignDetailSerializer(data)
            return Response({"error": False, "data" : serializer.data},status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Landing page api
class LandingPageApi(APIView):
    def get(self,request,*args, **kwargs) :
        try : 
            data = {
            "total_campaign" : Campaign.objects.count(),
            "total_donation" : Donor.objects.aggregate(Sum('amount'))['amount__sum'] or 0,
            "donor_count" : Donor.objects.count(),
            "successfull_campaign" : Campaign.objects.filter(is_successful=True).count(),
            # this should be done when the amoint is credited to student account.
            "student_benifited" : Campaign.objects.filter(is_withdrawal=True).count()
            }
            serializer = DashboardSerializer(data)
            return Response({"error" : False,"data" : serializer.data},status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error" : str(e)},status=status.HTTP_400_BAD_REQUEST)


# Create campaign API
class AddCampaignApi(APIView):
    def post(self,request,pk=None,*args, **kwargs):
        
        print(request.thisUser,"asdfghfrewq12345678987654321234567")
        # request.data['user'] = request.thisUser.id
        print("in add campaign")
        data = request.data
        print(data,"-------------------->")
        serializer = CampaignSerializer(data=data)
        if serializer.is_valid():
            print("serialier is valid")
            campaign = serializer.save()
            print(request.data["documents"])
            print(campaign,"this is campaign")
            uploaded_docs = request.FILES.getlist('documents')
            # upload_adhar  = request.FILES.getlist("adhar")
            # pan           = request.FILES.get("pan")
            # passbook_img      = request.FILES.get("passbook_img")
            
            # Documents save 
            doc_list = [] 
            for item in uploaded_docs:
                print("item",item)
                obj = Documents(doc_file=item,campaign=campaign)
                obj.save()
                print("saved",item)
                
                
            # Account Save 
            account_serializer = AccountDSerializer(data=data)
        
        # Kyc Save 

     
        
     
        # acocunt_details = []
        # kyc_details = [] 
        # documents = [] 
        return Response({"data" : serializer.data})
        
        
    