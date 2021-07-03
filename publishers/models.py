from django.db import models
from django.db.models.fields import CharField
from core.models import BaseModel

class Publisher(BaseModel):
    name = models.CharField(max_length=100)
    founded = models.DateField()
    country = models.CharField(max_length=100)