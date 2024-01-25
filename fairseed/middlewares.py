from django.conf import settings
from django.http import JsonResponse
from rest_framework import status
import jwt
from accounts.models import * 

class CustomAuthentication:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        if request.path.startswith("/admin/") or request.path.endswith("nt/")  or request.path.startswith("/api/token/"):
            request.thisUser = None
            response = self.get_response(request)
            return response
        token = request.headers.get('x-access-token')
        if not token:
           return JsonResponse({"Error" :"Credentials Not Found ..Please Login"},status=status.HTTP_403_FORBIDDEN)
        payload = jwt.decode(token,settings.SECRET_KEY,algorithms=['HS256']) #this key is used for both create and verify
        print(payload)
        # user = User.objects.filter(email=payload["email"]).first()
        user = User.objects.filter(id=payload["user_id"]).first()
        request.thisUser = user
        response = self.get_response(request)
        return response
    

# class AuthMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         token = request.headers.get("x-access-token")
#         # if request.path.startswith('/admin/') or (any(["/accounts/user/", "/accounts/login/"]) in request.path):
#         if request.path.startswith('/admin/') or request.path.endswith("/accounts/user/") or request.path.endswith("/accounts/login/") or request.path.endswith("/tenants/user/") or request.path.endswith("/tenants/tenant/") or request.path.startswith('/static/media_files/'):
#             # /tenants/user/
#             response = self.get_response(request)
#             return response
#         if not token:
#             return JsonResponse(data={"msg": "Token not provided"}, status=HTTP_403_FORBIDDEN)
#         try:
#             decoded_jwt = jwt.decode(token, env(
#                 "JWT_SECRET"), algorithms=["HS256"])
#             request.thisUser = User.objects.get(
#                 uuid=UUID(decoded_jwt["uuid"]).hex)
#             response = self.get_response(request)
#             return response
#         except (jwt.exceptions.InvalidSignatureError, User.DoesNotExist):
#             return JsonResponse(data={"msg": "Invalid token"}, status=HTTP_401_UNAUTHORIZED)

