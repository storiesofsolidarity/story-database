from rest_framework import serializers
from models import Author
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name')


class AuthorSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    #abuse to_relationship to hide user fields for anonymous authors
    def to_representation(self, instance):
        data = super(AuthorSerializer, self).to_representation(instance)

        if data['anonymous']:
            #only show id and anon flag
            return {'id': data['id'], 'anonymous': True}
        return data

    class Meta:
        model = Author
        fields = ('id', 'user', 'photo',
                  'employer', 'occupation',
                  'employed', 'part_time', 'anonymous')
