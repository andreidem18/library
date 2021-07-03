from django.db import models
from core.models import BaseModel

class Publisher(BaseModel):
    name = models.CharField(max_length=100)
    founded_year = models.IntegerField()
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name