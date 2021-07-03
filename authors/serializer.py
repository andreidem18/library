# from books.serializer import BookSerializer
from rest_framework.serializers import ModelSerializer
from authors.models import Author

class AuthorSerializer(ModelSerializer):

    # books = BookSerializer(read_only = True, many = True)
    class Meta:
        model = Author
        fields = ('id', 'firstname', 'lastname', 'dob', 'dod', 'nationality', 'books')

class CreateAuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = ('firstname', 'lastname', 'dob', 'dod', 'nationality')