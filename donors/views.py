from datetime import timezone
import threading
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.urls import reverse

import logging

logger = logging.getLogger(__name__)

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
from django.conf import settings


class DonatePaymentApi(APIView):
    def post(self,request):
        # check donation type of request 
        try:
            print(request.data,"--------------------------------->")
            with transaction.atomic() : 
                print("===========================",request.data)
                data = request.data
                payment_type = request.data.get('payment_type')
                print("========================>",payment_type)
                if payment_type == "UPI" :
                    print("in if part") 
                    
                    merchant_id = settings.PROD_MERCHANT_ID
                    salt_key = settings.PROD_SALT_KEY   
                    salt_index = settings.PROD_SALT_INDEX
                    env = Env.PROD 
                    # env = Env.UAT 

                    phonepe_client = PhonePePaymentClient(merchant_id=merchant_id, salt_key=salt_key, salt_index=salt_index, env=env)
                    unique_transaction_id = str(uuid.uuid4())[:-2]
                    ui_redirect_url  = settings.REDIRECT_URL
                    s2s_callback_url = settings.REDIRECT_URL
                    # s2s_callback_url = request.build_absolute_uri(reverse('donors:payment_callback'))
                    print(s2s_callback_url)
                    # s2s_callback_url = "http://0.0.0.0:8000/donors/check-status/"+unique_transaction_id
                    try:
                        amount = int(request.data.get('amount', 0)) 
                    except ValueError:
                        return Response({'error': True, 'message': 'Invalid amount value'}, status=status.HTTP_400_BAD_REQUEST)
                    # amount = int(request.data.get('amount'))*100
                    id_assigned_to_user_by_merchant = settings.PROD_MERCHANT_ID
                    pay_page_request = PgPayRequest.pay_page_pay_request_builder(
                        merchant_transaction_id=unique_transaction_id,
                        amount=amount* 100,
                        merchant_user_id=id_assigned_to_user_by_merchant,
                        callback_url=s2s_callback_url,
                        redirect_url=ui_redirect_url,
                    )
                    pay_page_response = phonepe_client.pay(pay_page_request)
                    pay_page_url = pay_page_response.data.instrument_response.redirect_info.url
                    
                    request.POST._mutable = True
                    # Start payment status checking timer
                    threading.Timer(60, update_transaction, args=[request,unique_transaction_id,amount]).start()
                    
                    data['transaction_id'] = unique_transaction_id
                    data['status'] = "Pending"
                    data["is_approved"] = False
                    
                    serializer = DonorSerializer2(data=request.data)
                    if serializer.is_valid(raise_exception=True):
                        donor = serializer.save()
                    
                    return Response({'pay_page_url': pay_page_url ,"transaction_id" : unique_transaction_id}, status=201)
                else :
                    print("in else part")
                    print("===========================",request.data)
                    amount = int(request.data.get('amount', 0))  # Ensure amount is parsed for non-UPI case
                    request.POST._mutable = True
                    request.data['amount'] = amount
                    print("amount==============>",amount)
                    serializer = DonorSerializer2(data=request.data)
                    if serializer.is_valid(raise_exception=True):
                        print("=================>IN serializer")
                        donor = serializer.save()
                        if donor.email: 
                            subject = "Donation Email"
                            msg = "Your Donation Has been done successfully of amount {}".format(donor.amount)
                            print(donor.email, "--------------", donor.amount)
                            send_email_async(subject, msg, [donor.email])
                    return Response({"error":False,"data" : serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': True, "message" : str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DonateMoneyAPI(APIView):
    def post(self,request,args,**kwargs):
        try:
            # print(request.data,"--------------------------------->")
            # data = request.data
            payment_type = request.data.get('payment_type')
            with transaction.atomic() : 
                if payment_type == "Bank_Transfer" :
                    print("===========================",request.data)
                    amount = int(request.data.get('amount', 0))  # Ensure amount is parsed for non-UPI case
                    serializer = DonorSerializer2(data=request.data)
                    if serializer.is_valid():
                       serializer.save()
                    return Response({"error":False,"data" : serializer.data}, status=status.HTTP_201_CREATED)
                else :
                    data = request.data
                    merchant_id = settings.PROD_MERCHANT_ID
                    salt_key = settings.PROD_SALT_KEY   
                    salt_index = settings.PROD_SALT_INDEX
                    env = Env.PROD 

                    phonepe_client = PhonePePaymentClient(merchant_id=merchant_id, salt_key=salt_key, salt_index=salt_index, env=env)
                    unique_transaction_id = str(uuid.uuid4())[:-2]
                    ui_redirect_url  = settings.REDIRECT_URL
                    s2s_callback_url = settings.REDIRECT_URL
                    # s2s_callback_url = "http://0.0.0.0:8000/donors/check-status/"+unique_transaction_id
                    try:
                        amount = int(request.data.get('amount', 0)) * 100
                    except ValueError:
                        return Response({'error': True, 'message': 'Invalid amount value'}, status=status.HTTP_400_BAD_REQUEST)
                    # amount = int(request.data.get('amount'))*100
                    id_assigned_to_user_by_merchant = settings.PROD_MERCHANT_ID
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
        except Exception as e:
            return Response({'error': True, "message" : str(e)}, status=status.HTTP_400_BAD_REQUEST)
                
                
                

class CheckPaymentStatusAPi(APIView):
    def get(self,request,pk=None,):
        try :
            merchant_id = settings.PROD_MERCHANT_ID
            salt_key    = settings.PROD_SALT_KEY   
            salt_index  = settings.PROD_SALT_INDEX
            env         = Env.PROD 
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


def update_transaction(unique_transaction_id, amount):
    try:
        donor = Donor.objects.get(transaction_id=unique_transaction_id)

        merchant_id = settings.PROD_MERCHANT_ID
        salt_key = settings.PROD_SALT_KEY
        salt_index = settings.PROD_SALT_INDEX
        env = Env.PROD

        phonepe_client = PhonePePaymentClient(merchant_id=merchant_id, salt_key=salt_key, salt_index=salt_index, env=env)
        response = phonepe_client.check_status(merchant_transaction_id=unique_transaction_id)

        print(response)

        if response.data.state=="COMPLETED":
            donor.status = "Approved"
            donor.is_approved = True
            donor.save()

            if donor.email:
                subject = "Donation Email"
                msg = "Your Donation has been approved successfully for the amount {}".format(amount)
                send_email_async(subject, msg, [donor.email])

            return JsonResponse({"error": "False", 'data': donor})
        elif response.data.state=="PENDING":
            return JsonResponse({"error": "False","message": "Transaction Pending"})
        elif response.data.state=="FAILED":
            donor.status = "Rejected"
            donor.is_approved = False
            donor.save()
            return JsonResponse({"error":"False",'message':"Transaction Failed"})
    except Donor.DoesNotExist:
        return JsonResponse({"error": "Transaction not found"})
    except Exception as e:
        return JsonResponse({"error": str(e)})
    
@csrf_exempt    
def payment_callback(request):
    if request.method == 'POST':
        transaction_id = request.POST.get('transaction_id')
        status = request.POST.get('status')
        # error_message = request.POST.get('error_message', '')
        
        print("Transaction_id======>",transaction_id)
        print("Status============>",status)
        


