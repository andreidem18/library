from authors.models import Author
from publishers.models import Publisher
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from publishers.serializer import PublisherSerializer
from books.serializer import BookSerializer
from books.models import Book
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from authors.serializer import AuthorSerializer

class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    @action(methods=['GET', 'POST', 'DELETE'], detail = True)
    def publisher(self, request, pk):
        book = Book.objects.get(id = pk)
        if request.method == 'GET':
            serialized = PublisherSerializer(book.publisher)
            return Response(
                status = status.HTTP_200_OK,
                data = serialized.data
            )

        if request.method == 'POST':
            publisher = Publisher.objects.get(id=request.data['publisher'])
            book.publisher = publisher
            book.save()
            return Response(status = status.HTTP_200_OK)

        if request.method == 'DELETE':
            book.publisher = None
            book.save()
            return Response(status = status.HTTP_204_NO_CONTENT)
            
    @action(methods=['GET', 'POST', 'DELETE'], detail = True)
    def authors(self, request, pk):
        book = Book.objects.get(id = pk)
        if request.method == 'GET':
            serialized = AuthorSerializer(book.authors, many = True)
            return Response(
                status = status.HTTP_200_OK,
                data = serialized.data
            )

        if request.method == 'POST':
            authors = Author.objects.filter(id__in = request.data['authors'])
            book.authors.set(authors)
            return Response(status = status.HTTP_200_OK)

        if request.method == 'DELETE':
            for author_id in request.data['authors']:
                author = Author.objects.get(id=author_id)
                book.authors.remove(author)
            return Response(status = status.HTTP_204_NO_CONTENT)