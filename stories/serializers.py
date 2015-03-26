from rest_framework import serializers
from models import Location, Story

from people.serializers import UserSerializer

class LocationSerializer(serializers.ModelSerializer):
    story_count = serializers.IntegerField(
        read_only=True
    )

    class Meta:
        model = Location
        fields = ('id', 'city', 'state', 'zipcode', 'lon', 'lat', 'story_count')

class StorySerializer(serializers.ModelSerializer):
    author_user = UserSerializer(source='author.user')

    class Meta:
        model = Story
        fields = ('id', 'created_at', 'updated_at',
                  'author_user', 'title', 'location', 'content')