from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.core.exceptions import ValidationError
from itertools import chain
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from django.core.paginator import Paginator,EmptyPage
import math

class GenericMethodsMixin:
    def __init__(self, serializer_class=None, create_serializer_class=None) -> None:
        self.model = self.get_model()
        self.queryset = self.get_queryset()
        self.serializer = self.get_serializer_class()
            
        self.lookup = self.get_lookup()
        self.query = self.get_query()

        
    def get_lookup(self):
        return self.lookup_field

    def get_serializer_class(self):
        return self.serializer_class
    
    def get_create_serializer(self):
        try:
            return self.create_serializer_class
        except:
            return self.serializer

    def get_model(self):
        return self.model

    def get_queryset(self):
        return self.model.objects.all()

    def get_query(self):
        return self.get_query
    
    def handle_does_not_exist_error(self):
        return Response(
            {"error": True, "message": f"{self.model._meta} object does not exist"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    
    def get_paginated_data(self, request):
        # page_number = int(request.GET.get('page', 0))  if we want the last page record on first page 
        data = self.model.objects.all()
        try:
            serializer = self.serializer_class(data, many=True)
            return Response({
                "error": False,
                "count": len(data) or 0 ,
                "rows": serializer.data,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": True, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_single_data(self, pk):
        try:
            # here we can add authentication and authorization
            print("get single data")
            data = self.model.objects.get(pk=pk)
            serializer = self.serializer_class(data)
            return Response({"error": False, "data": serializer.data}, status=status.HTTP_200_OK)
        except self.model.DoesNotExist:
            return self.handle_does_not_exist_error()

    # for post method
    def create_data(self, request):
        create_serializer_class = self.get_create_serializer()
        serializer  = create_serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"error": False, "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": True, "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
      
    def get(self, request, pk=None, *args, **kwargs):
        if pk in ["0", None]:
            return self.get_paginated_data(request)
        else:
            return self.get_single_data(pk)

    def post(self, request, pk=None, *args, **kwargs):
        if pk in ["0", None]:
            return self.create_data(request)
        else:
            return Response({"error": True, "message": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, *args, **kwargs):
       
        try:
            filter = {self.lookup_field: pk}
            object_instance = self.model.objects.get(**filter)
            serializer = self.create_serializer_class(object_instance,data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"error": False, "data": serializer.data}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({"error": True, "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except self.model.DoesNotExist:
            return self.handle_does_not_exist_error()
        
        except Exception as e:
            return Response({"error": True, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, *args, **kwargs):
        try:
            data = self.model.objects.get(pk=pk)
            if data:
                data.delete()
                return Response({"error": False, "data": "Record Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)
            else:
                return self.handle_does_not_exist_error()

        except ValidationError as e:
            return Response({"error": True, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, pk, *args, **kwargs):
    #     try : 
    #         data = self.model.objects.get(pk=pk)
    #         if data:
    #             data.delete()
    #             return Response(
    #                 {"error" : False, "data": "Record Deleted Successfully"},
    #                 status=status.HTTP_204_NO_CONTENT,
    #             )
    #         return Response(
    #             { "error" : True,
    #                 "message": str(self.model._meta).split(".")[1] + " object does not exists"
    #             },
    #             status=status.HTTP_400_BAD_REQUEST,
    #         )
        
    #     except self.model.DoesNotExist:
    #               return Response(
    #         {   "error" : True,
    #             "message": str(self.model._meta).split(".")[1] + " object does not exists"
    #         },
    #         status=status.HTTP_400_BAD_REQUEST,)
        
    #     except ValidationError as e:
    #             # Handle the specific error, e.g., display a custom error message
    #             return Response({
    #                 "error" : True,
    #                 "message" : str(e) 
    #             },status=status.HTTP_400_BAD_REQUEST)

    # print("paginated data")
        # limit = max(int(request.GET.get('limit', 0)), 5) 
        # page_number = max(int(request.GET.get('page', 0)), 1)  
        # # page_number = int(request.GET.get('page', 0))  if we want the last page record on first page 
        # data = self.model.objects.all()
        # print(len(data))
        # paginator = Paginator(data, limit)
        # try:
        #     current_page_data = paginator.get_page(page_number)
        # except EmptyPage:
        #     return Response(
        #         {"error": True, "message": "Page not found"},
        #         status=status.HTTP_404_NOT_FOUND
        #     )
        # serializer = self.serializer_class(current_page_data, many=True)
        # return Response({
        #     "error": False,
        #     "pages_count": paginator.num_pages,
        #     "count": paginator.count,
        #     "rows": serializer.data,
        # }, status=status.HTTP_200_OK)
        
