# Accouns folder choices 

USER_TYPES = [
    ('as INDIVIDUAL', 'Indiviudal'),
    ('as NGO', 'NGO'),
]


ROLE_CHOICES = [
    ("normal" ,"Normal")   , 
    ("campaign_approver" , "Campaign_Approver"),
    ("campaign_manager", "Campaign_Manager"),
    ("admin","Admin")
]


# Campaign Choices 

ZAKAT_CHOICES = [
    ('yes', 'yes'),
    ('no', 'no'),
]

RAISE_CHOICES = [
    ('self','self'),
    ('others','others')
]


CAMPAIGN_CHOICES = [
    ('pending',"pending"),
    ('active',"active"),
    ("completed" ,"completed"),
    ("rejected" , "completed")
]

COURSE_CHOICES  = [
    ("undergraduate","undergraduate"),
    ("postgraduate","postgraduate"),
    ("doctorate","doctorate")
]
# Donor 

DONATION_CHOICES  = [
    ("genral_donation","general_donation"),
    ("zakat","zakat"),
    ("interest_offloading","interest_offloading")
]

PAYMENT_CHOICES = [
    ("bank_transfer" ,"bank_transfer"),
    ("upi/credit_card/" ,"upi")
]


# DONATION_CHOICES = [
#     ("bank_transfer" ,"bank_transfer"),
#     ("upi/credit_card/" ,"upi")
# ]