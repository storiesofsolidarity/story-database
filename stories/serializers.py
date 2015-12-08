from django.conf import settings
from rest_framework import serializers
from models import Location, Story

from localflavor.us.us_states import US_STATES

from people.models import Author
from people.serializers import AuthorSerializer


# to remove
class LocationSerializer(serializers.ModelSerializer):
    city = serializers.CharField(source='city_fmt', allow_blank=True, required=False)
    state = serializers.CharField(source='state_fmt', allow_blank=True, required=False)
    county = serializers.CharField(source='county_fmt', allow_blank=True, required=False)

    class Meta:
        model = Location
        fields = ('id', 'zipcode', 'city', 'county', 'state', 'lon', 'lat')


class StateStoriesSerializer(serializers.ModelSerializer):
    abbr = serializers.CharField(source='location__state')
    name = serializers.SerializerMethodField('state_full')
    story_count = serializers.IntegerField(read_only=True, source='id__count')

    def state_full(self, obj):
        abbr = obj.get('location__state')
        if abbr:
            return dict(US_STATES)[abbr]
        else:
            return ""

    class Meta:
        model = Location
        fields = ('id', 'abbr', 'name', 'story_count')


class CountyStoriesSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='location__county')
    story_count = serializers.IntegerField(read_only=True, source='id__count')

    class Meta:
        model = Location
        fields = ('id', 'name', 'story_count')


class ZipcodeStoriesSerializer(serializers.ModelSerializer):
    story_count = serializers.IntegerField(read_only=True, source='id__count')
    zipcode = serializers.CharField(source='location__zipcode')

    class Meta:
        model = Location
        fields = ('id', 'zipcode', 'story_count')


class LocationStoriesSerializer(serializers.ModelSerializer):
    story_count = serializers.IntegerField(read_only=True)
    city = serializers.CharField(source='city_fmt')
    state = serializers.CharField(source='state_fmt')

    class Meta:
        model = Location
        fields = ('id', 'zipcode', 'city', 'state', 'lon', 'lat', 'story_count')


class StorySerializer(serializers.ModelSerializer):
    author = AuthorSerializer(required=False)
    location = LocationSerializer(required=False)
    photo = serializers.SerializerMethodField('get_photo_url')
    content = serializers.CharField(error_messages={'required': "Share a story before submitting"})

    def get_photo_url(self, obj):
        if obj.photo:
            return '%s%s' % (settings.MEDIA_URL, obj.photo)
        else:
            return ''

    #abuse to_relationship to hide name for anonymous authors
    def to_representation(self, instance):
        data = super(StorySerializer, self).to_representation(instance)
        if data['anonymous'] or data['author']['anonymous']:
            name = data.pop('author')
            return data
        return data

    def create(self, validated_data):
        "Handles nested data and model lookup or creation for author and location."

        initial_data = self.initial_data  # instead of validated_data, which won't include non-named fields
        name = initial_data.get('name')
        author, new_author = Author.objects.get_or_create_user(user__name=name)
        validated_data['author'] = author

        city = initial_data.get('location.city')
        state = initial_data.get('location.state')
        if (city and state) or state:
            location, new_location = Location.objects.get_or_create(city=city, state=state)
            if new_location:
                location.geocode('%s, %s' % (city, state))
                location.save()
            validated_data['location'] = location
        else:
            # overwrite the empty dict to avoid validation errors
            validated_data['location'] = None

        # save the photo
        if 'photo' in initial_data:
            validated_data['photo'] = initial_data['photo']

        story = Story.objects.create(**validated_data)  # here use validated_data which will include new objects
        return story

    class Meta:
        model = Story
        fields = ('id', 'created_at', 'updated_at',
                  'location', 'content', 'photo', 'author', 'anonymous')
