# Accouns folder choices 
# Make all choices CapitAL 
from .constants import * 
from django.db import models 

class UserChoices(models.TextChoices):
    INDIVIDUAL = INDIVIDUAL,INDIVIDUAL 
    NGO        = NGO,NGO


class RoleChoices(models.TextChoices):
    NORMAL            = NORMAL,NORMAL
    CAMPAIGN_APPROVER = CAMPAIGN_APPROVER,CAMPAIGN_APPROVER
    CAMPAIGN_MANAGER  = CAMPAIGN_MANAGER,CAMPAIGN_MANAGER
    ADMIN             = ADMIN ,ADMIN 


ROLE_CHOICES = [
    ("normal" ,"Normal")   , 
    ("campaign_approver" , "Campaign_Approver"),
    ("campaign_manager", "Campaign_Manager"),
    ("admin","Admin")
]


# Campaign Choices 


class ZakatChoices(models.TextChoices):
    YES = YES,YES
    NO  = NO,NO


class RaiseChoices(models.TextChoices):
    SELF  = SELF,SELF
    OTHER =  OTHER,OTHER


class CampaignChoices(models.TextChoices):
    PENDING    = PENDING,PENDING
    ACTIVE     = ACTIVE,ACTIVE
    COMPLETED  = COMPLETED,COMPLETED
    REJECTED   = REJECTED,REJECTED


class CourseChoices(models.TextChoices):
    UNDERGRADUATE = UNDERGRADUATE,UNDERGRADUATE
    POSTGRADUATE = POSTGRADUATE,POSTGRADUATE
    DOCTORATE,DOCTORATE,DOCTORATE



COURSE_CHOICES  = [
    ("undergraduate","undergraduate"),
    ("postgraduate","postgraduate"),
    ("doctorate","doctorate")
]
# Donor 

class DonationChoices(models.TextChoices):
    GENERAL_DONATION = GENERAL_DONATION,GENERAL_DONATION
    ZAKAT = ZAKAT,ZAKAT
    INTEREST_OFFLOADING = INTEREST_OFFLOADING,INTEREST_OFFLOADING


DONATION_CHOICES  = [
    ("genral_donation","general_donation"),
    ("zakat","zakat"),
    ("interest_offloading","interest_offloading")
]


class PaymentChoices(models.TextChoices):
    BANK_TRANSFER = BANK_TRANSFER,BANK_TRANSFER
    UPI = UPI,UPI
