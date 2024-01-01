from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

# class GenericMethodsMixin:
#     def __init__(self) -> None:
#         self.model = self.get_model()
#         self.queryset = self.get_queryset()
#         self.serializer = self.get_serializer_class()
#         self.lookup = self.get_lookup()
#         self.query = self.get_query()

#     def get_lookup(self):
#         return self.lookup_field

#     def get_serializer_class(self):
#         return self.serializer_class

#     def get_model(self):
#         return self.model

#     def get_queryset(self):
#         return self.model.objects.all()

#     def get_query(self):
#         return self.get_query

#     def get(self, request, uuid=None, *args, **kwargs):
#         filter = {self.lookup: uuid}
#         if uuid == 0 or uuid == None:
            
#             try:
#                 return Response({"error" : False,"data":self.serializer(self.model.objects.all(), many=True).data},
#                     status=status.HTTP_200_OK,
#                 )
#             except:
#                 return Response(
#                     {
#                         "Error": str(self.model._meta).split(".")[1]
#                         + " object does not exists"
#                     },
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )
#         else:
#             try:
#                 return Response({"error":False,"data" : 
#                     self.serializer(self.model.objects.get(uuid=uuid)).data},
#                     status=status.HTTP_200_OK,
#                 )
#             except self.model.DoesNotExist:
#                   return Response(
#             { "error" : True,
#                 "message": str(self.model._meta).split(".")[1] + " object does not exists"
#             },
#             status=status.HTTP_400_BAD_REQUEST,
#         )

#     def post(self, request, uuid=None,*args, **kwargs):
#         # if request.data['created_by'] : request.data['created_by'] = request.user.id
#         if uuid==0 or uuid == None :
#             serializer = self.serializer(data=request.data)
#             if serializer.is_valid():
#                 print("serializer data ")
#                 serializer.save()
#                 data = serializer.data
#                 return Response({ "error" : False,"data" : serializer.data}, status=status.HTTP_201_CREATED)
#             else:
#                 return Response({"error" : True , "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

#     def put(self, request, uuid, *args, **kwargs):
#         print("In request data" ,)
#         filter = {self.lookup: uuid}
#         try : 
#             object1 = self.model.objects.get(**filter)
#             serializer = self.serializer(object1, data=request.data, partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response({ "error" : False,"data" : serializer.data}, status=status.HTTP_202_ACCEPTED)
#             return Response({"error" : True , "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
#         except self.model.DoesNotExist:
#                   return Response(
#             { "error" : True,
#                 "message": str(self.model._meta).split(".")[1] + " object does not exists"
#             },
#             status=status.HTTP_400_BAD_REQUEST,)

#     def delete(self, request, uuid, *args, **kwargs):
#         try : 
#             data = self.model.objects.get(uuid=uuid)
#             if data:
#                 data.delete()
#                 return Response(
#                     {"error" : False, "data": "Record Deleted Successfully"},
#                     status=status.HTTP_204_NO_CONTENT,
#                 )
#             return Response(
#                 { "error" : True,
#                     "message": str(self.model._meta).split(".")[1] + " object does not exists"
#                 },
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
        
#         except self.model.DoesNotExist:
#                   return Response(
#             {   "error" : True,
#                 "message": str(self.model._meta).split(".")[1] + " object does not exists"
#             },
#             status=status.HTTP_400_BAD_REQUEST,)


class GenericMethodsMixin:
    def __init__(self) -> None:
        self.model = self.get_model()
        self.queryset = self.get_queryset()
        self.serializer = self.get_serializer_class()
        self.lookup = self.get_lookup()
        self.query = self.get_query()
        

    def get_lookup(self):
        return self.lookup_field

    def get_serializer_class(self):
        return self.serializer_class

    def get_model(self):
        return self.model

    def get_queryset(self):
        return self.model.objects.all()

    def get_query(self):
        return self.get_query

    def get(self, request, uuid=None, *args, **kwargs):
        filter = {self.lookup: uuid}
        if uuid == 0 or uuid == None:
            
            try:
                return Response({"error" : False,"data":self.serializer(self.model.objects.all(), many=True).data},
                    status=status.HTTP_200_OK,
                )
            except:
                return Response(
                    {
                        "Error": str(self.model._meta).split(".")[1]
                        + " object does not exists"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            try:
                return Response({"error":False,"data" : 
                    self.serializer(self.model.objects.get(uuid=uuid)).data},
                    status=status.HTTP_200_OK,
                )
            except self.model.DoesNotExist:
                  return Response(
            { "error" : True,
                "message": str(self.model._meta).split(".")[1] + " object does not exists"
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def post(self, request, uuid=None,*args, **kwargs):
        # if request.data['created_by'] : request.data['created_by'] = request.user.id
        if uuid==0 or uuid == None :
            serializer = self.serializer(data=request.data)
            

            if serializer.is_valid():
                print("serializer data ")
                serializer.save()
                data = serializer.data
                return Response({ "error" : False,"data" : serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({"error" : True , "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, uuid, *args, **kwargs):
        print("In request data" ,)
        filter = {self.lookup: uuid}
        try : 
            object1 = self.model.objects.get(**filter)
            serializer = self.serializer(object1, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({ "error" : False,"data" : serializer.data}, status=status.HTTP_202_ACCEPTED)
            return Response({"error" : True , "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except self.model.DoesNotExist:
                  return Response(
            { "error" : True,
                "message": str(self.model._meta).split(".")[1] + " object does not exists"
            },
            status=status.HTTP_400_BAD_REQUEST,)

    def delete(self, request, uuid, *args, **kwargs):
        try : 
            data = self.model.objects.get(uuid=uuid)
            if data:
                data.delete()
                return Response(
                    {"error" : False, "data": "Record Deleted Successfully"},
                    status=status.HTTP_204_NO_CONTENT,
                )
            return Response(
                { "error" : True,
                    "message": str(self.model._meta).split(".")[1] + " object does not exists"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        except self.model.DoesNotExist:
                  return Response(
            {   "error" : True,
                "message": str(self.model._meta).split(".")[1] + " object does not exists"
            },
            status=status.HTTP_400_BAD_REQUEST,)




# from itertools import chain
# from django.db.models import Q


# class GenericMethods:
#     def getall(Model, ModelSerializer):
#         print("Azhar")
#         try:
#             return Response({"error" : False,"Data":
#                 ModelSerializer(Model.objects.all(), many=True).data},
#                 status=status.HTTP_200_OK,
#                 success=True,
                
#             )
#         except:
#             return Response(
#                 data={
#                     "Error": str(Model._meta).split(".")[1] + " object does not exists"
#                 },
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#     def getone(Model, ModelSerializer, pk):
#         try:
#             return Response({"error" : False,"data" : 
#                 ModelSerializer(Model.objects.get(id=pk)).data},
#                 status=status.HTTP_200_OK,
#             )
#         except Model.DoesNotExist:
#             return Response(
#                 data={
#                     "Error": str(Model._meta).split(".")[1] + " object does not exists"
#                 },
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#     def post(ModelSerializer, data):
#         serializer = ModelSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(data=serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(data=serializer.errors, status=status.HTTP_200_OK)

#     def put(Model, ModelSerializer, data, id):
#         classroom = Model.objects.get(id=id)
#         serializer = ModelSerializer(classroom, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
#         return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


