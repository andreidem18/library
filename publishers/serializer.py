# from books.serializer import ToPublishersBookSerializer
from rest_framework.serializers import ModelSerializer
from publishers.models import Publisher

class PublisherSerializer(ModelSerializer):

    # books = ToPublishersBookSerializer(read_only=True, many=True)
    class Meta:
        model = Publisher
        # fields = ('id', 'name', 'founded_year', 'country', 'books')
        fields = ('id', 'name', 'founded_year', 'country')

class CreatePublisherSerializer(ModelSerializer):
    class Meta:
        model = Publisher
        fields = ('name', 'founded_year', 'country')