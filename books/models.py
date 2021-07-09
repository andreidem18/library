from django.db import models
from core.models import BaseModel
from publishers.models import Publisher
from authors.models import Author
from publishers.models import Publisher

class Book(BaseModel):
    name = models.CharField(max_length=100)
    pages = models.IntegerField()
    genre = models.CharField(max_length=100)
    relased_date = models.DateField()
    publisher =  models.ForeignKey(
        Publisher,
        related_name='books',
        on_delete=models.SET_NULL,
        null = True
    )
    authors = models.ManyToManyField(
        Author,
        related_name='books'
    )

    def __str__(self):
        return self.name