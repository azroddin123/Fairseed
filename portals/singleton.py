# from django.db import models
# import uuid

# class SingletonModelManager(models.Manager):
#     def get_or_create_singleton(self):
#         obj, created = self.get_or_create(pk=1)  # Assuming you always use pk=1 for the single record
#         return obj

# class SingletonModel(models.Model):
#     # Your fields go here...
#     id         = models.UUIDField(default=uuid.uuid4,primary_key=True)
#     created_on = models.DateTimeField(auto_now_add=True,editable=False)
#     updated_on = models.DateTimeField(auto_now=True)
 
   
#     objects = SingletonModelManager()
    
#     class Meta:
#         abstract = True
#         ordering = ("-created_on",)

#     def save(self, *args, **kwargs):
#         # Ensure only one record exists         if not self.id:
#         self.pk = uuid.UUID("64327d9d-b9aa-46dc-a49a-1b78a410ea70")
#         super().save(*args, **kwargs)


# import uuid
# from django.db import models

# class SingletonModelManager(models.Manager):
#     def get_or_create_singleton(self):
#         obj, created = self.get_or_create(pk=1)
#         return obj

# class SingletonModel(models.Model):
#     id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
#     created_on = models.DateTimeField(auto_now_add=True, editable=False)
#     updated_on = models.DateTimeField(auto_now=True)

#     objects = SingletonModelManager()

#     class Meta:
#         abstract = True
#         ordering = ("-created_on",)

#     def save(self, *args, **kwargs):
#         # Ensure only one record with a specific UUID (e.g., UUID of 1)
#         if not self.id:
#             self.id = uuid.UUID("00000000-0000-0000-0000-000000000001")  # Change this to the desired UUID
#         super().save(*args, **kwargs)

# # Example usage:
# # singleton_instance = SingletonModel.objects.get_or_create_singleton()
        

# import uuid
# from django.db import models

# class SingletonModelManager(models.Manager):
#     def get_or_create_singleton(self):
#         obj, created = self.get_or_create(pk=1)
#         return obj

# class SingletonModel(models.Model):
#     id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
#     created_on = models.DateTimeField(auto_now_add=True, editable=False)
#     updated_on = models.DateTimeField(auto_now=True)

#     class Meta:
#         abstract = True
#         ordering = ("-created_on",)

#     def save(self, *args, **kwargs):
#         # Ensure only one record with a specific UUID (e.g., UUID of 1)
#         if not self.id:
#             self.id = uuid.UUID("00000000-0000-0000-0000-000000000001")  # Change this to the desired UUID

#         super().save(*args, **kwargs)

# class ConcreteSingletonModel(SingletonModel):
#     objects = SingletonModelManager()

# Example usage:
# singleton_instance = ConcreteSingletonModel.objects.get_or_create_singleton()


