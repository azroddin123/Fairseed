from django.urls import path 

from .views import * 


urlpatterns = [

    path('pgsetting',PGApi.as_view()),
    path('pgsetting/<int:pk>',PGApi.as_view()),

    path('paypal',PaypalApi.as_view()),
    path('paypal/<int:pk>',PaypalApi.as_view()),

    path('stripe',StripeApi.as_view()),
    path('stripe/<int:pk>',StripeApi.as_view()),

    path('bank-transfer',BankTransferApi.as_view()),
    path('bank-transfer/<int:pk>',BankTransferApi.as_view()),

    path('razorpay',RazorpayApi.as_view()),
    path('razorpay/<int:pk>',RazorpayApi.as_view()),

    path('phonepay',PhonepayApi.as_view()),
    path('phonepay/<int:pk>',PhonepayApi.as_view()),

    path('qr-transfer',QRTransferApi.as_view()),
    path('qr-transfer/<int:pk>',QRTransferApi.as_view()),

    

]
