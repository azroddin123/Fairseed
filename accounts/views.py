import random
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
from portals.GM1 import GenericMethodsMixin
from .models import *
from .serializers import *
########################################################################        
class EmailSMTP(APIView):
    def post(self, request, *args, **kwargs):
        serializer = EmailSMTPSerializer(data=request.data)
        if serializer.is_valid():
            subject = serializer.validated_data['subject']
            message = serializer.validated_data['message']

            # recipient = serializer.validated_data['recipient']
            recipients = list(User.objects.values_list('email', flat=True))

            try:
                for recipient_email in recipients:
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        [recipient_email],
                        fail_silently=False,
                    )
                return Response({'message': 'Email sent successfully.'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'message': f'Error sending email: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        

# class RegisterApi(APIView):
#      def get(self, request, user_id):
#         try:
#             user = User.objects.get(id=user_id)
#         except User.DoesNotExist:
#             return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

#         serializer = UserSerializer1(user)
#         return Response(serializer.data)
    

class RegisterApi(APIView):
    def get(self, request):
        u1 = User.objects.all()
        serializer = UserSerializer1(u1, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer1(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 200,
                'message': 'Registration successful.',
                'data': serializer.data,
            })
        return Response({
            'status': 400,
            'message': 'Registration failed.',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        # u2 = User.objects.get(pk=pk)
        u2 = User.objects.filter(pk=pk).first()
        serializer = UserSerializer1(u2, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 200,
                'message': 'User information updated successfully.',
                'data': serializer.data,
            })
        return Response({
            'status': 400,
            'message': 'Update failed.',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

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


