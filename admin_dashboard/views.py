import openpyxl
from .serializers import *
from accounts.serializers import * 
from .models import *
from campaigns.models import *
from donors.models import *
from donors.serializers import * 
from django.utils import timezone
from rest_framework.views import APIView
from portals.GM2 import GenericMethodsMixin
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from campaigns.serializers import * 
from django.db import transaction
from openpyxl import Workbook
from django.http import HttpResponse
from campaigns.models import send_email_on_model_creation_or_update
from django.db.models import Count
from portals.services import paginate_model_data,paginate_data
class PagesAPi(GenericMethodsMixin,APIView):
    model = Pages
    serializer_class = PageSerializer
    lookup_field = "id"


class PagesSlugApi(APIView):
    def get(self,request,slug=None):
        try : 
            data = Pages.objects.get(slug=slug)
            serializer = PageSerializer(data)
            return Response({ "error" : False ,"data" : serializer.data},status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error" : True, "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)

class GeneralSettingApi(GenericMethodsMixin,APIView):
    model = GeneralSetting
    serializer_class = GSSerializer
    lookup_field = "id"

class KeywordSApi(GenericMethodsMixin,APIView):
    model = Keyword
    serializer_class = KeywordSerializer
    lookup_field = "id"

class LimitApi(GenericMethodsMixin,APIView):
    model = Limit
    serializer_class = LimitSerializer
    lookup_field = "id"

class SocialProfileApi(GenericMethodsMixin,APIView):
    model = SocialProfile
    serializer_class = SocialProfileSerializer
    lookup_field = "id"

class LandingPageSettingApi(GenericMethodsMixin,APIView):
    model = LandingPage
    serializer_class = LandingPageSerializer
    lookup_field = "id"

