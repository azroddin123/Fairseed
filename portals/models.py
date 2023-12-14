from django.db import models
import uuid
# Create your models here.


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    id         = models.UUIDField(default=uuid.uuid4,primary_key=True)

    class Meta:
        abstract = True


