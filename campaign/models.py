from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import FileExtensionValidator


# Create your models here.


class CampaignCatagories(models.Model):
    name   = models.CharField(max_length=50)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.name

ZAKAT_CHOICES = [
    ('yes', 'yes'),
    ('no', 'no'),
]

RAISE_CHOICES = [
    ('self','self'),
    ('others','others')
]

class CampaignCause(models.Model):
    cause_title = models.CharField(max_length=100)
    cause_img   = models.ImageField(upload_to="static/media_files/",blank=True, null=True)

    def __str__(self):
        return self.cause_title

class Campaign(models.Model):
    catagory        = models.ForeignKey(CampaignCatagories,on_delete=models.CASCADE)
    user            = models.ForeignKey(User,on_delete=models.CASCADE)
    rasing_for      = models.CharField(choices=RAISE_CHOICES,max_length=124)
    title           = models.CharField(max_length=50)
    goal_amount     = models.PositiveIntegerField(validators=[MinValueValidator(100, message="Value must be greater than or equal to 0"),
                    MaxValueValidator(1000, message="Value must be less than or equal to 100")])
    fund_raised     = models.PositiveIntegerField(validators=[MinValueValidator(100, message="Value must be greater than or equal to 0"),
                    MaxValueValidator(10000, message="Value must be less than or equal to 100")],null=True, blank=True)
    location        = models.CharField(max_length=124)
    zakat_eligible  = models.CharField(choices=ZAKAT_CHOICES,max_length=124)
    description     = models.TextField()
    summary         = models.TextField()
    status          = models.BooleanField(default=False)
    is_features     = models.BooleanField(default=False)
    is_reported     = models.BooleanField(default=False)
    is_scholarship  = models.BooleanField(default=False)
    course          = models.CharField(max_length=50,blank=True,null=True)
    is_successful   = models.BooleanField(default=False)  # to count successful campaign
    is_std_benenfited = models.BooleanField(default=False) # to count successful student benefited
    

    # def __str__(self):
    #     return self.is_std_benenfited

    def post_save(self, *args, **kwargs):
        super.save(*args, **kwargs)
        if self.fund_raised==self.goal_amount:
            self.is_successful = True
            self.save()

@receiver(post_save, sender=Campaign)
def update_cam_status(sender, instance, **kwargs):
    if instance.fund_raised == instance.goal_amount:
        Campaign.objects.filter(pk=instance.pk).update(is_successful=True)

# @receiver(post_save, sender=Campaign)
# def update_std_benefited(sender, instance, **kwargs):
#     # std= Campaign.objects.filter(catagory='Education')
#     if instance.catagory.name == 'Education' and instance.fund_raised == instance.goal_amount:
#         print(f"Setting is_std_benefited to True for campaign {instance.pk}")
#         Campaign.objects.filter(pk=instance.pk).update(is_std_benenfited=True)
#         instance.is_std_benenfited += 1
#         instance.save()



class BenificiaryBankDetails(models.Model):
    Campaign            = models.ForeignKey(Campaign,on_delete=models.CASCADE)
    account_holder_name = models.CharField(max_length=124)
    account_number      = models.PositiveIntegerField()
    bank_name           = models.CharField(max_length=124)
    branch_name         = models.CharField(max_length=124)
    ifsc_code           = models.CharField(max_length=124)
    passbook_image      = models.ImageField(upload_to="static/media_files/",blank=True,null=True,)


class KycDetails(models.Model):
    pan_card      = models.CharField(max_length=10)
    pan_img       = models.ImageField(upload_to="static/media_files/",blank=True,null=True,)
    adhar_no      = models.CharField(max_length=16)
    adhar_image   = models.ImageField(upload_to="static/media_files/",blank=True,null=True,)
    other_details = models.TextField()
    isVerified    = models.BooleanField(default=False)