class AdminDashboardApi(APIView):
    def get(self,request,*args, **kwargs):
        try :     
            data = {
                    "no_of_donation" : Donor.objects.count(),
                    "total_campaign" : Campaign.objects.count(),
                    "fund_raised" : Campaign.objects.filter().aggregate(Sum('fund_raised'))['fund_raised__sum'] or 0,
                    "user" : User.objects.filter().count()
                }
            return Response({"data" : data},status=status.HTTP_200_OK)  
        except Exception as e :
                return Response({"error" : True, "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)                  

class AdminDonationApi(APIView):
    def get(self,request,*args, **kwargs):
        try : 
            end_date = timezone.now()
            start_date = end_date - timedelta(days=30)
            fundraiser_data = Campaign.objects.filter(donors__created_on__range=(start_date,end_date)).values('donors__created_on').annotate(
            total_amount=Sum('donors__amount')
            ).order_by('donors__created_on')
            date_list = [start_date + timedelta(days=x) for x in range(30)]
            result = [
                    {"date": date.date(), "total_amount": next((item["total_amount"] for item in fundraiser_data if item["donors__created_on"] == date.date()), 0)}
                    for date in date_list
                ]
            return Response({"fundraiser_data" : result },status=status.HTTP_200_OK)
        except Exception as e :
                return Response({"error" : True, "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)

class AdminCountryApi(APIView):
    def get(self,request,*args, **kwargs):
        user_data =  [
        {
            "country": "India",
            "user_count": 4
        },
        {
            "country": "Australia",
            "user_count": 3
        }]
        country_user_count = User.objects.values('country').annotate(user_count=Count('id'))
        return Response({"error" : False, "user_data" :user_data },status=status.HTTP_200_OK)

class UserUpdateApi(APIView):
    def put(self,request,pk,*args, **kwargs):
        try : 
            user = User.objects.get(id=pk)
            serializer  = UserSerializer1(user,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"error" : False , "data" : serializer.data},status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error" : True, "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)
            
class CampaignKycAPI(GenericMethodsMixin,APIView):
    model = BankKYC
    serializer_class = CampBankKycSerializer
    lookup_field = "id"

    def put(self,request,pk,*args, **kwargs):
        try :
            data = request.data
            print(type(data),"data")
            print("data",request.data)
            with transaction.atomic():
                bankkyc = BankKYC.objects.get(id=pk)
                request.POST._mutable = True
                data.update(bankkyc.bank_data)
                print(data,"new data",bankkyc.bank_data)
                print("data",type(bankkyc.bank_data))
                if request.data['approve_kyc'] == 'true' : 
                    serializer = BankKYCSerializer(bankkyc,data=data,partial=True)
                    print("request.data",request.data,bankkyc.bank_data)
                    if serializer.is_valid(raise_exception=True) :
                        print("new bankkyc Data Approved ")
                        serializer.save()
                        # serializer1.save()
                        bankkyc.bank_data = {}
                        print("Approval Status Approved ",bankkyc.bank_data,bankkyc.approval_status)
                        bankkyc.approval_status="Approved"
                        bankkyc.save()
                    return Response({"error" : False , "data" : "Bank Kyc  Update Request Approved Successfully" ,"data1" : serializer.data},status=status.HTTP_200_OK)
                else :
                    bankkyc.bank_data = {}
                    bankkyc.approval_status="Rejected"
                    bankkyc.save()
                    return Response({"error" : False , "data" : "Bank KYC Update Request Rejected Successfully"},status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error" : True, "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)

class DonorsApi(GenericMethodsMixin,APIView):
    model = Donor
    serializer_class = DonorSerializer
    lookup_field = "id"

    def put(self,request,pk,*args, **kwargs):
        try : 
            donor = Donor.objects.get(id=pk)
            serializer  = DonorSerializer(donor,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"error" : False , "data" : serializer.data , "message" : "Donor Updated Successfully"},status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error" : True, "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)
           

class  CampaigncategoryApi2(GenericMethodsMixin,APIView):
    model = Campaigncategory
    serializer_class = CampaignCategorySerializer
    lookup_field = "id"
    
class RevisionHistoryApi(APIView):
    def get(self,request,pk,*args, **kwargs):
        try :
            data = RevisionHistory.objects.filter(campaign=pk)
            response = paginate_data(model=RevisionHistory,serializer=RHSerializer,request=request,data=data)
            return Response(response,status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error" : True, "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)
            
            
class UserApi2(GenericMethodsMixin,APIView):
    model = User
    serializer_class = UserAdminSerializer1
    create_serializer_class = UserSerializer2
    lookup_field  = "id"

    def post(self,request,*args, **kwargs):
        try : 
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"error" : False ,"message" : "User Created Successfully"},status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            return Response({"error" : True , "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request,pk,*args, **kwargs):
        try : 
            user = User.objects.get(id=pk)
            password = request.data.get('password')
            if password:
                user.set_password(password)
                print("password updated")
            serializer = UserSerializer2(user,data=request.data,partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"error" : False ,"message" : "User Updated Successfully"},status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            return Response({"error" : True , "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)
        

class CampaignAdminApi2(GenericMethodsMixin,APIView):
    model = Campaign
    serializer_class = CampaignDocumentSerializer
    create_serializer_class = CampaignSerializer
    lookup_field  = "id"

    def put(self, request, pk, *args, **kwargs):
        try:
            with transaction.atomic():
                filter = {self.lookup_field: pk}
                object_instance = self.model.objects.get(**filter)

                # Keep the original creator (user) from the object instance
                original_user = object_instance.user

                print("---------------------", request.data, request.thisUser)
                request_data = request.data.copy()

                # Ensure the original creator remains the same
                # You can skip setting 'user' from request.thisUser if you don't want to change it
                request_data["user"] = original_user.id

                # Partial update with existing data
                campaign_serializer = CampaignSerializer(object_instance, data=request_data, partial=True)
                if campaign_serializer.is_valid(raise_exception=True):
                    campaign = campaign_serializer.save()

                    print("---------------Document saved---------------------")
                    uploaded_docs = request.FILES.getlist("documents")
                    print("--------------------docs-------------", uploaded_docs)

                    documents_to_create = [Documents(doc_file=item, campaign=campaign) for item in uploaded_docs]
                    Documents.objects.bulk_create(documents_to_create)

                    return Response({
                        "error": False,
                        "message": "Campaign Documents Saved Successfully",
                        "data": campaign_serializer.data,
                        "id": campaign.id
                    }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "error": True,
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class CampaignEditApproval(GenericMethodsMixin,APIView):
    model = Campaign
    serializer_class = CampaignSerializer
    lookup_field="id"
    
    def get(self,request,pk=None,*args, **kwargs):
        try :
            if pk==None : 
                data = Campaign.objects.filter(approval_status="Pending")
                serializer = CampaignDocumentSerializer(data,many=True)
                response = paginate_data(model=Campaign,serializer=CampaignDocumentSerializer,request=request,data=data)
                return Response(response,status=status.HTTP_200_OK)            
            data = Campaign.objects.get(id=pk,approval_status="Pending")
            serializer = CampaignDocumentSerializer(data)
            return Response({"error" : False , "data" : serializer.data},status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error" : True, "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)
      
    def put(self,request,pk,*args, **kwargs):
        try :
            print("=================admin========",request.data)
            with transaction.atomic():
                campaign = Campaign.objects.get(id=pk)
                if request.data['approve_campaign'] == "true" :
                    serializer = CampaignSerializer(campaign,data=campaign.campaign_data,partial=True)
                    campaign.campaign_data['approval_status'] = "Approved"
                    if serializer.is_valid():
                        print("new campaign Data Approved ")
                        serializer.save()
                        campaign.campaign_data = {}
                        print("Approval Status Approved ",campaign.campaign_data,campaign.approval_status)
                        campaign.approval_status="Approved"
                        campaign.is_admin_approved = True
                        campaign.save()
                        # RevisionHistory.objects.create(modified_by=request.thisUser,campaign=campaign,campaign_data=campaign)
                    return Response({"error" : False , "data" : "Campaign Update Request Approved Successfully"},status=status.HTTP_202_ACCEPTED)
                else :
                    campaign.campaign_data = {}
                    campaign.approval_status="Rejected"
                    campaign.save()
                    # RevisionHistory.objects.create(modified_by=request.thisUser,campaign=campaign.id,campaign_data=campaign)
                    return Response({"error" : False , "data" : "Campaign Update Request Rejected Successfully"},status=status.HTTP_202_ACCEPTED)
        except Exception as e :
            return Response({"error" : True, "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)

class DocumentAPI(GenericMethodsMixin,APIView):
    model = Documents
    serializer_class = DocumentSerializer
    lookup_field = "id"


class WithdrawalApi(GenericMethodsMixin,APIView):
    model = Withdrawal
    serializer_class = WithDrawalSerializer
    lookup_field = "id"

    def get(self,request,pk=None,*args,**kwargs):
        try :
            if pk==None : 
                data = Withdrawal.objects.all()
                response = paginate_data(model=Withdrawal,serializer=WithDrawalSerializer,request=request,data=data)
                return Response(response,status=status.HTTP_200_OK)
            data = Withdrawal.objects.get(id=pk)
            bank_data = BankKYC.objects.get(campaign=data.campaign)
            serializer1 = BankKYCSerializer(bank_data)
            serializer = WithdrawalSerializer1(data)
            return Response({"error" : False , "campaign_data" : serializer.data,"bank_data" : serializer1.data},status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error" : True, "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)

class DonationGraphAPI(APIView):
    def get(self,request):
        try : 
            end_date = timezone.now()
            start_date = end_date - timedelta(days=30)
            fundraiser_data = Campaign.objects.filter(donors__created_on__range=(start_date,end_date)).values('donors__created_on').annotate(
            donation_count=Count('id')
            ).order_by('donors__created_on')

            for item in fundraiser_data:
                print(item)
            date_list = [start_date + timedelta(days=x) for x in range(31)]
            result = [
                    {"date": date.date(), "donation_count": next((item["donation_count"] for item in fundraiser_data if item["donors__created_on"] == date.date()), 0)}
                    for date in date_list
                ]
            return Response({"donation_data" : result },status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error" : True, "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)



class CausEditApi(GenericMethodsMixin,APIView):
    model = CauseEdit
    serializer_class = CauseEditSerializer1
    lookup_field = "id"

    def get(self,request,pk=None,*args,**kwargs):
        if pk is None :
            data = CauseEdit.objects.filter(approval_status="Pending")
            response = paginate_data(model=CauseEdit,serializer=CauseEditSerializer1,request=request,data=data)
            return Response(response,status=status.HTTP_200_OK)
    
        cause_edit = CauseEdit.objects.get(id=pk)
        serializer = CauseEditSerializer1(cause_edit)
        return Response({"error" : False , "data" : serializer.data},status=status.HTTP_200_OK)

    def put(self,request,pk,*args,**kwargs):
        try :
            print("request_data",request.data)
            with transaction.atomic():
                cause_edit = CauseEdit.objects.get(id=pk,approval_status="Pending")
                print("cause_edit",cause_edit.campaign_data)
                if request.data['approve_campaign'] == "true" :
                    campaign = Campaign.objects.get(id=cause_edit.campaign.id)
                    serializer = CampaignSerializer(campaign,data=cause_edit.campaign_data,partial=True)
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                    print("cause_edit",cause_edit.campaign_image)
                    if cause_edit.campaign_image is not None and cause_edit.campaign_image != '':
                        print("in if part")
                        campaign.campaign_image = cause_edit.campaign_image
                        campaign.save()
                    docs = []
                    for doc_field_name in ["doc1", "doc2", "doc3"]:
                        doc_value = getattr(cause_edit, doc_field_name)
                        if doc_value:
                            docs.append(doc_value)
                    if docs :
                            Documents.objects.filter(campaign=campaign).delete()
                            documents_to_create = [Documents(doc_file=item, campaign=campaign) for item in docs]
                            Documents.objects.bulk_create(documents_to_create)
                    cause_edit.approval_status = "Approved"
                    cause_edit.save()
                    RevisionHistory.objects.create(modified_by=request.thisUser,campaign=campaign,cause_data=cause_edit)
                    return Response({"error" : True, "message" : "Campaign Approved Successfully"},status=status.HTTP_200_OK)
                else :
                    cause_edit.approval_status = "Rejected"
                    campaign = Campaign.objects.get(id=cause_edit.campaign.id)
                    cause_edit.save()
                    RevisionHistory.objects.create(modified_by=request.thisUser,campaign=campaign,cause_data=cause_edit)
                    return Response({"error" : True, "message" : "Campaign Rejected Successfully Successfully"},status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error" : True, "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)


class BankKycEditApi(GenericMethodsMixin,APIView):
    model = BankKYCEdit
    serializer_class = BankKYCEditSerializer
    lookup_field = "id"

    def get(self,request,pk=None,*args,**kwargs):
        try : 
            if pk is None :
                data = BankKYCEdit.objects.filter(approval_status="Pending")
                response = paginate_data(BankKYCEdit,BankKYCEditSerializer,request=request,data=data)
                return Response(response,status=status.HTTP_200_OK)
        
            bank_edit = BankKYCEdit.objects.get(id=pk)
            serializer = BankKYCEditSerializer(bank_edit)
            return Response({"error" : False , "data" : serializer.data},status=status.HTTP_200_OK)
        except Exception as e :
                return Response({"error" : True, "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk,*args,**kwargs):
        try :
            print("request_data",request.data)
            with transaction.atomic():
                bank_edit = BankKYCEdit.objects.get(id=pk,approval_status="Pending")
                if request.data['approve_kyc'] == "true" :
                    print("In Approve KYC")
                    bank_kyc = BankKYC.objects.get(id=bank_edit.bank_kyc.id)
                    serializer = BankKYCEditSerializer(bank_kyc,data=bank_edit.bank_data,partial=True)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                   
                    if bank_edit.adhar_card_image :
                        bank_kyc.adhar_card_image = bank_edit.adhar_card_image
                    if bank_edit.pan_card_image :
                        bank_kyc.pan_card_image = bank_edit.pan_card_image
                    if bank_edit.passbook_image :
                        bank_kyc.passbook_image = bank_edit.passbook_image
                    bank_kyc.status="Approved"
                    bank_edit.approval_status = "Approved"
                    bank_kyc.save()
                    return Response({"error" : True, "message" : "Kyc Request Approved Successfully"},status=status.HTTP_200_OK)
                else :
                    bank_edit.approval_status = "Rejected"
                    bank_kyc.status="Rejected"
                    bank_edit.save()
                    return Response({"error" : True, "message" : "Kyc Request Rejected Successfully"},status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error" : True, "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)


class ReportedCauseAPI(GenericMethodsMixin,APIView):
    model = ReportedCampaign
    serializer_class = ReportedCampaignSerializer
    lookup_field = "id"

    def put(self,request,pk,*args,**kwargs):
        try : 
            print("pk",pk)
            rc = ReportedCampaign.objects.get(id=pk)
            campaign = Campaign.objects.get(id=rc.campaign.id)
            campaign.status = "Rejected"
            campaign.save()
            rc.delete()
            return Response({"error" : True, "message" : "Campaign Status Rejected Successfully"},status=status.HTTP_200_OK)
        except Exception as e :
                return Response({"error" : True, "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)
        



class ExportToCSV(APIView):
       def get(self, request, *args, **kwargs):
        data = Campaign.objects.all()

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=campaign_data.xlsx'

        workbook = Workbook()
        worksheet = workbook.active

        worksheet.append(['title', 'username', 'mobile_no', 'goal_amount', 'fund_raised', 'status', 'end_date'])

        for obj in data:
            row = [obj.title, obj.user.username if obj.user else None, obj.user.mobile_number if obj.user else None,
                   obj.goal_amount, obj.fund_raised, obj.status, obj.end_date]
            worksheet.append(row)

        workbook.save(response)
        return response
       


class GenericSearchAPI(APIView):
    pass

class ExportExcelView(APIView):
    def get(self, request, *args, **kwargs):
        # Create a workbook and a worksheet
        workbook = openpyxl.Workbook()
        worksheet = workbook.active
        worksheet.title = 'Donor Data'

        # Write the header
        headers = ['campaign', 'user','donation_type','full_name','amount','email','city','country','mobile','pancard',
                   'comment','payment_type','is_anonymous','status','is_approved','transaction_id','bank_name',
                   'transaction_date','other_details','date']
        worksheet.append(headers)

        # Write data
        queryset = Donor.objects.all()

        for obj in queryset:
            row = [obj.campaign.title, obj.user.username if obj.user else None, obj.donation_type,obj.full_name,obj.amount,
                   obj.email, obj.city, obj.country, obj.mobile,
                   obj.pancard, obj.comment, obj.payment_type, obj.is_anonymous,
                   obj.status, obj.is_approved, obj.transaction_id, obj.bank_name,
                   obj.transaction_date, obj.other_details, obj.date]
            worksheet.append(row)
        

        # Create an HTTP response with the Excel file
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="donor_data.xlsx"'

        # Save the workbook to the response
        workbook.save(response)

        return response