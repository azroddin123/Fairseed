from django.conf import settings
from django.http import JsonResponse
from rest_framework import status
import jwt
from accounts.models import User

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
        payload = jwt.decode(token,settings.SECRET_KEY,algorithms=['HS256'])
        user = User.objects.filter(id=payload["id"]).first()
        request.thisUser = user
        response = self.get_response(request)
        return response    
