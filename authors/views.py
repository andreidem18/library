from rest_framework.response import Response
from books.serializer import ToAuthorsBookSerializer
from books.models import Book
from authors.serializer import AuthorSerializer, CreateAuthorSerializer
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from authors.models import Author
from rest_framework.decorators import action
from rest_framework import status
from django.core.mail import send_mail

class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def  get_queryset(self):
        data = {}
        if self.request.query_params:
            for k, v in self.request.query_params.items():
                if k == 'page':
                    continue
                data[k] = v
        return self.queryset.filter(**data)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateAuthorSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        send_mail(
            subject = "Info about library.api",
            message = "You have been added in our system!",
            from_email = "library@api.com",
            recipient_list = [f"{request.data['firstname']}@gmail.com"],
            fail_silently = False
        )
        return super().create(request, *args, **kwargs)

    @action(methods=['GET', 'POST', 'DELETE'], detail = True)
    def books(self, request, pk):
        author = Author.objects.get(id = pk)
        if request.method == 'GET':
            serialized = ToAuthorsBookSerializer(author.books, many = True)
            return Response(data = serialized.data, status=status.HTTP_200_OK)

        if request.method == 'POST':
            books = Book.objects.filter(id__in = request.data['books'])
            author.books.set(books)
            return Response(status = status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            for id in request.data['books']:
                book = Book.objects.get(id = id)
                author.books.remove(book)
            return Response(status = status.HTTP_204_NO_CONTENT)