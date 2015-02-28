from rest_framework import serializers
from models import Location, Story

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'state', 'zipcode', 'lon', 'lat')

class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ('id', 'created_at', 'updated_at',
                  'user', 'title', 'location', 'content', 'image')