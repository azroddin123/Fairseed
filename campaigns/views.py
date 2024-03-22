# from django.shortcuts import render
from django.db.models import Sum
from donors.models import Donor
from .serializers import * 
from .models import (
    Campaign, 
    Campaigncategory,
)
from datetime import datetime
current_date = datetime.now()
from django.db import transaction
from rest_framework.views import APIView
from portals.GM2 import GenericMethodsMixin
from rest_framework.response import Response
from rest_framework import status
from portals.services import paginate_model_data,paginate_data
from django.db.models import Count

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
                data = Campaign.objects.filter(status="Active",end_date__gt=current_date)
                response = paginate_data(model=Campaign,serializer=CampaignAdminSerializer,request=request,data=data)
                return Response(response,status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error" : True, "message" : str(e)},status=status.HTTP_200_OK)


class  CampaigncategoryApi(GenericMethodsMixin,APIView):
    model = Campaigncategory
    serializer_class = CampaignCategorySerializer
    lookup_field = "id"

    def get(self,request,*args, **kwargs) :
        try :
            data = Campaigncategory.objects.filter(is_active=True)
            response = paginate_data(Campaigncategory, CampaignCategorySerializer, request, data)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error" : str(e) },status=status.HTTP_400_BAD_REQUEST)

class DocumentApi(GenericMethodsMixin,APIView):
    model = Documents
    serializer_class = DocumentSerializer
    lookup_field = "id"

class CampaignFilterApi(APIView):
    def get(self,request,*args, **kwargs):
        try : 
            category = request.GET.get('name')
            campaign_id=Campaigncategory.objects.get(name=category)
            campaign_data = Campaign.objects.filter(category=campaign_id)
            response = paginate_data(model=Campaign,serializer=CampaignSerializer1,request=request,data=campaign_data)
            return Response(response,status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error" : str(e) },status=status.HTTP_400_BAD_REQUEST)

class ReportedCauseApi(APIView):
    def get(self,request,*args, **kwargs) :
        try :
            data = Campaign.objects.filter(is_reported=True)
            response = paginate_data(model=Campaign,serializer=CampaignAdminSerializer,request=request,data=data)
            return Response(response,status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error" : str(e) },status=status.HTTP_400_BAD_REQUEST)

class SuccessfulCauseApi(APIView):
    def get(self,request,*args, **kwargs) :
        try :
            data = Campaign.objects.filter(is_successful=True)
            response = paginate_data(model=Campaign,serializer=CampaignAdminSerializer,request=request,data=data)
            return Response(response,status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error" : str(e) },status=status.HTTP_400_BAD_REQUEST)

class FeaturedCauseApi(APIView):
    def get(self,request,*args, **kwargs) :
        try :
            data = Campaign.objects.filter(is_featured=True)
            response = paginate_data(model=Campaign,serializer=CampaignAdminSerializer,request=request,data=data)
            return Response(response,status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error" : str(e) },status=status.HTTP_400_BAD_REQUEST)

# Campaign By Category
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
            "successful_campaign" : Campaign.objects.filter(is_successful=True).count(),
            # this should be done when the amount is credited to student account.
            "student_benefited" : Campaign.objects.filter(is_withdrawal=True).count()
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

class CampaignTabsAPi(APIView):
    def get(self, request, *args, **kwargs):
        try:
            filter_key = request.GET.get('filter')
            data = []
            print(filter_key =="most_supported")
            if filter_key  == "most_supported":
                data = Campaign.objects.annotate(donor_count=Count('donors')).order_by('-donor_count').filter(status="Active")
            elif filter_key  == "needs_love": 
                data = Campaign.objects.annotate(donor_count=Count('donors')).order_by('donor_count').filter(status="Active")
            elif filter_key  == "expiring_soon": 
                data = Campaign.objects.filter(status="Active").order_by('-end_date')
            elif filter_key  == "newly_added": 
                data = Campaign.objects.filter(status="Active").order_by('created_on')
            else :
                data = Campaign.objects.filter(status="Active")
            response = paginate_data(Campaign, CampaignAdminSerializer, request, data)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": True, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Need to add category key
class CampaignTabsAPi2(APIView):
    def get(self, request, *args, **kwargs):
        try:
            filter_key = request.GET.get('filter')
            cat_id     = request.GET.get('category')
            data = []
            if filter_key  == "most_supported":
                data = Campaign.objects.annotate(donor_count=Count('donors')).order_by('-donor_count').filter(status="Active",category=cat_id)
            elif filter_key  == "needs_love": 
                data = Campaign.objects.annotate(donor_count=Count('donors')).order_by('donor_count').filter(status="Active",category=cat_id)
            elif filter_key  == "expiring_soon": 
                data = Campaign.objects.filter(status="Active",category=cat_id).order_by('-end_date')
            elif filter_key  == "newly_added": 
                data = Campaign.objects.filter(status="Active",category=cat_id).order_by('created_on')
            else :
                data = Campaign.objects.filter(status="Active",category=cat_id)
            response = paginate_data(Campaign, CampaignAdminSerializer, request, data)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": True, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class AddCampaignApi(APIView):
    def post(self,request,pk=None,*args, **kwargs):
        try : 
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
                        Documents.objects.filter(campaign=campaign).delete()
                        print("------------------Updating Docs-----------------------")
                        documents_to_create = [Documents(doc_file=item, campaign=campaign) for item in uploaded_docs]
                        Documents.objects.bulk_create(documents_to_create)
                    
                    print("----------------------Updating Accounts----------------------")
                    obj = BankKYC.objects.get(campaign=campaign)
                    request.data["campaign"] = campaign.id
                    bkc_serializer = BankKYCSerializer(obj, data=request.data,partial = True)
                    bkc_serializer.is_valid(raise_exception=True)
                    bkc_serializer.save()
                    return Response({"error": False, "message": "Campaign Data Updated Successfully", "data": c_serializer.data}, status=status.HTTP_200_OK)
                else :
                    print(request.FILES,"====================>")
                    print("---------------------",request.data,request.thisUser)
                    request.data["user"]  = request.thisUser.id
                    campaign_serializer = CampaignSerializer(data=request.data)
                    if campaign_serializer.is_valid(raise_exception=True):
                        campaign = campaign_serializer.save()
                        print("---------------Document saved---------------------")
                        uploaded_docs = request.FILES.getlist("documents")
                        documents_to_create = [Documents(doc_file=item, campaign=campaign) for item in uploaded_docs]
                        Documents.objects.bulk_create(documents_to_create)
                        print("---------------Bank KYC Saving---------------------")
                        request.data["campaign"] = campaign.id
                        bkc_serializer = BankKYCSerializer(data = request.data)
                        bkc_serializer.is_valid(raise_exception=True)
                        bkc_serializer.save()
                        print("---------------Bank KYC  Saved ---------------------")
                        return Response({"error" : False, "message" : "Campaign Data Saved Successfully" , "data" : campaign_serializer.data, "id" : campaign.id},status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error" : True , "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)


