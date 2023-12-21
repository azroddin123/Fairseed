from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework.views import APIView
from fairseed.GM1 import GenericMethodsMixin
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ValidationError
from django.db.models import Sum

class PagesAPi(APIView):
    def get(self, request, pk=None):
        try : 
            if pk:
                data = Pages.objects.get(pk=pk)
                serializer = PageSerializer(data)
            else:
                data = Pages.objects.all()
                serializer = PageSerializer(data, many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
        except Pages.DoesNotExist:
            return Response({"error" : "Record not found or exists"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request,pk=None):
        try : 
            if pk==None or pk == 0 :
                serializer = PageSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            

    def put(self, request, pk):
        try : 
            data = Pages.objects.get(pk=pk)
            serializer = PageSerializer(data, data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Pages.DoesNotExist:
            return Response({"error" : "Record not found or exists"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try : 
            data = Pages.objects.get(pk=pk)
            data.delete()
            return Response({"SUCCESS" : "Record Deleted Successfully"},status=status.HTTP_204_NO_CONTENT)
        except Pages.DoesNotExist:
            return Response({"error" : "Record not found or exists"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class GeneralSettingApi(GenericMethodsMixin,APIView):
    model = GeneralSetting
    serializer_class = GSSerializer
    lookup_field = "id"

    def post(self,request,pk=None,*args, **kwargs):
        try : 
            if pk==None or pk == 0 :
                serializer = GSSerializer(data=request.data)
                if serializer.is_valid():
                    gs = serializer.save()
                    kl = []
                    for item in request.data['keywords'] :
                        kl.append(Keyword(name=item,gs=gs))
                    res = Keyword.objects.bulk_create(kl)
                    print(res)

                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

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

# class PagesApi(GenericMethodsMixin,APIView):
#     model = Pages
#     serializer_class = PageSerializer
#     lookup_field = "id"



