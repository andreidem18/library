from rest_framework.serializers import ModelSerializer
from authors.models import Author

class AuthorSerializer(ModelSerializer):

    class Meta:
        model = Author
        fields = ('id', 'firstname', 'lastname', 'dob', 'dod', 'nationality', 'books')

class CreateAuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = ('firstname', 'lastname', 'dob', 'dod', 'nationality')