from rest_framework import serializers
from models import Author
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name')

class AuthorSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Author
        fields = ('id', 'user', 'photo',
                  'company', 'title',
                  'employed', 'part_time')
