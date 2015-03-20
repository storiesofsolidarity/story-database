from rest_framework import serializers
from models import Location, Story

from people.serializers import UserSerializer

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'state', 'zipcode', 'lon', 'lat')

class StorySerializer(serializers.ModelSerializer):
    author_user = UserSerializer(source='author.user')

    class Meta:
        model = Story
        fields = ('id', 'created_at', 'updated_at',
                  'author_user', 'title', 'location', 'content')