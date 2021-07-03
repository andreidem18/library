from django.db import models
from core.models import BaseModel

class Author(BaseModel):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    dob = models.DateField()
    dod = models.DateField(null=True)
    nationality = models.CharField(max_length=100)

    def __str__(self):
        return self.firstname
