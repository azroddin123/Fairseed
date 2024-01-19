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
from django.core.paginator import Paginator,EmptyPage
from portals.services import paginate_model_data

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

# Camapign By Catagory : ---> 
class CampaignByCategoryApi(APIView):
    def get(self,request,*args, **kwargs):
        try : 
            cat_id = request.GET.get('category')
            response = paginate_model_data(model=Campaign,serializer=CampaignSerializer2,request=request,filter_key='category')
            category_data = CampaignCategorySerializer(Campaigncategory.objects.get(id=cat_id)).data 
            response["category_data"] = category_data
            return Response(response,status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error" : True, "message" : str(e)},status=status.HTTP_200_OK)
   
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
                    print(len(upload_adhar),"------------------->")
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
                    data._mutable = True

                    # uploaded_docs = request.FILES.getlist('documents')
                    # upload_adhar  = request.FILES.getlist("adhar")
                    print("---------------------")
                    print("camapign save")
                    
                    request.data["user"] = "574db924-d56a-4978-a56c-97727bdadacf"
                    campaign_serializer = CampaignSerializer(data=request.data)
                    if campaign_serializer.is_valid(raise_exception=True):
                        print("serilaizer is valid")
                        campaign = campaign_serializer.save()
                        print("Document save")
                        # documents_to_create = [Documents(doc_file=item, campaign=campaign) for item in uploaded_docs]
                        # Documents.objects.bulk_create(documents_to_create)
                
                        request.data["campaign"] = campaign.id
                        account_serializer = AccountDSerializer(data=data)
                        account_serializer.is_valid(raise_exception=True)
                        account_serializer.save()

                        # code for Kyc Serializer 
                        print("kyc save")
                        # request.data["adhar_card_front"] = upload_adhar[0]
                        # request.data["adhar_card_back"]  = upload_adhar[1]
                        
                        kyc_serializer = KycSerializer(data=request.data)
                        kyc_serializer.is_valid(raise_exception=True)
                        kyc_serializer.save()
                        
                        return Response({"error" : False, "message" : "Campaign Data Saved Succefully" , "data" : campaign_serializer.data},status=status.HTTP_200_OK)
                   
        except Exception as e :
            return Response({"error" : True , "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)

class CampaignByCategoryApi2(APIView):
    def get(self,request,pk,*args, **kwargs):
        try : 
            cat_id = request.GET.get('category')
            response = paginate_model_data(model=Campaign,serializer=CampaignSerializer2,request=request,filter_key='category')
            category_data = CampaignCategorySerializer(Campaigncategory.objects.get(id=cat_id)).data 
            response["category_data"] = category_data
            return Response(response,status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error" : True, "message" : str(e)},status=status.HTTP_200_OK)
   
            cat_id = request.GET.get('category')
            print(request.GET.get('limit'), " --------------------------------limit---------------------------->")
            print(request.GET.get('page'),"-----------------------------------page---------------------------->")
            limit = max(int(request.GET.get('limit', 0)),1) 
            page_number = max(int(request.GET.get('page', 0)), 1)  
            data = Campaign.objects.filter(category=pk)
            print(len(data))
            paginator = Paginator(data, limit)
            try:    
                current_page_data = paginator.get_page(page_number)
            except EmptyPage:
                return Response({"error": True, "message": "Page not found"},status=status.HTTP_404_NOT_FOUND)
            serializer = CampaignSerializer(current_page_data, many=True)
            return Response({"error": False,"pages_count": paginator.num_pages,"count" : paginator.count,"rows": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error" : True, "message" : str(e)},status=status.HTTP_200_OK)



class CreateCampaignApi(APIView):
    def post(self,request,*args, **kwargs):
        try :
             with transaction.atomic():
                campaign_serializer = CampaignSerializer(data=request.data)
                if campaign_serializer.is_valid():
                    campaign = campaign_serializer.save()
                    
                    uploaded_docs = request.FILES.getlist("documents")
                    if uploaded_docs:
                        print("adding docs")
                        documents_to_create = [Documents(doc_file=item, campaign=campaign) for item in uploaded_docs]
                        Documents.objects.bulk_create(documents_to_create)
                        
                        account = request.data.get('account_details')
                        obj = AccountDetail.objects.create(campaign=campaign,account_holder_name = account["account_holder_name"],account_number=account["account_number"],bank_name=account["bank_name"],branch_name=account["branch_name"],ifsc_code = account["ifsc_code"]) 

                    # return Response({"error" : True, "message" : "Campaign create successfully"},status=status.HTTP_200_OK)
                    # account_details = request.data.get('account_details')
                    # obj = AccountDetail(campaign=campaign,account_holder_name=account_details["account_holder_name"])
        except Exception as e:
            return Response({"error" : True, "message" : str(e)},status=status.HTTP_200_OK)           
                     

# Filter API
# days left 
# Trending  --> 
# Most Supported --> where donor count is grater 

# Need's love ---> donor count is less 
# Expiring Soon --> campaign Which are expiring soon
# 