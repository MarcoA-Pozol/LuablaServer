from django.db import models
from datetime import datetime

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, default=datetime.now())
    updated_at = models.DateTimeField(auto_now_add=True, default=datetime.now())

    class Meta:
        abstract = True
