# from django.shortcuts import render
from django.db.models import Sum
from donors.models import Donor
from .serializers import * 
from .models import (
    Campaign, 
    Campaigncategory,
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
from portals.services import paginate_model_data,paginate_data


# 
class CampaignApi(GenericMethodsMixin,APIView):
    model = Campaign
    serializer_class = CampaignAdminSerializer
    create_serializer_class = CampaignSerializer
    lookup_field = "id"
    
    def get(self,request,pk=None,*args, **kwargs):
        try : 
            if pk:
                data = Campaign.objects.get(id=pk)
                serializer = CampaignAdminSerializer(data=data)
                return Response({"error" : False , "data" : serializer.data},status=status.HTTP_200_OK)
            else :
                data = Campaign.objects.filter(status="Active")
                response = paginate_data(model=Campaign,serializer=CampaignAdminSerializer,request=request,data=data)
                return Response(response,status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error" : True, "message" : str(e)},status=status.HTTP_200_OK)

class  CampaigncategoryApi(GenericMethodsMixin,APIView):
    model = Campaigncategory
    serializer_class = CampaignCategorySerializer
    lookup_field = "id"
    

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

# Camapign By Catagory
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
   
          
from django.db.models import Count

class CampaignFilterAPI(APIView):
   def get(self,request,key,*args, **kwargs):
        if key == "most_supported" : 
        # Most supported 
            Campaign.objects.annotate(donor_count=Count('donors')).order_by('-donor_count')
        # Needs_love
        if key == "needs_love" : 
            Campaign.objects.annotate(donor_count=Count('donors')).order_by('donor_count')
        # Expiring soon
        if key == "expiring_soon" : 
            Campaign.objects.filter().order_by('-end_date')
        # newly added logic 
        if key == "newly_added" : 
            Campaign.objects.filter().order_by('-created_on')
        # response =paginate_model_data(model=Campaign,serializer=CampaignSerializer2,request=request,filter_key='category')

# Need's love ---> donor count is less 
# Expiring Soon --> campaign Which are expiring soon

# data =  Campaign.objects.annotate(donor_count=Count('donors')).order_by('donor_count')
# for item in data :
#     print(item,item.fund_raised)


# Days left 

class AddCampaignApi(APIView):
    def post(self,request,pk=None,*args, **kwargs):
        try : 
            # return Response(status=status.HTTP_400_BAD_REQUEST)
            with transaction.atomic():
                if pk :
                    data = request.data
                    print("---------------------",request.data)
                    campaign = Campaign.objects.get(id=pk)
                    c_serializer = CampaignSerializer(campaign,data=request.data,partial=True)
                    c_serializer.is_valid(raise_exception=True)
                    c_serializer.save()
                    print("------------------Updating Campaigns-----------------------")
                    print(campaign.id,campaign)
                    uploaded_docs = request.FILES.getlist("documents")
                    print(uploaded_docs,request.FILES)
                    if uploaded_docs:
                        print("deletting Docs")
                        Documents.objects.filter(campaign=campaign).delete()
                        print("------------------Updating Docs-----------------------")
                        documents_to_create = [Documents(doc_file=item, campaign=campaign) for item in uploaded_docs]
                        Documents.objects.bulk_create(documents_to_create)
                    
                    # Acocunt Details 
                    print("----------------------Updating Accounts----------------------")
                    obj = BankKYC.objects.get(campaign=campaign)
                    request.data["campaign"] = campaign.id
                    bkc_serializer = BankKYCSerializer(obj, data=request.data,partial = True)
                    bkc_serializer.is_valid(raise_exception=True)
                    bkc_serializer.save()
                    return Response({"error": False, "message": "Campaign Data Updated Successfully", "data": c_serializer.data}, status=status.HTTP_200_OK)
                else :
                    print(request.FILES,"====================>")
                    print("---------------------",request.data)
                    print("camapign save")
                    request.data["user"]  = "e5477dc6-2ae9-4622-93f3-ae68162b7007"
                    campaign_serializer = CampaignSerializer(data=request.data)
                    if campaign_serializer.is_valid(raise_exception=True):
                        campaign = campaign_serializer.save()
                        print("---------------Document saved---------------------")
                        uploaded_docs = request.FILES.getlist("documents")
                        print("uploaded docus ","------------------>",uploaded_docs)
                        documents_to_create = [Documents(doc_file=item, campaign=campaign) for item in uploaded_docs]
                        Documents.objects.bulk_create(documents_to_create)
                        print("---------------Bank KYC Saving---------------------")
                        request.data["campaign"] = campaign.id
                        bkc_serializer = BankKYCSerializer(data = request.data)
                        bkc_serializer.is_valid(raise_exception=True)
                        bkc_serializer.save()
                        print("---------------Bank KYC  Saved ---------------------")
                        return Response({"error" : False, "message" : "Campaign Data Saved Succefully" , "data" : campaign_serializer.data, "id" : campaign.id},status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error" : True , "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)


# from django.db.models import Q
# search = [{"username" : "az"},{"email" : "33az"}]
# search =[{'column':'user','operator':'=','value':'wijdsjdjd'},{'column':'user','operator':'=','value':'wijdsjdjd'}]
# if search :
#             query = Q()
#             for item in search:
#                 print(item['column'])
#             #         query &= Q(**{f"{key}__icontains": value})
#             #     print(query,"query is ")
#             # data = User.objects.filter(query)
#             # print("data",len(data),data)
