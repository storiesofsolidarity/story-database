from rest_framework import serializers
from models import Location, Story

from people.serializers import AuthorSerializer

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'city', 'state', 'zipcode', 'lon', 'lat')

class LocationStoriesSerializer(serializers.ModelSerializer):
    story_count = serializers.IntegerField(
        read_only=True
    )
    class Meta:
        model = Location
        fields = ('id', 'city', 'state', 'zipcode', 'lon', 'lat', 'story_count')


class StorySerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    location = LocationSerializer()

    class Meta:
        model = Story
        fields = ('id', 'created_at', 'updated_at',
                  'title', 'location', 'content',
                  'author')