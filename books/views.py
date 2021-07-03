from books.serializer import BookSerializer
from books.models import Book
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer