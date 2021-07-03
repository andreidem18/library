from authors.serializer import AuthorSerializer, CreateAuthorSerializer
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from authors.models import Author

class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateAuthorSerializer
        return super().get_serializer_class()

