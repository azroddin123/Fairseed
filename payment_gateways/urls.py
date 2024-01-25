from django.urls import path 

from .views import * 


urlpatterns = [

    path('pgsetting',PGApi.as_view()),
    path('pgsetting/<str:pk>',PGApi.as_view()),

    path('paypal',PaypalApi.as_view()),
    path('paypal/<str:pk>',PaypalApi.as_view()),

    path('stripe',StripeApi.as_view()),
    path('stripe/<str:pk>',StripeApi.as_view()),

    path('bank-transfer',BankTransferApi.as_view()),
    path('bank-transfer/<str:pk>',BankTransferApi.as_view()),

    path('razorpay',RazorpayApi.as_view()),
    path('razorpay/<str:pk>',RazorpayApi.as_view()),

    path('phonepay',PhonepayApi.as_view()),
    path('phonepay/<str:pk>',PhonepayApi.as_view()),

    path('qr-transfer',QRTransferApi.as_view()),
    path('qr-transfer/<str:pk>',QRTransferApi.as_view()),

    ###############################################

    path('pg-general/',PG_General.as_view()),
    
    path('paypalapi/',PayPalApi.as_view()),

    path('stripeapi/',StripeApi.as_view()),
    
    path('razorpayapi/',RazorPayApi.as_view()),
    
    path('qrtransferapi/',QRTransferApi.as_view()),

    path('phonepayapi/',PhonePayApi.as_view()),



]
