from rest_framework import serializers
from models import Author

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'user',
                  'company', 'title',
                  'employed', 'part_time')
