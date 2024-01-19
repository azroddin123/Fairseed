from django.db import models
import uuid
# Create your models here.


class BaseModel(models.Model):
    id         = models.UUIDField(default=uuid.uuid4,primary_key=True)
    created_on = models.DateTimeField(auto_now_add=True,editable=False)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ("-created_on",)


# class SameModel(models.Model):
#     id         = models.UUIDField(default=uuid.uuid4,primary_key=True)
#     created_on = models.DateTimeField(auto_now_add=True,editable=False)
#     updated_on = models.DateTimeField(auto_now=True)
 
#     class Meta:
#         abstract = True
#         ordering = ("-created_on",)
    

# class SingletonModel(models.Model):
#     def save(self,*args, **kwargs):
#         self.pk = 1
#         super().save(*args, **kwargs)

# class Social(SingletonModel):
#     facebook_url  = models.CharField(max_length=124)
#     twitter_url   = models.CharField(max_length=124)
#     instagram_url = models.CharField(max_length=124)
        

# Correct spelling 
# i