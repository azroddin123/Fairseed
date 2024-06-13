from django.shortcuts import render
import uuid
import requests
# Create your views here.
from .serializers import * 
from .models import (
    Donor,
)

from portals.services import donation_email
from rest_framework.views import APIView
from portals.GM2 import GenericMethodsMixin
from rest_framework import status
from rest_framework.response import Response
from phonepe.sdk.pg.payments.v1.payment_client import PhonePePaymentClient
from phonepe.sdk.pg.env import Env
from phonepe.sdk.pg.payments.v1.models.request.pg_pay_request import PgPayRequest
from django.db import transaction
from portals.email_utility import send_email_async


class DonatePaymentApi(APIView):
    def post(self,request):
        # check donation type of request 
        try:
            print(request.data,"--------------------------------->")
            with transaction.atomic() : 
                print("===========================",request.data)
                data = request.data
                payment_type = request.data.get('payment_type')
                if payment_type == "UPI" :
                    # merchant_id = "PGTESTPAYUAT100"  
                    # salt_key = "cc2f75ad-01c2-4417-92f8-32964ce8d12d"  
                    # salt_index = 1 
                    # env = Env.UAT 
                    
                    merchant_id = "FAIRSEEDONLINE"   
                    salt_key = "fe43ebc9-626b-4dc3-8d4f-fa28b20846b9"    
                    salt_index = 1 
                    env = Env.PROD 

                    phonepe_client = PhonePePaymentClient(merchant_id=merchant_id, salt_key=salt_key, salt_index=salt_index, env=env)
                    unique_transaction_id = str(uuid.uuid4())[:-2]
                    ui_redirect_url = "https://staging.fairseed.org"
                    s2s_callback_url = "http://143.110.253.227:8000/donors/check-status/"+unique_transaction_id
                    # s2s_callback_url = "http://0.0.0.0:8000/donors/check-status/"+unique_transaction_id
                    try:
                        amount = int(request.data.get('amount', 0)) * 100
                    except ValueError:
                        return Response({'error': True, 'message': 'Invalid amount value'}, status=status.HTTP_400_BAD_REQUEST)
                    # amount = int(request.data.get('amount'))*100
                    id_assigned_to_user_by_merchant = "PGTESTPAYUAT100"
                    pay_page_request = PgPayRequest.pay_page_pay_request_builder(
                        merchant_transaction_id=unique_transaction_id,
                        amount=amount,
                        merchant_user_id=id_assigned_to_user_by_merchant,
                        callback_url=s2s_callback_url,
                        redirect_url=ui_redirect_url,
                    )
                    pay_page_response = phonepe_client.pay(pay_page_request)
                    pay_page_url = pay_page_response.data.instrument_response.redirect_info.url
                    request.POST._mutable = True
                    data['transaction_id'] = unique_transaction_id
                    data['status'] = "Approved"
                    data["is_approved"] = True
                    serializer = DonorSerializer2(data=request.data)
                    if serializer.is_valid(raise_exception=True):
                        donor = serializer.save()
                        if donor.email : 
                            subject = "Donation Email"
                            msg = "Your Donation Has been done successfully of amount ".format(amount)
                            print(donor.email,"--------------",donor.amount)
                            send_email_async(subject,msg,[donor.email])
                            # res = donation_email(donor.email,donor.amount)
                    return Response({'pay_page_url': pay_page_url , "data" : serializer.data,"transaction_id" : unique_transaction_id}, status=201)
                else :
                    print(type(amount))
                    try:
                        amount = int(request.data.get('amount', 0))  # Ensure amount is parsed for non-UPI case
                    except ValueError:
                        return Response({'error': True, 'message': 'Invalid amount value'}, status=status.HTTP_400_BAD_REQUEST)
                    
                    serializer = DonorSerializer2(data=request.data)
                    if serializer.is_valid(raise_exception=True):
                        donor = serializer.save()
                        # if donor.email: 
                        #     subject = "Donation Email"
                        #     msg = "Your Donation Has been done successfully of amount {}".format(donor.amount)
                        #     print(donor.email, "--------------", donor.amount)
                        #     send_email_async(subject, msg, [donor.email])
                    return Response({"error":False,"data" : serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': True, "message" : str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class CheckPaymentStatusAPi(APIView):
    def get(self,request,pk=None,):
        try :
            merchant_id = "FAIRSEEDONLINE"  
            salt_key = "fe43ebc9-626b-4dc3-8d4f-fa28b20846b9"  
            salt_index = 1 
            env = Env.PROD 
            phonepe_client = PhonePePaymentClient(merchant_id=merchant_id, salt_key=salt_key, salt_index=salt_index, env=env)
            print("pk",pk)
            unique_transaction_id = pk
            transaction_status_response = phonepe_client.check_status(merchant_transaction_id=unique_transaction_id)  
            transaction_state = transaction_status_response.data.state
            current_status = { 
                "status" : transaction_status_response.code,
                "message" : transaction_status_response.message,
                "transaction_State" : transaction_status_response.data.state

            }
            return Response({"transaction_status" : current_status},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DonorApi(GenericMethodsMixin,APIView):
    model = Donor
    serializer_class = DonorSerializer
    lookup_field = "id"

