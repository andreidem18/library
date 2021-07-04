from rest_framework.serializers import ModelSerializer
from publishers.serializer import PublisherSerializer
from authors.serializer import AuthorSerializer
from books.models import Book

class BookSerializer(ModelSerializer):

    publisher = PublisherSerializer(read_only=True)
    authors = AuthorSerializer(read_only=True, many=True)
    class Meta:
        model = Book
        fields = ('id', 'name', 'pages', 'genre', 'relased_date', 'publisher', 'authors')

    
class CreateBookSerializer(ModelSerializer):

    class Meta:
        model = Book
        fields = ('id', 'name', 'pages', 'genre', 'relased_date', 'publisher', 'authors')

class ToPublishersBookSerializer(ModelSerializer):
    
    class Meta:
        model = Book
        fields = ('id', 'name', 'pages', 'genre', 'relased_date', 'authors')

class ToAuthorsBookSerializer(ModelSerializer):

    class Meta:
        model = Book
        fields = ('id', 'name', 'pages', 'genre', 'relased_date', 'publisher')