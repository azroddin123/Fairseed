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
from django.db import transaction
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


# Campaign Detail API
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
        try : 
            with transaction.atomic():
                if pk :
                    campaign = Campaign.objects.get(id=pk)
                    c_serializer = CampaignSerializer(campaign,data=request.data,partial=True)
                    c_serializer.is_valid(raise_exception=True)
                    c_serializer.save()
                    
                    print(campaign.id,campaign)
                    # if Documents 
                    upload_adhar  = request.FILES.getlist("adhar")
                    uploaded_docs = request.FILES.getlist("documents")
                    
                    print(uploaded_docs)
                        # Uodate Account 
                    if uploaded_docs:
                        print("deletting Docs")
                        Documents.objects.filter(campaign=campaign).delete()
                        print("updating docs")
                        documents_to_create = [Documents(doc_file=item, campaign=campaign) for item in uploaded_docs]
                        Documents.objects.bulk_create(documents_to_create)
                        
                    # Acocunt Details 
                    AccountDetail.objects.get(campaign=campaign).delete()
                    
                    request.data["campaign"] = campaign.id
                    account_serializer = AccountDSerializer(data=request.data)
                    account_serializer.is_valid(raise_exception=True)
                    account_serializer.save()
                    
                    # Kyc 
                    Kyc.objects.get(campaign=campaign).delete()
                    
                    request.data["adhar_card_front"] = upload_adhar[0]
                    request.data["adhar_card_back"]  = upload_adhar[1]
                    
                    kyc_serializer = KycSerializer(data=request.data)
                    kyc_serializer.is_valid(raise_exception=True)
                    kyc_serializer.save()
                    return Response({"error": False, "message": "Campaign Data Updated Successfully", "data": c_serializer.data}, status=status.HTTP_200_OK)
              
                else :
                    data = request.data
                    uploaded_docs = request.FILES.getlist('documents')
                    upload_adhar  = request.FILES.getlist("adhar")
                    campaign_serializer = CampaignSerializer(data=request.data)
                    if campaign_serializer.is_valid():
                        campaign = campaign_serializer.save()
                        documents_to_create = [Documents(doc_file=item, campaign=campaign) for item in uploaded_docs]
                        Documents.objects.bulk_create(documents_to_create)
                        request.data["campaign"]=campaign.id
                        
                        # Code For Account Serializer
                        account_serializer = AccountDSerializer(data=request.data)
                        account_serializer.is_valid(raise_exception=True)
                        account_serializer.save()
              
                        # code for Kyc Serializer 
                        request.data["adhar_card_front"] = upload_adhar[0]
                        request.data["adhar_card_back"]  = upload_adhar[1]
                        kyc_serializer = KycSerializer(data=request.data)
                        kyc_serializer.is_valid(raise_exception=True)
                        kyc_serializer.save()
                        serializer = KycSerializer(data=request.data)
                        return Response({"error" : False, "message" : "Campaign Data Saved Succefully" , "data" : campaign_serializer.data},status=status.HTTP_200_OK)
                    
        except Exception as e :
            return Response({"error" : True , "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)
    