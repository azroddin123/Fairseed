# Create your views here.
# from django.shortcuts import render
from django.db.models import Sum,Count
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
from portals.services import paginate_data

# User Dasboard API
class UserDashboardApi(APIView):
    def get(self,request,*args, **kwargs):
        try :
            print(request.thisUser)
            # print(Donor.objects.count(user=request.thisUser))
            data = {
                "no_of_donation" : Donor.objects.filter(user=request.thisUser).count(),
                "total_campaign" : Campaign.objects.filter(user=request.thisUser).count(),
                "amount_received" : Campaign.objects.filter(user=request.thisUser).aggregate(Sum('fund_raised'))['fund_raised__sum'] or 0,
            }
            return Response({"data" : data},status=status.HTTP_200_OK)
        except Exception as e:
                return Response({"error" : True , "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)

# Donation Count API
class DonationCountApi(APIView):
    def get(self,request):
        try :     
            end_date = timezone.now()
            start_date = end_date - timedelta(days=30)
            fundraiser_data = Campaign.objects.filter(donors__created_on__range=(start_date,end_date),user=request.thisUser).values('donors__created_on').annotate(
            donation_count=Count('id')
            ).order_by('donors__created_on')

            for item in fundraiser_data:
                print(item)
            date_list = [start_date + timedelta(days=x) for x in range(31)]
            result = [
                    {"date": date.date(), "donation_count": next((item["donation_count"] for item in fundraiser_data if item["donors__created_on"] == date.date()), 0)}
                    for date in date_list
                ]
            return Response({"donation_data" : result},status=status.HTTP_200_OK)
        except Exception as e:
                return Response({"error" : True , "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)
# FundRaised API
class FundRaisedApi(APIView):
    def get(self,request):
        try : 
            end_date = timezone.now()
            start_date = end_date - timedelta(days=30)
            fundraiser_data = Campaign.objects.filter(donors__created_on__range=(start_date,end_date),user=request.thisUser).values('donors__created_on').annotate(
            total_amount=Sum('donors__amount')
            ).order_by('donors__created_on')
            for item in fundraiser_data :
                print(item)

            date_list = [start_date + timedelta(days=x) for x in range(31)]
            result = [
                    {"date": date.date(), "total_amount": next((item["total_amount"] for item in fundraiser_data if item["donors__created_on"] == date.date()), 0)}
                    for date in date_list
                ]
            return Response({"fundraiser_data" : result },status=status.HTTP_200_OK)
        except Exception as e:
                return Response({"error" : True , "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)   

# Campaign API
class CampaignApi3(GenericMethodsMixin,APIView):
    model = Campaign
    serializer_class = CampaignAdminSerializer
    create_serializer_class = CampaignSerializer
    lookup_field = "id"
    
    def put(self,request,pk,*args,**Kwargs):
            try :
                campaign = Campaign.objects.get(id=pk)
                print(request.data,"----------------->",request.FILES)
            
                # Extracting images 
                campaign_image = request.FILES.get('campaign_image')
                uploaded_docs  = request.FILES.getlist("documents")
   
                print(uploaded_docs,"------doc list-----------")
                if len(request.FILES) == 0:
                    print("changes_sent")
                    CauseEdit.objects.create(campaign=campaign,campaign_data=request.data,approval_status="Pending")
                    return Response({"error" : False , "message" : "Your changes have been recorded for this campaign and are sent for approval to the admin"},status=status.HTTP_200_OK)
            
                else :
                    request.data.pop('campaign_image', None)
                    request.data.pop('documents', None)
                    # Initialize doc variables
                    doc1, doc2, doc3 = None, None, None
                    if uploaded_docs:
                        doc1 = uploaded_docs[0]
                        if len(uploaded_docs) > 1:
                            doc2 = uploaded_docs[1]
                        if len(uploaded_docs) > 2:
                            doc3 = uploaded_docs[2]

                    CauseEdit.objects.create(campaign=campaign,campaign_data=request.data,campaign_image=campaign_image,doc1=doc1,doc2=doc2,doc3=doc3,approval_status="Pending")
                    return Response({"error" : False , "message" : "Your changes have been recorded for this campaign and are sent for approval to the admin"},status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error" : True , "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)


class CauseEditAPi(APIView):
    def put(self,request,pk,*args,**Kwargs):
        try :
            campaign = Campaign.objects.get(id=pk)
            print(request.data,"----------------->")
            # Extracting images 
            campaign_image = request.FILES.get('campaign_image')
            uploaded_docs  = request.FILES.getlist("documents")
            
            if len(request.FILES) == 0:
                print("changes_sent")
                CauseEdit.objects.create(campaign=campaign,campaign_data=request.data,approval_status="Pending")
                return Response({"error" : False , "message" : "Your changes have been recorded for this campaign and are sent for approval to the admin"},status=status.HTTP_200_OK)
          
            else :
                request.data.pop('campaign_image', None)
                request.data.pop('documents', None)
                # Initialize doc variables
                doc1, doc2, doc3 = None, None, None
                if uploaded_docs:
                    doc1 = uploaded_docs[0]
                    if len(uploaded_docs) > 1:
                        doc2 = uploaded_docs[1]
                    if len(uploaded_docs) > 2:
                        doc3 = uploaded_docs[2]

                CauseEdit.objects.create(campaign=campaign,campaign_data=request.data,campaign_image=campaign_image,doc1=doc1,doc2=doc2,doc3=doc3,approval_status="Pending")
                return Response({"error" : False , "message" : "Your changes have been recorded for this campaign and are sent for approval to the admin"},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error" : True , "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)

# Donor API Donation Done By MySelf 
class MyDonationApi(GenericMethodsMixin,APIView):
    model= Donor
    serializer_class = DonorSerializer
    lookup_field = "id"
    
# Received Donation For my Campaign 
class ReceivedDonationApi(APIView):
    def get(self,request,pk=None,*args, **kwargs):
        try : 
            if pk:
                data = Donor.objects.filter(id=pk,campaign__user=request.thisUser)
                response = paginate_data(model=Donor,serializer=DonorSerializer,request=request,data=data)
                return Response(response,status=status.HTTP_200_OK)
            data = Donor.objects.filter(campaign__user=request.thisUser)
            serializer = DonorSerializer(data,many=True)
            response = paginate_data(model=Donor,serializer=DonorSerializer,request=request,data=data)
            return Response(response,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error" : True , "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)

class BankKycApi(GenericMethodsMixin,APIView):
    model = BankKYC
    serializer_class = BankKYCSerializer
    lookup_field = "id"

    def put(self,request,pk,*args, **kwargs):
        try :
            print(request.data,"--------------------")
            kyc = BankKYC.objects.get(campaign=pk)

            if not request.FILES:
                print("changes_sent")
                # No files, create BankKYCEdit object with bank_data and set approval_status to Pending
                BankKYCEdit.objects.create(bank_kyc=kyc, bank_data=request.data, approval_status="Pending")
                return Response({"error": False, "message": "Your changes have been recorded and are sent for approval to Admin"}, status=status.HTTP_200_OK)
            
            # Extract file fields
            file_fields = ['adhar_card_image', 'pan_card_image', 'passbook_image']
            bank_kyc_object = {field: request.FILES.get(field) for field in file_fields}
       
            print(bank_kyc_object)
            for key in bank_kyc_object.keys():
                request.data.pop(key, None)

            BankKYCEdit.objects.create(bank_kyc=kyc,bank_data=request.data,adhar_card_image=bank_kyc_object['adhar_card_image'],pan_card_image=bank_kyc_object['pan_card_image'],passbook_image=bank_kyc_object['passbook_image'],approval_status="Pending")
            return Response({"error" : False , "message" : " Your changes has been recorded and are  sent for approval to Admin "},status=status.HTTP_200_OK)
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

            if not request.FILES:
                print("changes_sent")
                # No files, create BankKYCEdit object with bank_data and set approval_status to Pending
                BankKYCEdit.objects.create(bank_kyc=kyc, bank_data=request.data, approval_status="Pending")
                return Response({"error": False, "message": "Your changes have been recorded and are sent for approval to Admin"}, status=status.HTTP_200_OK)
            
            # Extract file fields
            file_fields = ['adhar_card_image', 'pan_card_image', 'passbook_image']
            bank_kyc_object = {field: request.FILES.get(field) for field in file_fields}
       
            print(bank_kyc_object)
            for key in bank_kyc_object.keys():
                request.data.pop(key, None)

            BankKYCEdit.objects.create(bank_kyc=kyc,bank_data=request.data,adhar_card_image=bank_kyc_object['adhar_card_image'],pan_card_image=bank_kyc_object['pan_card_image'],passbook_image=bank_kyc_object['passbook_image'],approval_status="Pending")
            return Response({"error" : False , "message" : " Your changes has been recorded and are  sent for approval to Admin "},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error" : True , "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)


