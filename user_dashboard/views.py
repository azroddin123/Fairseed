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
        fundraise_data = Campaign.objects.filter(donors__created_on__range=(start_date,end_date),user=request.thisUser).values('donors__created_on').annotate(
        donation_count=Count('id')
        ).order_by('donors__created_on')

        for item in fundraise_data:
            print(item)
        date_list = [start_date + timedelta(days=x) for x in range(31)]
        result = [
                {"date": date.date(), "donation_count": next((item["donation_count"] for item in fundraise_data if item["donors__created_on"] == date.date()), 0)}
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
        for item in fundraise_data :
            print(item)

        date_list = [start_date + timedelta(days=x) for x in range(31)]
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


class CauseEditAPi(GenericMethodsMixin,APIView):
    def put(self,request,pk,*args,**Kwargs):
        try :
            campaign       = Campaign.objects.get(id=pk)
            # Extracting images 
            campaign_image = request.FILES.get('campaign_image')
            uploaded_docs  = request.FILES.getlist("documents")
            
            if len(request.FILES) == 0:
                print("changes_sent")
                CauseEdit.objects.create(campaign=campaign,campaign_data=request.data,approval_status="Pending")
                return Response({"error" : False , "message" : "Your changes have been recorded for this campaign and are sent for approval to the admin"},status=status.HTTP_200_OK)
            else :
                if campaign_image and uploaded_docs:
                    request.data.pop('campaign_image')
                    request.data.pop('documents')
                    doc1, doc2, doc3 = None, None, None
                    if len(uploaded_docs) == 1 :
                        doc1 = uploaded_docs[0]
                    elif len(uploaded_docs) == 2 :
                        print("In Uploaded Docs 2 ")
                        doc1 = uploaded_docs[0]
                        doc2 = uploaded_docs[1]
                    elif len(uploaded_docs) == 3:
                        doc1 = uploaded_docs[0]
                        doc2 = uploaded_docs[1]
                        doc3 = uploaded_docs[2]
                    print("object created")
                    CauseEdit.objects.create(campaign=campaign,campaign_data=request.data,campaign_image=campaign_image,doc1=doc1,doc2=doc2,doc3=doc3,approval_status="Pending")
                elif campaign_image and len(uploaded_docs) == 0 :
                    request.data.pop('campaign_image')
                    CauseEdit.objects.create(campaign=campaign,campaign_data=request.data,campaign_image=campaign_image,approval_status="Pending")
                elif uploaded_docs and campaign_image is None:
                    doc1, doc2, doc3 = None, None, None
                    request.data.pop('documents')
                    CauseEdit.objects.create(campaign=campaign,campaign_data=request.data,doc1=doc1,doc2=doc2,doc3=doc3,approval_status="Pending")
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
    
    # def put(self,request,pk,*args, **kwargs):
    #     try :
    #         campaign = BankKYC.objects.get(id=pk)
    #         campaign.campaign_data = request.data
    #         campaign.approval_status = "Pending"
    #         campaign.save()
    #         return Response({"error" : False , "message" : "Your changes have been recorded for this campaign and are sent for approval to the admin"},status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response({"error" : True , "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)

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

    # def put(self,request,pk,*args, **kwargs):
    #     try :
    #         kyc = BankKYC.objects.get(campaign=pk)
    #         if len(request.FILES) == 0:
    #             print("changes_sent")
    #             BankKYCEdit.objects.create(bank_kyc=kyc,bank_data=request.data,approval_status="Pending")
    #             return Response({"error" : False , "message" : " Your changes has been recorded and are  sent for approval to Admin "},status=status.HTTP_200_OK)
    #         else :
    #             adhar    = request.FILES.get('adhar_card_image')
    #             pan      = request.FILES.get('pan_card_image')
    #             passbook = request.FILES.get('passbook_image')
    #             if adhar and passbook and pan:
    #                 request.data.pop["adhar_card_image"]
    #                 request.data.pop["pan_card_image"]
    #                 request.data.pop["passbook_image"]
    #                 BankKYCEdit.objects.create(bankkyc=kyc,bank_data=request.data,adhar_image=adhar,pan_image=pan,passbook_image=passbook,approval_status="Pending")
    #             elif adhar and  pan and passbook is None :
    #                 pass
                    
            

    #         kyc.bank_data = request.data
    #         kyc.approval_status = "Pending"
    #         kyc.save()
    #         return Response({"error" : False , "message" : " Your changes has been recorded and are  sent for approval to Admin "},status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response({"error" : True , "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)


