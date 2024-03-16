from phonepe.sdk.pg.payments.v1.payment_client import PhonePePaymentClient
from phonepe.sdk.pg.env import Env


merchant_id = "PGTESTPAYUAT"  
salt_key = "099eb0cd-02cf-4e2a-8aca-3e6c6aff0399"  
salt_index = 1 
env = Env.UAT # Change to Env.PROD when you go live


# instanace of phone pay client class
phonepe_client = PhonePePaymentClient(merchant_id=merchant_id, salt_key=salt_key, salt_index=salt_index, env=env)


# initaite transaction 
import uuid  
from phonepe.sdk.pg.payments.v1.models.request.pg_pay_request import PgPayRequest
from rest_framework.response import Response
# class PaymentApi(APIView):
def payment(request):
        unique_transaction_id = str(uuid.uuid4())[:-2]
        ui_redirect_url = "https://www.merchant.com/redirectPage"  
        s2s_callback_url = "https://www.merchant.com/callback"  
        amount = 1000 
        id_assigned_to_user_by_merchant = 'MUID123'  
        pay_page_request = PgPayRequest.pay_page_pay_request_builder(merchant_transaction_id=unique_transaction_id,  
                                                                amount=amount,  
                                                                merchant_user_id=id_assigned_to_user_by_merchant,  
                                                                callback_url=s2s_callback_url,
                                                                redirect_url=ui_redirect_url) 
        
        pay_page_response = phonepe_client.pay(pay_page_request)
        
        pay_page_url = pay_page_response.data.instrument_response.redirect_info.url
        # return Response({"error" : False})
    

    
    
    
# unique_transaction_id = str(uuid.uuid4())[:-2]
# ui_redirect_url = "https://www.merchant.com/redirectPage"  
# s2s_callback_url = "https://www.merchant.com/callback"  
# amount = 1000 
# id_assigned_to_user_by_merchant = 'MUID123'  
# pay_page_request = PgPayRequest.pay_page_pay_request_builder(merchant_transaction_id=unique_transaction_id,  
#                                                              amount=amount,  
#                                                              merchant_user_id=id_assigned_to_user_by_merchant,  
#                                                              callback_url=s2s_callback_url,
#                                                             redirect_url=ui_redirect_url) 
# pay_page_response = phonepe_client.pay(pay_page_request) 

# pay_page_url = pay_page_response.data.instrument_response.redirect_info.url

# print("pay page response",pay_page_response)

# # View the state for the transaction we just initiated.
# unique_transaction_id = unique_transaction_id 
# transaction_status_response = phonepe_client.check_status(merchant_transaction_id=unique_transaction_id)  
# transaction_state = transaction_status_response.data.state
# print("transaction status",transaction_status_response)
# print("transaction state",transaction_state)


# # Check the validity of callback
# x_verify_header_data = "a005532637c6a6e4a4b08ebc6f1144384353305a9cd253d995067964427cd0bb###1"

# phonepe_s2s_callback_response_body_string = '{"response": "eyJzdWNjZXNzIjpmYWxzZSwiY29kZSI6IlBBWU1FTlRfRVJST1IiLCJtZXNzYWdlIjoiUGF5bWVudCBGYWlsZWQiLCJkYXRhIjp7Im1lcmNoYW50SWQiOiJtZXJjaGFudElkIiwibWVyY2hhbnRUcmFuc2FjdGlvbklkIjoibWVyY2hhbnRUcmFuc2FjdGlvbklkIiwidHJhbnNhY3Rpb25JZCI6IkZUWDIzMDYwMTE1NDMxOTU3MTYzMjM5IiwiYW1vdW50IjoxMDAsInN0YXRlIjoiRkFJTEVEIiwicmVzcG9uc2VDb2RlIjoiUkVRVUVTVF9ERUNMSU5FX0JZX1JFUVVFU1RFRSIsInBheW1lbnRJbnN0cnVtZW50IjpudWxsfX0="}'

# is_valid = phonepe_client.verify_response(x_verify=x_verify_header_data,  
#                                           response=phonepe_s2s_callback_response_body_string)


# print("checking validity of callabck",is_valid)

# Refund Transaction 
# import uuid

# unique_transcation_id = str(uuid.uuid4())[:-2]
# original_transaction_id = "MERCHANT_TRANSACTION_YOU_WANT_TO_REFUND"  
# amount = 100   
# # //refund amount <= pay amount  
# s2s_callback_url = "https://www.merchant.com/callback"  
# refund_response = phonepe_client.refund(merchant_transaction_id=unique_transcation_id,  
#                                         original_transaction_id=original_transaction_id,  
#                                         amount=amount,  
#                                         callback_url=s2s_callback_url)  

# response_code = refund_response.data.response_code


# {
#     "keyIndex": 1,
#     "key": "fe43ebc9-626b-4dc3-8d4f-fa28b20846b9"
# }
# Merchant ID : FAIRSEEDONLINE
# Merchant USer ID : --------------
