from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from portals.GM1 import GenericMethodsMixin
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ValidationError
from django.core.mail import send_mail
from django.conf import settings

#########################################################################

class EmailNotificationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = EmailNotificationSerializer(data=request.data)
        if serializer.is_valid():
            subject = serializer.validated_data['subject']
            message = serializer.validated_data['message']
            recipient = serializer.validated_data['recipient']

            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [recipient],
                    fail_silently=False,
                )
                return Response({'message': 'Email sent successfully.'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'message': f'Error sending email: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class RegisterApi(APIView):
    def get(self, request):
        u1 = User.objects.all()
        serializers = UserSerializer1(u1, many = True)
        return Response(serializers.data)


########################################################################
class UserApi(GenericMethodsMixin, APIView):
    model = User
    serializer_class = UserSerializer1
    lookup_field = "id"
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer1(user)
        return Response(serializer.data)

class RegisterUserApi(APIView):
    def post(self,request,*args, **kwargs):
        try : 
            serializer = UserSerializer(data=request.data)
            if  serializer.is_valid():
                serializer.save()
                return Response({"message" : "User Created Succefully" , "data" : serializer.data},status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            raise ValidationError({
                "status_code" : status.HTTP_400_BAD_REQUEST,
                "message" :  e
            })

class ChangePasswordApi(APIView):
    def post(self,request,*args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data,context={'request': self.request})
        if serializer.is_valid():
            serializer.save()
            return Response({"Success": "Password updated successfully"},status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


