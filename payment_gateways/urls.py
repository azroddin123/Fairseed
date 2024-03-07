from django.urls import path 

from .views import * 


urlpatterns = [

    path('pgsetting',PGApi.as_view()),
    path('pgsetting/<str:pk>',PGApi.as_view()),

    path('bank-transfer',BankTransferApi.as_view()),
    path('bank-transfer/<str:pk>',BankTransferApi.as_view()),

    path('phonepay',PhonepayApi.as_view()),
    path('phonepay/<str:pk>',PhonepayApi.as_view()),


]
